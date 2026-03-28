"""
Test file for Iteration 3 - New Profile Features
Tests: Change Password API, PWA Manifest
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://intercultura-dev.preview.emergentagent.com')

# Test credentials
STUDENT_EMAIL = "testuser123@test.com"
STUDENT_PASSWORD = "password123"
TEACHER_EMAIL = "profesor@test.com"
TEACHER_PASSWORD = "profesor123"


class TestChangePasswordAPI:
    """Tests for POST /api/auth/change-password endpoint"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token for student"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": STUDENT_EMAIL, "password": STUDENT_PASSWORD}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        return response.json()["access_token"]
    
    def test_change_password_wrong_current_password(self, auth_token):
        """Test change password with wrong current password returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/auth/change-password",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword123"
            }
        )
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert "detail" in data
        assert "incorrecta" in data["detail"].lower() or "incorrect" in data["detail"].lower()
        print(f"✓ Wrong current password returns 400 with message: {data['detail']}")
    
    def test_change_password_short_new_password(self, auth_token):
        """Test change password with short new password returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/auth/change-password",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "current_password": STUDENT_PASSWORD,
                "new_password": "12345"  # Less than 6 characters
            }
        )
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert "detail" in data
        assert "6" in data["detail"]  # Should mention 6 characters
        print(f"✓ Short password returns 400 with message: {data['detail']}")
    
    def test_change_password_success(self, auth_token):
        """Test successful password change and revert"""
        # Change password
        new_password = "newpassword123"
        response = requests.post(
            f"{BASE_URL}/api/auth/change-password",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "current_password": STUDENT_PASSWORD,
                "new_password": new_password
            }
        )
        assert response.status_code == 200, f"Password change failed: {response.text}"
        data = response.json()
        assert "message" in data
        print(f"✓ Password changed successfully: {data['message']}")
        
        # Verify new password works by logging in
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": STUDENT_EMAIL, "password": new_password}
        )
        assert login_response.status_code == 200, "Login with new password failed"
        new_token = login_response.json()["access_token"]
        print("✓ Login with new password successful")
        
        # Revert password back to original
        revert_response = requests.post(
            f"{BASE_URL}/api/auth/change-password",
            headers={"Authorization": f"Bearer {new_token}"},
            json={
                "current_password": new_password,
                "new_password": STUDENT_PASSWORD
            }
        )
        assert revert_response.status_code == 200, "Password revert failed"
        print("✓ Password reverted to original")
        
        # Verify original password works
        final_login = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": STUDENT_EMAIL, "password": STUDENT_PASSWORD}
        )
        assert final_login.status_code == 200, "Login with original password failed"
        print("✓ Original password works again")
    
    def test_change_password_unauthenticated(self):
        """Test change password without auth token returns 401/403"""
        response = requests.post(
            f"{BASE_URL}/api/auth/change-password",
            json={
                "current_password": STUDENT_PASSWORD,
                "new_password": "newpassword123"
            }
        )
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print(f"✓ Unauthenticated request returns {response.status_code}")


class TestPWAManifest:
    """Tests for PWA manifest.json"""
    
    def test_manifest_exists(self):
        """Test that manifest.json is accessible"""
        response = requests.get(f"{BASE_URL}/manifest.json")
        assert response.status_code == 200, f"Manifest not found: {response.status_code}"
        print("✓ manifest.json is accessible")
    
    def test_manifest_intercultura_branding(self):
        """Test manifest has Intercultura branding"""
        response = requests.get(f"{BASE_URL}/manifest.json")
        assert response.status_code == 200
        data = response.json()
        
        # Check name contains Intercultura
        assert "name" in data
        assert "intercultura" in data["name"].lower(), f"Name should contain Intercultura: {data['name']}"
        print(f"✓ Manifest name: {data['name']}")
        
        # Check short_name
        assert "short_name" in data
        assert "intercultura" in data["short_name"].lower(), f"Short name should contain Intercultura: {data['short_name']}"
        print(f"✓ Manifest short_name: {data['short_name']}")
        
        # Check theme_color (Intercultura green)
        assert "theme_color" in data
        print(f"✓ Theme color: {data['theme_color']}")
        
        # Check icons
        assert "icons" in data
        assert len(data["icons"]) > 0
        print(f"✓ Icons configured: {len(data['icons'])} icon(s)")
    
    def test_favicon_exists(self):
        """Test that favicon.png is accessible"""
        response = requests.get(f"{BASE_URL}/favicon.png")
        assert response.status_code == 200, f"Favicon not found: {response.status_code}"
        assert "image" in response.headers.get("content-type", ""), "Favicon should be an image"
        print("✓ favicon.png is accessible")


class TestExistingAuthEndpoints:
    """Verify existing auth endpoints still work"""
    
    def test_login_student(self):
        """Test student login works"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": STUDENT_EMAIL, "password": STUDENT_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == STUDENT_EMAIL
        assert data["user"]["role"] == "student"
        print(f"✓ Student login successful: {data['user']['name']}")
    
    def test_login_teacher(self):
        """Test teacher login works"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEACHER_EMAIL, "password": TEACHER_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == TEACHER_EMAIL
        assert data["user"]["role"] == "teacher"
        print(f"✓ Teacher login successful: {data['user']['name']}")
    
    def test_get_me(self):
        """Test /api/auth/me endpoint"""
        # Login first
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": STUDENT_EMAIL, "password": STUDENT_PASSWORD}
        )
        token = login_response.json()["access_token"]
        
        # Get user info
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == STUDENT_EMAIL
        print(f"✓ /api/auth/me returns user: {data['name']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
