"""Enrich French lessons with real educational content aligned to Alter Ego+ textbook."""
import asyncio, os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

FR_RICH = {
"A1": [
"""Bienvenue dans votre premier cours de français ! Dans cette leçon, vous apprendrez à vous présenter et à saluer les gens.

Salutations : 'Bonjour' (hello/good morning — formel), 'Salut' (hi — informel), 'Bonsoir' (good evening), 'Bonne nuit' (good night). Au revoir : 'Au revoir' (goodbye), 'À bientôt' (see you soon), 'À demain' (see you tomorrow), 'Salut' (bye — informel).

Se présenter : 'Je m'appelle Marie' (My name is Marie). 'Comment vous appelez-vous ?' (formel) / 'Comment tu t'appelles ?' (informel) — What's your name? 'Je suis costaricien(ne)' (I am Costa Rican). 'J'ai 25 ans' (I am 25 years old — en français on dit 'j'ai' et non 'je suis').

Le verbe ÊTRE : je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont. Le verbe AVOIR : j'ai, tu as, il/elle a, nous avons, vous avez, ils/elles ont.

Note culturelle : En France, on fait la bise (on se fait un bisou sur la joue) pour se saluer entre amis. Le nombre de bises varie selon la région : une à quatre ! On dit 'vous' aux inconnus et 'tu' aux amis et à la famille.""",

"""Apprenez les nombres de 0 à 100 et comment parler de l'âge en français.

Nombres de 0 à 20 : zéro, un, deux, trois, quatre, cinq, six, sept, huit, neuf, dix, onze, douze, treize, quatorze, quinze, seize, dix-sept, dix-huit, dix-neuf, vingt.

Dizaines : trente (30), quarante (40), cinquante (50), soixante (60). Attention ! soixante-dix (70 = 60+10), quatre-vingts (80 = 4×20), quatre-vingt-dix (90 = 4×20+10). Cent (100).

Particularités : 21 = vingt et un, 31 = trente et un... mais 22 = vingt-deux (avec trait d'union). 80 = quatre-vingts (avec 's'), mais 81 = quatre-vingt-un (sans 's'). En Belgique et Suisse : septante (70), nonante (90), et en Suisse : huitante (80).

L'âge : 'Quel âge avez-vous ?' / 'Quel âge as-tu ?' — 'J'ai vingt-cinq ans'. En français, on utilise le verbe AVOIR pour l'âge : 'Elle a trente ans' (She is 30 — littéralement 'She has 30 years').

La monnaie : l'euro (€). 'Combien ça coûte ?' (How much does it cost?). 'Ça coûte dix euros cinquante' (10,50€). 'C'est cher !' (It's expensive!). 'C'est pas cher' (It's cheap).""",

"""Dans cette leçon, apprenez le vocabulaire de la famille en français.

La famille proche : le père (father), la mère (mother), le frère (brother), la sœur (sister), le fils (son), la fille (daughter), les parents (parents), les enfants (children). Le mari (husband), la femme (wife).

La famille élargie : le grand-père (grandfather), la grand-mère (grandmother), l'oncle (uncle), la tante (aunt), le cousin/la cousine (cousin), le neveu (nephew), la nièce (niece), le beau-père (father-in-law/stepfather), la belle-mère (mother-in-law/stepmother).

Décrire sa famille : 'Ma famille est grande' (My family is big). 'J'ai deux frères et une sœur' (I have two brothers and one sister). 'Mon père s'appelle Jean' (My father's name is Jean). 'Mes grands-parents habitent à Paris' (My grandparents live in Paris).

Adjectifs possessifs : mon/ma/mes (my), ton/ta/tes (your), son/sa/ses (his/her). Attention ! Devant une voyelle féminine : 'mon amie' (et non 'ma amie'). 'Ma mère est professeur'. 'Nos enfants vont à l'école'.

État civil : célibataire (single), marié(e) (married), divorcé(e) (divorced), veuf/veuve (widowed), pacsé(e) (civil partnership — très courant en France). 'Je suis marié et j'ai trois enfants'.""",

"""Apprenez à parler des professions et des activités quotidiennes.

Les professions : le professeur / la professeure (teacher), le médecin (doctor), l'avocat(e) (lawyer), l'ingénieur(e) (engineer), le/la comptable (accountant), le serveur / la serveuse (waiter/waitress), le boulanger / la boulangère (baker), l'infirmier / l'infirmière (nurse).

Masculin et féminin : Beaucoup de professions changent de forme. -eur → -euse (vendeur/vendeuse), -eur → -rice (acteur/actrice), -ien → -ienne (musicien/musicienne). Certaines ne changent pas : 'Elle est médecin'. En français moderne, on féminise de plus en plus.

Parler du travail : 'Qu'est-ce que vous faites dans la vie ?' / 'Quelle est votre profession ?' — 'Je suis ingénieur'. 'Où travaillez-vous ?' — 'Je travaille dans un hôpital'. 'Je travaille comme serveur dans un restaurant'.

Les verbes du premier groupe (-ER) : parler (je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent), travailler, habiter, aimer, manger, étudier. 'Je parle français et espagnol'. 'Nous habitons à San José'.

Les jours : lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche. 'Je travaille du lundi au vendredi'. 'Le samedi, je fais les courses' (On Saturdays, I go shopping).""",

"""Apprenez le vocabulaire de la nourriture et comment commander dans un restaurant français.

Les repas : le petit-déjeuner (breakfast), le déjeuner (lunch), le goûter (afternoon snack), le dîner (dinner). En France, le déjeuner est un repas important, souvent entre 12h et 14h.

Au restaurant : 'Une table pour deux, s'il vous plaît' (A table for two, please). 'Je voudrais voir le menu / la carte' (I'd like to see the menu). 'Qu'est-ce que vous recommandez ?' (What do you recommend?). 'Je vais prendre le poulet rôti' (I'll have the roast chicken). 'L'addition, s'il vous plaît' (The bill, please).

Nourriture française : le croissant, la baguette, le fromage (cheese — la France a plus de 400 fromages !), le vin rouge/blanc, la quiche lorraine, la ratatouille, le croque-monsieur, la crêpe, le macaron, la tarte tatin.

Les articles partitifs : du (masc.), de la (fém.), de l' (voyelle), des (pluriel). 'Je mange du pain' (I eat some bread). 'Je bois de la soupe' (I drink some soup). 'Je veux de l'eau' (I want some water). Négatif : 'Je ne mange pas de viande' (pas DE, jamais DU/DE LA après la négation).

Verbe VOULOIR : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent. Plus poli : 'Je voudrais...' (I would like). 'Vous désirez ?' (What would you like? — au restaurant).""",

"""Apprenez à vous orienter dans une ville francophone et à demander votre chemin.

Les lieux : la gare (train station), l'aéroport (airport), la banque (bank), la pharmacie (pharmacy), l'hôpital (hospital), le supermarché (supermarket), la boulangerie (bakery), la poste (post office), la bibliothèque (library — faux ami ! pas 'librairie' qui = bookshop).

Demander son chemin : 'Excusez-moi, où est la gare ?' (Excuse me, where is the station?). 'Comment aller à la pharmacie ?' (How do I get to the pharmacy?). 'C'est loin d'ici ?' (Is it far from here?). 'C'est tout près' (It's very close). 'C'est à cinq minutes à pied' (It's 5 minutes on foot).

Directions : 'Allez tout droit' (Go straight). 'Tournez à gauche/à droite' (Turn left/right). 'Prenez la première rue à gauche' (Take the first street on the left). 'Au carrefour' (at the crossroads). 'Au feu rouge' (at the traffic light). 'En face de' (across from). 'À côté de' (next to).

Les prépositions de lieu : à (in/at), dans (in/inside), sur (on), sous (under), devant (in front of), derrière (behind), entre (between). 'La pharmacie est à côté de la banque'. 'Le parc est derrière l'église'.

Le verbe ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont. 'Je vais au supermarché' (au = à + le). 'Elle va à la poste' (à la). 'Nous allons à l'école' (à l'). 'Ils vont aux toilettes' (aux = à + les)."""
],
"A2": [
"""Apprenez à décrire vos habitudes quotidiennes et votre routine.

La routine : 'Je me réveille à sept heures' (I wake up at 7). 'Je me lève, je me douche et je m'habille' (I get up, shower, and get dressed). 'Je prends le petit-déjeuner' (I have breakfast). 'Je pars au travail à huit heures' (I leave for work at 8).

Les verbes pronominaux (reflexive verbs) : se réveiller (to wake up), se lever (to get up), se laver (to wash), se doucher (to shower), s'habiller (to get dressed), se coucher (to go to bed). 'Elle se lève à six heures'. 'Nous nous couchons à onze heures'.

L'heure : 'Quelle heure est-il ?' — 'Il est huit heures' (8:00). 'Il est midi' (noon). 'Il est minuit' (midnight). 'Il est trois heures et demie' (3:30). 'Il est cinq heures moins le quart' (4:45). 'Il est une heure et quart' (1:15).

Fréquence : toujours (always), souvent (often), parfois/quelquefois (sometimes), rarement (rarely), jamais (never), tous les jours (every day), le week-end (on weekends). 'Je fais du sport trois fois par semaine'.

Le passé composé : avoir/être + participe passé. 'J'ai mangé' (I ate). 'Elle est partie' (She left — verbes de mouvement avec être). DR MRS VANDERTRAMP : devenir, revenir, monter, rester, sortir, venir, aller, naître, descendre, entrer, rentrer, tomber, retourner, arriver, mourir, partir.""",

"""Apprenez à décrire votre logement et votre environnement.

Les pièces : le salon (living room), la chambre (bedroom), la cuisine (kitchen), la salle de bains (bathroom), les toilettes (toilet — separate room in France!), l'entrée (entrance), le couloir (hallway), le balcon (balcony), le jardin (garden), le garage.

Les meubles : le lit (bed), la table (table), la chaise (chair), le canapé (sofa), l'armoire (wardrobe), le bureau (desk), le réfrigérateur/frigo (fridge), la cuisinière (stove), la machine à laver (washing machine), l'étagère (shelf).

Décrire : 'Mon appartement a trois pièces' (My apartment has three rooms). 'La cuisine est petite mais bien équipée' (The kitchen is small but well equipped). 'Il y a un grand jardin' (There is a big garden). 'C'est au troisième étage sans ascenseur' (It's on the third floor without an elevator).

L'imparfait : pour décrire le passé (habitudes, descriptions). je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient. 'Quand j'étais petit, j'habitais à la campagne' (When I was small, I lived in the countryside). 'La maison de mes grands-parents avait un grand jardin'.

Comparer : plus... que (more... than), moins... que (less... than), aussi... que (as... as). 'Paris est plus grande que Lyon'. 'Mon appartement est moins cher que le tien'. Irrégulier : bon → meilleur (better), bien → mieux (better).""",

"""Apprenez le vocabulaire de la santé et comment consulter un médecin en France.

Le corps : la tête (head), les yeux (eyes), le nez (nose), la bouche (mouth), l'oreille (ear), le bras (arm), la main (hand), la jambe (leg), le pied (foot), le dos (back), le ventre (stomach), le genou (knee).

Chez le médecin : 'J'ai mal à la tête' (I have a headache). 'J'ai de la fièvre' (I have a fever). 'J'ai mal au ventre' (I have a stomachache). 'J'ai attrapé un rhume' (I caught a cold). 'Je tousse beaucoup' (I cough a lot). 'Depuis quand avez-vous ces symptômes ?' (Since when have you had these symptoms?).

Le système de santé français : 'La Sécurité sociale rembourse environ 70% des frais médicaux'. 'La carte Vitale est la carte d'assurance maladie'. 'Il faut d'abord aller chez le médecin traitant (GP) avant de voir un spécialiste'.

Expressions avec AVOIR : avoir mal à (to have pain in), avoir faim (to be hungry), avoir soif (to be thirsty), avoir froid (to be cold), avoir chaud (to be hot), avoir peur (to be afraid). 'Tu as l'air fatigué' (You look tired).

Conseils du médecin (impératif) : 'Prenez ce médicament trois fois par jour' (Take this medicine 3 times a day). 'Reposez-vous pendant deux jours' (Rest for two days). 'Buvez beaucoup d'eau' (Drink lots of water). 'Bon rétablissement !' (Get well soon!).""",

"""Apprenez à planifier et raconter vos voyages et vacances.

Destinations populaires en France : Paris (Tour Eiffel, Louvre, Champs-Élysées), la Côte d'Azur (Nice, Cannes, Saint-Tropez), la Provence (lavande, Avignon), la Bretagne (crêpes, mer), les Alpes (ski, Mont-Blanc), la vallée de la Loire (châteaux).

À l'aéroport : 'J'ai un vol pour Paris à 10 heures' (I have a flight to Paris at 10). 'Où est l'enregistrement ?' (Where is check-in?). 'Fenêtre ou couloir ?' (Window or aisle?). 'La porte d'embarquement est la B12' (The boarding gate is B12).

À l'hôtel : 'Je voudrais réserver une chambre pour deux nuits' (I'd like to book a room for two nights). 'Une chambre simple ou double ?' (Single or double?). 'Le petit-déjeuner est-il inclus ?' (Is breakfast included?). 'À quelle heure est le check-out ?' (What time is check-out?).

Raconter au passé : Passé composé (actions) + Imparfait (contexte). 'Il faisait beau quand nous sommes arrivés' (It was nice when we arrived). 'Je visitais le musée quand il a commencé à pleuvoir' (I was visiting the museum when it started raining).

Pronoms y et en : 'Tu vas à Paris ?' — 'Oui, j'y vais demain' (y = there). 'Tu veux du fromage ?' — 'Oui, j'en veux' (en = some of it). 'J'en ai mangé trois' (I ate three of them).""",

"""Apprenez à faire du shopping et à parler de la mode en France.

Les vêtements : la robe (dress), le pantalon (pants), la jupe (skirt), la chemise (shirt), le pull (sweater), le manteau (coat), les chaussures (shoes), les bottes (boots), l'écharpe (scarf), le chapeau (hat), le sac à main (handbag).

Dans un magasin : 'Je cherche une robe noire' (I'm looking for a black dress). 'Quelle taille faites-vous ?' (What size are you?). 'Je fais du 38' (I'm a size 38 — European). 'Est-ce que je peux l'essayer ?' (Can I try it on?). 'Ça me va bien' (It fits me well). 'C'est trop grand/petit' (It's too big/small).

Les soldes : 'Les soldes d'hiver commencent en janvier et les soldes d'été en juin' (Winter sales start in January, summer sales in June). 'Il y a 30% de réduction' (There's 30% off). 'C'est une bonne affaire !' (It's a good deal!).

Les pronoms COD : me, te, le/la, nous, vous, les. 'Tu aimes cette robe ?' — 'Oui, je l'aime beaucoup' (l' = la robe). 'Ces chaussures, je les achète' (les = chaussures). 'Il m'a aidé' (He helped me). Place : avant le verbe conjugué.

Les couleurs (adjectifs) : rouge (red), bleu(e) (blue), vert(e) (green), noir(e) (black), blanc/blanche (white), jaune (yellow), rose (pink), gris(e) (grey). Invariables : orange, marron. 'Une jupe bleue', 'des chaussures noires', mais 'des chaussures orange'.""",

"""Apprenez à parler de vos souvenirs et expériences passées.

Raconter des souvenirs : 'Quand j'étais enfant, nous allions à la plage chaque été' (When I was a child, we went to the beach every summer). 'Je me souviens de mon premier jour d'école' (I remember my first day of school). 'C'était une époque formidable' (It was a wonderful time).

Imparfait vs. Passé composé : L'imparfait = habitudes, descriptions, émotions dans le passé. Le passé composé = actions ponctuelles, événements. 'Il pleuvait (imparfait) quand je suis sorti (passé composé)'. 'Je regardais (imparfait) la télé quand le téléphone a sonné (passé composé)'.

Expressions de temps : autrefois (in the past), à cette époque (at that time), quand j'étais jeune (when I was young), il y a dix ans (ten years ago), pendant (during), depuis (since/for). 'Il y a trois ans, j'ai visité Paris pour la première fois'.

Le plus-que-parfait : action antérieure à une autre action passée. avoir/être à l'imparfait + participe passé. 'Quand je suis arrivé, elle était déjà partie' (When I arrived, she had already left). 'Il avait étudié le français avant de venir en France'.

Marqueurs de discours : d'abord (first), ensuite/puis (then), après (after), enfin/finalement (finally). 'D'abord, nous avons visité le Louvre. Ensuite, nous sommes allés aux Champs-Élysées. Finalement, nous avons dîné dans un restaurant'."""
],
"B1": [
"""Discutez de l'engagement citoyen et des questions de société.

La société française : la liberté, l'égalité, la fraternité — devise de la République française. La laïcité (secularism) est un principe fondamental. 'En France, la religion est une affaire privée'. 'L'école publique est laïque, gratuite et obligatoire'.

Engagement : le bénévolat (volunteering), l'association (nonprofit organization), la manifestation (protest/demonstration), la pétition, le syndicat (trade union). 'Les Français manifestent souvent pour défendre leurs droits'. 'Les Restos du Cœur, fondés par Coluche, distribuent des repas gratuits'.

Droits sociaux : 'La France a 35 heures de travail par semaine'. 'Les salariés ont 5 semaines de congés payés'. 'Le SMIC (salaire minimum) est d'environ 1 400 € net par mois'. 'La retraite est un sujet de débat permanent en France'.

Le subjonctif : après les expressions de volonté, doute, émotion. 'Il faut que nous fassions quelque chose' (We must do something). 'Je veux que tu viennes' (I want you to come). 'Il est important que chacun participe'. Formation : radical de 'ils' au présent + -e, -es, -e, -ions, -iez, -ent.

Exprimer son opinion : 'Je pense que...' (+ indicatif), 'Je ne pense pas que...' (+ subjonctif). 'À mon avis...' (In my opinion). 'Il me semble que...' (It seems to me that). 'Je suis convaincu(e) que...' (I'm convinced that).""",

"""Explorez le monde du travail et la vie professionnelle en France.

Le CV français : état civil (personal details), formation (education), expérience professionnelle, compétences (skills), centres d'intérêt (hobbies). 'En France, on met souvent une photo sur le CV'. 'La lettre de motivation accompagne toujours le CV'.

L'entretien d'embauche : 'Parlez-moi de vous' (Tell me about yourself). 'Quels sont vos points forts et vos points faibles ?' (What are your strengths and weaknesses?). 'Où vous voyez-vous dans cinq ans ?' (Where do you see yourself in 5 years?). 'Pourquoi voulez-vous travailler chez nous ?' (Why do you want to work with us?).

Le monde du travail : le CDI (contrat à durée indéterminée — permanent contract), le CDD (contrat à durée déterminée — fixed-term), le stage (internship), l'intérim (temp work), le télétravail (remote work), la démission (resignation), le licenciement (layoff).

Les pronoms relatifs : qui (subject), que (object), où (place/time), dont (of which/whose). 'C'est l'entreprise qui m'intéresse' (It's the company that interests me). 'Le poste que je cherche est à Paris'. 'La ville où j'aimerais travailler'. 'C'est le projet dont je t'ai parlé'.

Conditionnel présent : radical du futur + terminaisons de l'imparfait. 'Je voudrais postuler pour ce poste' (I would like to apply for this position). 'J'aimerais avoir plus de responsabilités'. 'Si j'avais de l'expérience, je postulerais'.""",

"""Discutez de l'environnement et de l'écologie en français.

Problèmes environnementaux : le changement climatique (climate change), le réchauffement climatique (global warming), la pollution de l'air (air pollution), la déforestation, les déchets plastiques (plastic waste), la disparition des espèces (species extinction).

Solutions : le tri sélectif (recycling/sorting waste), les énergies renouvelables (renewable energy — solaire, éolienne, hydraulique), les transports en commun, l'agriculture biologique (organic farming), la réduction du plastique. 'En France, il y a des poubelles de différentes couleurs pour le tri'.

La France et l'écologie : 'L'Accord de Paris sur le climat a été signé en 2015'. 'La France produit 70% de son électricité grâce au nucléaire'. 'Les Vélib' à Paris encouragent l'utilisation du vélo'. 'Le bonus écologique aide à acheter des voitures électriques'.

Le gérondif : en + participe présent (en -ant). 'En recyclant, on protège la planète' (By recycling, we protect the planet). 'En utilisant les transports en commun, on réduit la pollution'. 'Tout en reconnaissant le problème, le gouvernement n'agit pas assez vite'.

Exprimer la cause et la conséquence : Cause — parce que, car, puisque, grâce à, à cause de. Conséquence — donc, c'est pourquoi, par conséquent, si bien que. 'La température augmente à cause des émissions de CO2'. 'Il faut agir maintenant, c'est pourquoi nous manifestons'.""",

"""Explorez la culture et les médias dans le monde francophone.

Le cinéma français : la Nouvelle Vague (années 1960) — François Truffaut ('Les 400 Coups'), Jean-Luc Godard ('À bout de souffle'). Le Festival de Cannes est le plus prestigieux festival de cinéma au monde. La Palme d'Or. Films célèbres : 'Amélie' (2001), 'Intouchables' (2011), 'La Haine' (1995).

La littérature : Victor Hugo ('Les Misérables', 'Notre-Dame de Paris'), Albert Camus ('L'Étranger', 'La Peste'), Simone de Beauvoir ('Le Deuxième Sexe'). 'Le Petit Prince de Saint-Exupéry est le livre français le plus traduit au monde'.

La musique : Édith Piaf ('La Vie en rose'), Charles Aznavour, Jacques Brel (Belgique), Stromae (Belgique — 'Papaoutai', 'Alors on danse'), Zaz ('Je veux'). Le rap français : MC Solaar, IAM, Booba. 'La Fête de la Musique a lieu le 21 juin chaque année'.

Les médias : France 2, TF1 (télévision), Le Monde, Le Figaro, Libération (journaux). TV5Monde (chaîne francophone internationale). 'Les Français regardent en moyenne 3 heures de télévision par jour'.

La mise en relief : 'C'est... qui/que' — 'C'est le cinéma français qui m'intéresse le plus' (It's French cinema that interests me the most). 'Ce qui me plaît, c'est...' (What pleases me is...). 'Ce que j'aime, c'est...' (What I like is...).""",

"""Apprenez à exprimer vos sentiments et à parler des relations.

Les émotions : la joie (joy), la tristesse (sadness), la colère (anger), la peur (fear), la surprise, la déception (disappointment), la fierté (pride), la jalousie (jealousy), l'amour (love), la honte (shame).

Les relations : l'amitié (friendship), l'amour (love), le couple, la rupture (breakup), le mariage, le divorce. 'Ils sortent ensemble depuis deux ans' (They've been dating for two years). 'Ils se sont séparés' (They broke up). 'Ils se sont mariés l'été dernier'.

Exprimer des émotions : 'Je suis content(e) que tu sois là' (I'm happy you're here — subjonctif). 'Je suis triste qu'elle parte' (I'm sad she's leaving). 'Ça me rend furieux/furieuse' (That makes me furious). 'J'en ai marre !' (I'm fed up!).

Les pronoms COI : me, te, lui, nous, vous, leur. 'Je lui ai téléphoné' (I called him/her). 'Elle leur a écrit' (She wrote to them). 'Tu me manques' (I miss you — littéralement 'You are missing to me'). Double pronom : 'Je le lui ai dit' (I told it to him/her).

Hypothèse au présent : 'Si + présent, futur simple'. 'Si tu m'appelles, je viendrai' (If you call me, I'll come). 'Si on se dispute, on doit parler calmement'. Futur simple : je parlerai, tu parleras, il parlera... Irréguliers : serai (être), aurai (avoir), irai (aller), ferai (faire).""",

"""Apprenez à parler de vos projets et de l'avenir.

Exprimer des projets : 'Je vais déménager à Paris' (I'm going to move to Paris — futur proche). 'L'année prochaine, je voyagerai en Asie' (Next year, I'll travel to Asia — futur simple). 'J'ai l'intention de créer mon entreprise' (I intend to start my business). 'J'envisage de reprendre mes études' (I'm considering going back to school).

Le futur simple : Verbes réguliers : infinitif + -ai, -as, -a, -ons, -ez, -ont. 'Je travaillerai', 'Tu étudieras', 'Il voyagera'. Irréguliers : être → serai, avoir → aurai, aller → irai, faire → ferai, pouvoir → pourrai, vouloir → voudrai, devoir → devrai, venir → viendrai, voir → verrai, savoir → saurai.

Projets de vie : 'Je voudrais me marier et avoir des enfants' (I'd like to get married and have children). 'Mon rêve est de vivre à l'étranger' (My dream is to live abroad). 'J'espère trouver un travail qui me passionne' (I hope to find a job I'm passionate about).

Le conditionnel pour les hypothèses : 'Si j'avais plus d'argent, je ferais le tour du monde' (If I had more money, I'd travel the world). 'Si je pouvais, j'habiterais au bord de la mer' (If I could, I'd live by the sea). Si + imparfait → conditionnel présent.

Connecteurs temporels : dans (in — 'dans deux ans'), d'ici (by — 'd'ici 2030'), à partir de (starting from), dès que (as soon as — 'Dès que j'aurai mon diplôme, je chercherai un emploi')."""
],
"B2": [
"""Explorez les grandes œuvres de la littérature française.

Les classiques : Molière (17e siècle) — 'Le Malade imaginaire', 'Le Misanthrope', 'Tartuffe'. Maître de la comédie, il critiquait l'hypocrisie de la société. Voltaire (18e) — 'Candide' — satire philosophique. 'Il faut cultiver notre jardin'. Rousseau — 'Du Contrat social' : 'L'homme est né libre, et partout il est dans les fers'.

Le 19e siècle : Victor Hugo — 'Les Misérables' (Jean Valjean, justice sociale). Gustave Flaubert — 'Madame Bovary' (le réalisme, le 'bovarysme' — l'insatisfaction romantique). Émile Zola — 'Germinal' (la condition ouvrière), 'J'accuse' (l'affaire Dreyfus). Baudelaire — 'Les Fleurs du mal' (poésie moderne).

Le 20e siècle : Marcel Proust — 'À la recherche du temps perdu' (7 volumes, la mémoire). Albert Camus — 'L'Étranger' (l'absurde : 'Aujourd'hui, maman est morte'). Sartre — 'La Nausée' (existentialisme). Simone de Beauvoir — 'Le Deuxième Sexe' ('On ne naît pas femme, on le devient').

Analyse littéraire : le narrateur (narrator), le personnage (character), l'intrigue (plot), le cadre (setting), le thème (theme). 'Le roman est écrit à la première personne'. 'L'auteur utilise l'ironie pour critiquer la société'.

Discours indirect au passé : 'Il a dit qu'il avait lu le livre' (He said he had read the book). 'Elle a demandé si j'aimais la littérature'. Concordance des temps : présent → imparfait, passé composé → plus-que-parfait, futur → conditionnel.""",

"""Analysez les enjeux de société et l'actualité en France.

La politique française : le Président de la République (élu pour 5 ans), le Premier ministre, l'Assemblée nationale (577 députés), le Sénat (348 sénateurs). 'La Ve République a été fondée par le Général de Gaulle en 1958'. Les partis : LR (droite), PS (gauche), LREM/Renaissance (centre), RN (extrême droite), LFI (gauche radicale).

Enjeux sociaux : les banlieues (suburbs — souvent associées aux inégalités sociales), l'immigration, l'intégration, le chômage des jeunes, la réforme des retraites. 'Les gilets jaunes (2018-2019) ont protesté contre l'augmentation du prix du carburant et les inégalités sociales'.

Laïcité : 'La loi de 1905 sépare l'Église et l'État'. 'Le port de signes religieux ostensibles est interdit dans les écoles publiques depuis 2004'. 'La laïcité est un sujet de débat permanent en France'.

Argumentation structurée : Thèse → Antithèse → Synthèse. 'D'une part... d'autre part...' (On one hand... on the other). 'Force est de constater que...' (One must acknowledge that). 'Il n'en demeure pas moins que...' (It remains nonetheless that).

Le passif : 'La loi a été votée par l'Assemblée' (The law was voted by the Assembly). 'Les droits sont garantis par la Constitution'. Formation : être + participe passé. 'Le vin est produit en Bourgogne'.""",

"""Explorez l'art français et le monde de l'esthétique.

L'Impressionnisme : Claude Monet ('Impression, soleil levant' — qui a donné son nom au mouvement, 'Les Nymphéas'), Pierre-Auguste Renoir ('Le Déjeuner des canotiers'), Edgar Degas (les danseuses). 'Les impressionnistes peignaient en plein air pour capturer la lumière naturelle'.

Le Post-impressionnisme : Paul Cézanne ('La Montagne Sainte-Victoire'), Paul Gauguin (Tahiti), Vincent van Gogh (Néerlandais vivant en France — 'La Nuit étoilée'). 'Cézanne est considéré comme le père de l'art moderne'.

L'art moderne : Henri Matisse (fauvisme — couleurs vives), Marcel Duchamp ('Fontaine' — readymade, art conceptuel), Le Corbusier (architecture moderne). Le Centre Pompidou (Paris) abrite la plus grande collection d'art moderne en Europe.

Les musées : le Louvre (le plus grand musée du monde — la Joconde, la Vénus de Milo), le Musée d'Orsay (impressionnisme), le Centre Pompidou (art moderne). 'Le Louvre accueille environ 10 millions de visiteurs par an'.

La nominalisation : 'La beauté de cette œuvre est frappante' (au lieu de 'Cette œuvre est belle'). 'L'utilisation de la couleur montre...' 'La représentation de la nature'. Participe présent vs. adjectif verbal : 'fatigant' (verb) vs. 'fatigant' (adj — same!), mais 'provoquant' (verb) vs. 'provocant' (adj).""",

"""Discutez des avancées scientifiques et de l'innovation.

La science française : Marie Curie (deux prix Nobel — physique et chimie, découverte du radium et du polonium). Louis Pasteur (pasteurisation, vaccin contre la rage). 'L'Institut Pasteur est un centre de recherche de renommée mondiale'.

Innovation : Ariane (fusée européenne lancée depuis la Guyane française), Airbus (avionneur européen basé à Toulouse), le TGV (train à grande vitesse — jusqu'à 320 km/h). 'La France est à la pointe de la technologie nucléaire'.

Vocabulaire scientifique : l'hypothèse (hypothesis), l'expérience (experiment), la découverte (discovery), la recherche (research), le résultat (result), la preuve (proof). 'Cette étude démontre que...' 'Les résultats confirment l'hypothèse'.

Exprimer la certitude et le doute : Certitude — 'Il est certain que...' (+ indicatif), 'Il est évident que...'. Doute — 'Il est possible que...' (+ subjonctif), 'Il se peut que...', 'Je doute que...'. 'Il est probable que la technologie continuera à évoluer'. 'Il n'est pas certain que cette découverte soit applicable'.

La voix passive et les tournures impersonnelles : 'Il a été démontré que...' (It has been demonstrated that). 'On constate que...' (We observe that). 'Il convient de noter que...' (It should be noted that).""",

"""Explorez le système politique et les institutions françaises.

Les institutions : le Président (chef de l'État et des armées), le Premier ministre (chef du gouvernement), le Conseil constitutionnel (9 membres, contrôle la constitutionnalité des lois), le Conseil d'État (juridiction administrative suprême).

Les élections : 'L'élection présidentielle a lieu tous les cinq ans, au suffrage universel direct'. 'Les élections législatives suivent l'élection présidentielle'. La proportionnelle vs. le scrutin majoritaire. 'Le vote est un droit et un devoir civique'.

L'Union européenne : 'La France est un membre fondateur de l'UE'. 'Strasbourg accueille le Parlement européen'. 'L'espace Schengen permet la libre circulation'. 'L'euro est la monnaie commune depuis 2002'. 'Le couple franco-allemand est le moteur de l'intégration européenne'.

La francophonie : 'Le français est parlé par 321 millions de personnes dans le monde'. L'OIF (Organisation internationale de la Francophonie) compte 88 États membres. 'Le français est la langue officielle de 29 pays'. Afrique francophone : Sénégal, Côte d'Ivoire, RDC, Madagascar, Cameroun.

Concession : 'Bien que la France soit une démocratie solide, des défis persistent' (+ subjonctif). 'Malgré les critiques, le système perdure'. 'Certes... mais...' 'Quoique...'. Subjonctif passé : 'Bien qu'il ait voté, il n'est pas satisfait du résultat'.""",

"""Découvrez la francophonie et les échanges interculturels.

La diversité francophone : Le français en Afrique (Sénégal, Cameroun, RDC — le pays francophone le plus peuplé), au Canada (Québec — 'icitte' = ici, 'char' = voiture, 'blonde' = petite amie), en Belgique (septante, nonante), en Suisse (huitante, souper = dîner).

Expressions francophones : Québécois — 'C'est correct' (c'est OK), 'Bienvenue' (de rien). Africain — 'Je suis fatigué un peu' (je suis un peu fatigué), 'On dit quoi ?' (comment ça va ?). Belge — 'Ça va ou bien ?' (ça va ?). 'Chaque variété du français a sa richesse'.

Cuisine francophone : couscous (Maghreb), poulet yassa (Sénégal), poutine (Québec — frites, fromage, sauce brune), gaufres et moules-frites (Belgique), fondue (Suisse). 'La cuisine francophone reflète la diversité culturelle du monde francophone'.

L'interculturalité : 'Voyager, c'est apprendre à voir le monde avec d'autres yeux'. 'Les malentendus culturels viennent souvent de ce qu'on pense être universel'. 'L'ouverture d'esprit est la clé de la communication interculturelle'.

L'expression de l'opposition : 'Alors que la France métropolitaine..., les DOM-TOM...' (Whereas). 'Tandis que le Québec utilise beaucoup d'anglicismes, la France les évite'. 'Contrairement à ce qu'on croit...' (Contrary to what people think). 'En revanche...' (On the other hand)."""
],
"C1": [
"""Développez vos compétences en français académique et universitaire.

L'écriture académique : objectivité et rigueur. Éviter le 'je' : 'On peut observer que...' au lieu de 'J'observe que...'. 'Il apparaît que...' 'Force est de constater que...'. 'La présente étude vise à analyser...' (This study aims to analyze...).

Structure d'une dissertation : Introduction (amorce, problématique, annonce du plan), Développement (thèse, antithèse, synthèse), Conclusion (bilan, ouverture). 'Dans un premier temps, nous examinerons... Puis, nous analyserons... Enfin, nous proposerons...'

Citer et référencer : Citation directe : 'Selon Bourdieu (1979), "le goût est un marqueur social"'. Citation indirecte : 'Bourdieu soutient que le goût constitue un marqueur social'. 'Op. cit.', 'Ibid.', 'Cf.', 'passim'.

Connecteurs logiques avancés : 'En l'occurrence...' (in this case), 'En l'espèce...' (in this particular case), 'Eu égard à...' (with regard to), 'Nonobstant...' (notwithstanding), 'Qui plus est...' (what's more), 'Somme toute...' (all in all).

Subjonctif après certaines conjonctions : 'Afin que vous compreniez...' (So that you understand), 'Avant que le cours ne commence...' (Before the class starts), 'Pourvu que les résultats soient significatifs...' (Provided the results are significant). Le 'ne' explétif après 'avant que', 'à moins que'.""",

"""Analysez les grandes œuvres littéraires avec un regard critique.

La critique littéraire : structuralisme (Roland Barthes — 'La mort de l'auteur'), psychanalyse (appliquer Freud/Lacan aux textes), marxisme (lire le texte comme reflet des rapports de classe), féminisme (remettre en question la représentation des femmes).

Barthes : 'La mort de l'auteur' (1967) — le sens d'un texte ne dépend pas de l'intention de l'auteur mais de l'interprétation du lecteur. 'Un texte est un tissu de citations'. 'Le lecteur est le lieu où la multiplicité du texte se rassemble'.

Proust : 'La madeleine de Proust' — la mémoire involontaire déclenchée par les sens. 'Longtemps, je me suis couché de bonne heure'. 'À la recherche du temps perdu' explore le temps, la mémoire, l'art et l'amour à travers plus de 3000 pages.

Camus et l'absurde : 'L'Étranger' — Meursault, un homme indifférent, tue un Arabe sur une plage. 'Le Mythe de Sisyphe' : 'Il faut imaginer Sisyphe heureux'. L'homme face à un monde sans sens doit créer son propre sens.

Antériorité et postériorité : 'Après avoir lu le texte, on peut affirmer que...' 'Avant d'analyser le style, il convient d'examiner le contexte'. Participe passé composé : 'Ayant terminé son œuvre, l'auteur s'est retiré'.""",

"""Débattez des grands enjeux contemporains du monde francophone.

L'immigration : 'La France est un pays d'immigration depuis le 19e siècle'. 'Les vagues migratoires ont contribué à la diversité culturelle'. 'Le débat sur l'identité nationale est récurrent'. 'L'intégration des immigrants reste un défi majeur'.

Inégalités : 'Les écarts de richesse se creusent'. 'La précarité touche de plus en plus de jeunes'. 'L'ascenseur social est en panne' (Social mobility is broken). 'Les discriminations à l'embauche persistent malgré les lois'.

Numérique et société : 'Les réseaux sociaux ont transformé le débat public'. 'La désinformation menace la démocratie'. 'Le droit à la déconnexion a été inscrit dans la loi française en 2017'. 'L'intelligence artificielle soulève des questions éthiques majeures'.

Transition écologique : 'La sobriété énergétique devient une nécessité'. 'Comment concilier croissance économique et protection de l'environnement ?'. 'Les accords de Paris engagent les pays à limiter le réchauffement à 1,5°C'.

Tournures concessives avancées : 'Tout en reconnaissant les progrès accomplis, il convient de souligner les lacunes persistantes'. 'Si légitime que soit cette revendication, elle se heurte à des obstacles pratiques'. 'Pour peu que les conditions soient réunies...' (Provided that).""",

"""Explorez la philosophie française et ses grands penseurs.

René Descartes (1596-1650) : 'Je pense, donc je suis' (Cogito ergo sum). Le doute méthodique : remettre tout en question pour trouver une vérité indubitable. 'Le Discours de la méthode' — fondation de la philosophie moderne.

Jean-Jacques Rousseau (1712-1778) : 'L'homme est naturellement bon, c'est la société qui le corrompt'. 'Du Contrat social' : la souveraineté populaire, la volonté générale. Il a influencé la Révolution française et les droits de l'homme.

L'existentialisme : Jean-Paul Sartre — 'L'existence précède l'essence'. L'homme est condamné à être libre. 'L'Être et le Néant'. Simone de Beauvoir — 'On ne naît pas femme, on le devient'. Albert Camus — l'absurde et la révolte.

Michel Foucault (1926-1984) : le pouvoir est partout, dans les institutions (prison, hôpital, école). 'Surveiller et punir' — le panoptique comme métaphore du contrôle social. 'Le savoir est pouvoir'.

Style philosophique : 'Il s'ensuit que...' (It follows that), 'En dernière analyse...' (In the final analysis), 'Tout bien considéré...' (All things considered). Subjonctif imparfait (littéraire) : 'Il fallait qu'il comprît' (il comprenne). 'Quoiqu'il en fût' (quoiqu'il en soit).""",

"""Perfectionnez votre production écrite avec des textes complexes.

Types de textes avancés : la dissertation (essay — structure française classique), l'essai argumentatif, le commentaire composé (literary analysis), le compte-rendu critique (critical review), la synthèse de documents (document synthesis — épreuve du DALF).

La synthèse : 'Il s'agit de confronter plusieurs documents pour en dégager les idées principales'. Règles : ne jamais donner son opinion personnelle, reformuler (ne pas citer), organiser thématiquement et non document par document.

Transitions élaborées : 'Si l'on se place dans une perspective différente...' (If we take a different perspective). 'Il reste à déterminer dans quelle mesure...' (It remains to determine to what extent). 'Cela nous amène à nous interroger sur...' (This leads us to question).

Cohérence textuelle : anaphore ('ce phénomène', 'ladite mesure'), cataphore (annonce : 'Voici le problème :'), connecteurs de reformulation ('autrement dit', 'en d'autres termes', 'c'est-à-dire').

Registres : soutenu (littéraire — 'certes', 'en effet', 'toutefois'), courant (standard), familier ('vachement', 'boulot', 'fringues'). 'La maîtrise des registres est essentielle pour adapter son discours au contexte communicatif'.""",

"""Préparez-vous au DALF C1 avec des stratégies d'examen et de communication.

Le DALF C1 : Compréhension orale (40 min), Compréhension écrite (50 min), Production écrite (2h30 — synthèse + essai argumenté), Production orale (30 min de préparation + 20 min de passation).

Synthèse de documents : 'Identifier les thèmes communs aux documents'. 'Reformuler sans reprendre les mots du texte'. 'Organiser par thèmes, pas par documents'. 'Ne jamais donner son opinion'. 220 mots minimum.

Essai argumenté : 'Prendre position sur le thème abordé dans les documents'. 'Structurer en introduction, développement (2-3 parties), conclusion'. 'Utiliser des exemples concrets'. 250 mots minimum.

Production orale : Présentation d'un point de vue à partir d'un document déclencheur, suivie d'un débat avec le jury. 'Dans un premier temps, je vais présenter...' 'En conclusion, je dirai que...'. Défendre son point de vue : 'Je maintiens que...', 'Permettez-moi de nuancer...'.

Expressions pour le débat : 'Vous soulevez un point intéressant, cependant...' (You raise an interesting point, however...). 'Je ne suis pas entièrement de cet avis' (I don't entirely share this view). 'C'est une question qui mérite réflexion' (That's a question worth reflecting on)."""
],
"C2": [
"""Développez votre pensée critique et explorez l'épistémologie en français.

L'épistémologie : étude de la connaissance — comment savons-nous ce que nous savons ? Gaston Bachelard : 'La connaissance se construit contre l'opinion'. L'obstacle épistémologique — nos préjugés empêchent la connaissance scientifique. 'La science ne progresse que par la rectification des erreurs'.

Karl Popper (influence majeure en France) : la falsifiabilité — une théorie scientifique doit pouvoir être réfutée. 'Mille confirmations ne prouvent pas une théorie, mais une seule réfutation suffit à l'invalider'. Thomas Kuhn : les paradigmes scientifiques et les révolutions.

La pensée critique : distinguer fait et opinion, identifier les biais cognitifs (biais de confirmation, effet de halo, sophismes), évaluer la fiabilité des sources. 'Tout argument d'autorité doit être examiné avec scepticisme'.

Edgar Morin : la pensée complexe — 'Il faut relier ce qui est séparé'. Contre la pensée réductrice et disciplinaire. 'La connaissance pertinente est celle qui est capable de situer toute information dans son contexte'.

Constructions intellectuelles : 'En tant que construct social, le concept de...' 'Il convient de déconstruire la notion de...' 'À l'aune de (in light of) ces considérations, il apparaît que...' 'Loin de constituer une évidence, cette idée relève d'un présupposé contestable'.""",

"""Explorez la richesse de la littérature francophone mondiale.

Littérature africaine : Léopold Sédar Senghor (Sénégal, Négritude — 'L'émotion est nègre, la raison est hellène'), Aimé Césaire (Martinique — 'Cahier d'un retour au pays natal'), Frantz Fanon ('Les Damnés de la terre' — décolonisation et identité).

Littérature maghrébine : Tahar Ben Jelloun (Maroc — 'L'Enfant de sable'), Assia Djebar (Algérie — 'L'Amour, la fantasia'), Kateb Yacine ('Nedjma'). 'La littérature maghrébine francophone explore la double identité et le rapport à l'ancien colonisateur'.

Littérature québécoise : Michel Tremblay ('Les Belles-Sœurs' — écrit en joual, le français populaire québécois), Gabrielle Roy ('Bonheur d'occasion'). 'La littérature québécoise affirme une identité distincte face à l'anglophonie'.

Littérature caribéenne : Patrick Chamoiseau (Martinique — 'Texaco', Prix Goncourt 1992), Maryse Condé (Guadeloupe — 'Moi, Tituba sorcière'). La créolité — 'Ni Européens, ni Africains, ni Asiatiques, nous nous proclamons Créoles'.

Intertextualité et postcolonialisme : 'L'écriture postcoloniale s'inscrit dans un rapport dialogique avec le canon occidental'. 'L'hybridité culturelle se manifeste dans le métissage linguistique'. Subjonctif imparfait : 'Il eût fallu que la littérature franchît les frontières'.""",

"""Approfondissez vos connaissances en linguistique et en sémiologie.

Ferdinand de Saussure (1857-1913) : père de la linguistique moderne. Le signe linguistique = signifiant (forme sonore) + signifié (concept). 'Le rapport entre le signifiant et le signifié est arbitraire'. Langue (système) vs. parole (usage individuel). Synchronie vs. diachronie.

Roland Barthes : sémiologie — l'étude des signes dans la société. 'Mythologies' (1957) — analyse de la culture populaire (catch, publicité, steak-frites). 'Le mythe est un système de communication'. 'Le degré zéro de l'écriture' — existe-t-il une écriture neutre ?

Pragmatique : les actes de langage (Austin, Searle). Acte locutoire (ce qui est dit), illocutoire (l'intention), perlocutoire (l'effet). 'Il fait froid ici' peut être un constat, une demande de fermer la fenêtre, ou un reproche.

Sociolinguistique : Pierre Bourdieu — le 'marché linguistique', le capital linguistique. 'La langue légitime est celle de la classe dominante'. 'L'accent, le vocabulaire et la syntaxe sont des marqueurs sociaux'.

Néologie et évolution : 'Le français évolue constamment'. Anglicismes (start-up, deadline, feedback), verlan (meuf = femme, keuf = flic, relou = lourd), langage SMS (slt = salut, bcp = beaucoup, mdr = mort de rire). 'L'Académie française veille sur la langue, mais la langue appartient à ceux qui la parlent'.""",

"""Maîtrisez le français juridique et les relations internationales.

Le droit français : le Code civil (Code Napoléon, 1804 — modèle pour de nombreux pays), le Code pénal, le droit administratif. 'Nul n'est censé ignorer la loi' (Ignorance of the law is no excuse). 'Le droit français est un système de droit civil (codifié), par opposition au common law anglo-saxon'.

Institutions internationales : l'ONU (siège à New York, la France est membre permanent du Conseil de sécurité), la Cour internationale de Justice (La Haye), la Cour pénale internationale. 'La Déclaration universelle des droits de l'homme a été rédigée en 1948'.

Droit européen : 'Le droit communautaire prime sur le droit national'. La CEDH (Cour européenne des droits de l'homme, Strasbourg). 'Tout citoyen européen peut saisir la CEDH'.

Vocabulaire juridique : le plaignant (plaintiff), le prévenu (defendant), l'acquittement (acquittal), la condamnation (conviction), le pourvoi en cassation (appeal to supreme court), la jurisprudence (case law). 'Attendu que... Par ces motifs... Le tribunal condamne...'.

Style juridique : 'Il est porté à la connaissance de l'intéressé que...' (The interested party is hereby informed that). 'En vertu de l'article 1240 du Code civil...' (By virtue of Article 1240). 'Vu les pièces du dossier...' (Having examined the case files). Phrases longues avec subordonnées enchaînées.""",

"""Explorez l'esthétique et la création artistique dans la pensée française.

L'art pour l'art : Théophile Gautier (19e siècle) — 'L'art n'a pas d'utilité, sa beauté se suffit à elle-même'. Baudelaire : la beauté du mal, le spleen, la modernité. 'Le beau est toujours bizarre'. Marcel Duchamp : 'C'est le regardeur qui fait le tableau' — l'art conceptuel.

L'esthétique philosophique : Kant — le jugement de goût est subjectif mais prétend à l'universalité. Hegel — l'art comme manifestation sensible de l'Idée. 'L'art est-il mort ?' (Hegel pensait que la philosophie remplacerait l'art).

L'art contemporain français : Daniel Buren (les colonnes de Buren au Palais-Royal), Sophie Calle (art et autobiographie), JR (photographie urbaine, collages monumentaux). 'L'art contemporain interroge les limites de ce qui peut être considéré comme art'.

La mode comme art : Coco Chanel ('La mode se démode, le style jamais'), Christian Dior (le New Look), Yves Saint-Laurent (le smoking pour femmes). 'Paris reste la capitale mondiale de la haute couture'. 'La mode est un langage visuel qui exprime une identité'.

Registre soutenu littéraire : 'Il n'est pas sans intérêt de noter que...' (It is not without interest to note that). 'À bien des égards...' (In many respects). 'De prime abord...' (At first glance). 'En fin de compte...' (In the final analysis).""",

"""Atteignez la maîtrise totale de la langue française : style, humour et sophistication.

La maîtrise linguistique : au niveau C2, vous comprenez sans effort tout ce que vous lisez ou entendez. Vous pouvez restituer faits et arguments de sources diverses, en les résumant de façon cohérente. Vous vous exprimez spontanément, avec fluidité et précision.

Expressions idiomatiques : 'Avoir le cafard' (to feel down/blue). 'Poser un lapin' (to stand someone up). 'Mettre son grain de sel' (to put one's two cents in). 'Avoir la moutarde qui monte au nez' (to be getting angry). 'Couper la poire en deux' (to split the difference). 'Donner sa langue au chat' (to give up guessing).

L'humour français : l'ironie est la marque du français cultivé. 'Les Français adorent les jeux de mots' — 'Les poissons sont bien élevés : ils vivent dans des bancs' (banc = bench / school of fish). 'Un homme entre dans un café... plouf !' (café = café / coffee).

Les registres de la perfection : Littéraire — 'Il eût été souhaitable que nous parvînssions à un accord' (subjonctif imparfait). Diplomatique — 'Veuillez agréer, Monsieur l'Ambassadeur, l'expression de ma très haute considération'. Familier — 'J'en ai ras le bol de ce boulot, je me casse !'

Proverbes : 'L'habit ne fait pas le moine' (Don't judge a book by its cover). 'Pierre qui roule n'amasse pas mousse' (A rolling stone gathers no moss). 'Qui vivra verra' (Time will tell). 'Mieux vaut tard que jamais' (Better late than never). 'Petit à petit, l'oiseau fait son nid' (Little by little, the bird builds its nest)."""
]
}

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = 0
    for level, contents in FR_RICH.items():
        course = await db.courses.find_one({"language": "french", "level": level})
        if not course: continue
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for i, content in enumerate(contents):
            if i < len(lessons):
                await db.lessons.update_one({"_id": lessons[i]["_id"]}, {"$set": {"content": content}})
                total += 1
        print(f"Enriched french-{level}: {min(len(contents), len(lessons))} lessons")
    print(f"\nTotal: {total}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
