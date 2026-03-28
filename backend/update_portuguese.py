"""Update Portuguese lessons to align with Novo Avenida Brasil textbook series."""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

# Novo Avenida Brasil 1 (A1), 2 (A2), 3 (B1), + advanced levels
PORTUGUESE_CONTENT = {
    "A1": [
        {
            "title": "Conteúdo 1: Encontros e Apresentações",
            "content": "Baseado no Novo Avenida Brasil 1 - Unidade 1. Nesta lição, você aprenderá a se apresentar, cumprimentar pessoas e trocar informações pessoais básicas em português brasileiro. Os diálogos incluem situações do dia a dia como encontros em festas, no trabalho e na rua. Expressões como 'Oi, tudo bem?', 'Como vai?' e 'Prazer em conhecê-lo' são fundamentais para a comunicação básica. No Brasil, é comum cumprimentar com um beijo no rosto ou um aperto de mão.",
            "vocabulary": [
                {"word": "Oi", "translation": "Hi", "example": "Oi, tudo bem?"},
                {"word": "Prazer", "translation": "Nice to meet you", "example": "Prazer em conhecê-lo."},
                {"word": "Como vai?", "translation": "How are you?", "example": "Como vai? Eu estou bem, obrigado."},
                {"word": "Obrigado/a", "translation": "Thank you", "example": "Muito obrigado pela ajuda."},
                {"word": "De nada", "translation": "You're welcome", "example": "De nada, foi um prazer."},
                {"word": "Tchau", "translation": "Bye", "example": "Tchau, até amanhã!"}
            ],
            "grammar_points": [
                "Verbo SER no presente: eu sou, você é, ele/ela é, nós somos, vocês são, eles/elas são",
                "Pronomes pessoais: eu, você, ele/ela, nós, vocês, eles/elas",
                "Cumprimentos formais vs. informais: 'Como vai o senhor?' (formal) vs. 'E aí, beleza?' (informal)"
            ]
        },
        {
            "title": "Conteúdo 2: Nacionalidade e Profissões",
            "content": "Novo Avenida Brasil 1 - Unidade 2. Aprenda a falar sobre sua nacionalidade, país de origem e profissão. No Brasil, perguntar 'De onde você é?' é muito comum. Também vamos aprender os artigos definidos e indefinidos, fundamentais para a estrutura das frases em português. As profissões têm formas masculinas e femininas: professor/professora, médico/médica.",
            "vocabulary": [
                {"word": "País", "translation": "Country", "example": "De que país você é?"},
                {"word": "Profissão", "translation": "Profession", "example": "Qual é a sua profissão?"},
                {"word": "Professor/a", "translation": "Teacher", "example": "Ela é professora de português."},
                {"word": "Médico/a", "translation": "Doctor", "example": "Meu irmão é médico."},
                {"word": "Estrangeiro/a", "translation": "Foreigner", "example": "Sou estrangeiro, vim dos Estados Unidos."},
                {"word": "Trabalhar", "translation": "To work", "example": "Eu trabalho em um escritório."}
            ],
            "grammar_points": [
                "Artigos definidos: o (masc.), a (fem.), os (masc. pl.), as (fem. pl.)",
                "Artigos indefinidos: um (masc.), uma (fem.), uns (masc. pl.), umas (fem. pl.)",
                "Gênero das profissões: engenheiro/engenheira, advogado/advogada, cantor/cantora"
            ]
        },
        {
            "title": "Conteúdo 3: No Hotel e Reservas",
            "content": "Novo Avenida Brasil 1 - Unidade 3. Situações práticas em hotéis: fazer reservas, pedir informações sobre quartos, preços e serviços. Vocabulário essencial para viajantes no Brasil. Os números são fundamentais: 1-100 e valores em reais (R$). Também aprenderemos a usar o verbo TER (ter) para expressar posse e existência.",
            "vocabulary": [
                {"word": "Quarto", "translation": "Room", "example": "Eu gostaria de reservar um quarto."},
                {"word": "Diária", "translation": "Daily rate", "example": "Qual é o valor da diária?"},
                {"word": "Chave", "translation": "Key", "example": "Aqui está a chave do seu quarto."},
                {"word": "Reserva", "translation": "Reservation", "example": "Tenho uma reserva no nome de Silva."},
                {"word": "Café da manhã", "translation": "Breakfast", "example": "O café da manhã está incluído?"},
                {"word": "Conta", "translation": "Bill", "example": "Posso ver a conta, por favor?"}
            ],
            "grammar_points": [
                "Verbo TER: eu tenho, você tem, ele/ela tem, nós temos, vocês têm, eles/elas têm",
                "Números 1-100: um, dois, três... dez, vinte, trinta... cem",
                "Expressões de polidez: Eu gostaria de..., Por favor, Com licença"
            ]
        },
        {
            "title": "Conteúdo 4: Comidas e Bebidas",
            "content": "Novo Avenida Brasil 1 - Unidades 4-5. A culinária brasileira é rica e diversa. Nesta lição, aprenderemos a pedir comida em restaurantes, falar sobre preferências alimentares e usar o verbo QUERER. Pratos típicos como feijoada, pão de queijo e açaí fazem parte do vocabulário cultural. No Brasil, almoço é a refeição principal do dia.",
            "vocabulary": [
                {"word": "Feijoada", "translation": "Black bean stew", "example": "A feijoada é o prato nacional do Brasil."},
                {"word": "Almoço", "translation": "Lunch", "example": "Vamos almoçar? Estou com fome."},
                {"word": "Suco", "translation": "Juice", "example": "Eu quero um suco de laranja, por favor."},
                {"word": "Pão de queijo", "translation": "Cheese bread", "example": "O pão de queijo de Minas é delicioso."},
                {"word": "Cardápio", "translation": "Menu", "example": "Posso ver o cardápio?"},
                {"word": "Garçom", "translation": "Waiter", "example": "Garçom, a conta, por favor."}
            ],
            "grammar_points": [
                "Verbo QUERER: eu quero, você quer, ele/ela quer, nós queremos",
                "Verbo GOSTAR DE: Eu gosto de café. Você gosta de suco?",
                "Partitivos: um copo de água, uma xícara de café, um prato de arroz"
            ]
        },
        {
            "title": "Conteúdo 5: A Cidade e Transportes",
            "content": "Novo Avenida Brasil 1 - Unidades 6-7. Aprenda a se locomover nas cidades brasileiras. Vocabulário sobre meios de transporte (ônibus, metrô, táxi), direções e localização. Cidades como São Paulo, Rio de Janeiro e Salvador têm características únicas. Usaremos os verbos IR e ESTAR para indicar movimento e localização.",
            "vocabulary": [
                {"word": "Ônibus", "translation": "Bus", "example": "O ônibus para o centro sai às 8h."},
                {"word": "Metrô", "translation": "Subway", "example": "O metrô é o transporte mais rápido em São Paulo."},
                {"word": "Rua", "translation": "Street", "example": "A padaria fica nesta rua."},
                {"word": "Perto", "translation": "Near", "example": "O banco fica perto do hospital."},
                {"word": "Longe", "translation": "Far", "example": "A praia não é longe daqui."},
                {"word": "Esquina", "translation": "Corner", "example": "Vire na esquina à direita."}
            ],
            "grammar_points": [
                "Verbo IR: eu vou, você vai, ele/ela vai, nós vamos, vocês vão",
                "Preposições de lugar: em, no/na, perto de, longe de, ao lado de, em frente a",
                "Contrações: em + o = no, em + a = na, de + o = do, de + a = da"
            ]
        },
        {
            "title": "Conteúdo 6: Rotina Diária",
            "content": "Novo Avenida Brasil 1 - Unidades 8-9. Como é o dia a dia de um brasileiro? Aprenda a descrever sua rotina diária usando verbos reflexivos e expressões de tempo. No Brasil, os horários podem ser mais flexíveis: o almoço geralmente é entre 12h e 14h, e o jantar entre 19h e 21h. Verbos como acordar, tomar banho e dormir são essenciais.",
            "vocabulary": [
                {"word": "Acordar", "translation": "To wake up", "example": "Eu acordo às sete horas."},
                {"word": "Tomar banho", "translation": "To take a shower", "example": "No Brasil, as pessoas tomam banho todos os dias."},
                {"word": "Almoçar", "translation": "To have lunch", "example": "Nós almoçamos ao meio-dia."},
                {"word": "Dormir", "translation": "To sleep", "example": "Eu durmo às onze da noite."},
                {"word": "Trabalhar", "translation": "To work", "example": "Ela trabalha das 9h às 18h."},
                {"word": "Fim de semana", "translation": "Weekend", "example": "No fim de semana, eu vou à praia."}
            ],
            "grammar_points": [
                "Verbos reflexivos: levantar-se (eu me levanto), vestir-se (eu me visto)",
                "Horas: São oito horas. É meio-dia. É meia-noite. São três e meia.",
                "Expressões de frequência: sempre, geralmente, às vezes, nunca"
            ]
        }
    ],
    "A2": [
        {
            "title": "Conteúdo 1: Moradia e Descrição",
            "content": "Novo Avenida Brasil 2 - Unidade 1. Descreva sua casa, apartamento e bairro. Vocabulário sobre tipos de moradia, cômodos e mobília. No Brasil, muitas pessoas moram em apartamentos nas grandes cidades. Aprenda a usar adjetivos para descrever lugares e o pretérito perfeito para falar sobre mudanças.",
            "vocabulary": [
                {"word": "Apartamento", "translation": "Apartment", "example": "Meu apartamento tem dois quartos."},
                {"word": "Cozinha", "translation": "Kitchen", "example": "A cozinha é grande e bem iluminada."},
                {"word": "Banheiro", "translation": "Bathroom", "example": "O banheiro fica no final do corredor."},
                {"word": "Aluguel", "translation": "Rent", "example": "O aluguel é de dois mil reais por mês."},
                {"word": "Mudança", "translation": "Moving", "example": "Fizemos a mudança no sábado."},
                {"word": "Vizinho", "translation": "Neighbor", "example": "Meus vizinhos são muito simpáticos."}
            ],
            "grammar_points": [
                "Pretérito perfeito (regular): eu falei, você falou, ele/ela falou, nós falamos",
                "Adjetivos descritivos: grande/pequeno, bonito/feio, novo/velho, limpo/sujo",
                "Comparativos: mais... que, menos... que, tão... quanto"
            ]
        },
        {
            "title": "Conteúdo 2: Compras e Serviços",
            "content": "Novo Avenida Brasil 2 - Unidades 2-3. Situações de compras em lojas, supermercados e feiras. Aprenda a negociar preços (muito comum no Brasil!), pedir descontos e fazer reclamações educadamente. O verbo PODER é essencial para fazer pedidos educados.",
            "vocabulary": [
                {"word": "Desconto", "translation": "Discount", "example": "Tem desconto se pagar à vista?"},
                {"word": "Barato", "translation": "Cheap", "example": "Esta camisa está bem barata."},
                {"word": "Caro", "translation": "Expensive", "example": "O restaurante é caro demais."},
                {"word": "Promoção", "translation": "Sale/Promotion", "example": "As frutas estão em promoção hoje."},
                {"word": "Troco", "translation": "Change (money)", "example": "Você tem troco para cem reais?"},
                {"word": "Feira", "translation": "Street market", "example": "Aos domingos vou à feira comprar frutas."}
            ],
            "grammar_points": [
                "Verbo PODER: eu posso, você pode, ele/ela pode, nós podemos",
                "Pronomes demonstrativos: este/esta, esse/essa, aquele/aquela",
                "Pretérito perfeito (irregulares): fui, fiz, tive, estive, disse"
            ]
        },
        {
            "title": "Conteúdo 3: Saúde e Corpo",
            "content": "Novo Avenida Brasil 2 - Unidades 4-5. Aprenda vocabulário sobre partes do corpo, sintomas e como se comunicar em situações médicas. No Brasil, o SUS (Sistema Único de Saúde) oferece atendimento gratuito. Usar o imperativo para dar conselhos de saúde.",
            "vocabulary": [
                {"word": "Dor de cabeça", "translation": "Headache", "example": "Estou com dor de cabeça."},
                {"word": "Febre", "translation": "Fever", "example": "Acho que estou com febre."},
                {"word": "Remédio", "translation": "Medicine", "example": "Preciso tomar um remédio."},
                {"word": "Farmácia", "translation": "Pharmacy", "example": "Tem uma farmácia aqui perto?"},
                {"word": "Consulta", "translation": "Medical appointment", "example": "Marquei uma consulta para terça-feira."},
                {"word": "Receita", "translation": "Prescription", "example": "O médico passou uma receita."}
            ],
            "grammar_points": [
                "Imperativo: tome (tomar), beba (beber), descanse (descansar), vá (ir)",
                "Estar com + substantivo: estar com fome, estar com sede, estar com dor",
                "Pretérito imperfeito: eu era, eu tinha, eu fazia, eu ia (ações habituais no passado)"
            ]
        },
        {
            "title": "Conteúdo 4: Lazer e Cultura",
            "content": "Novo Avenida Brasil 2 - Unidades 6-7. O Brasil é famoso por sua cultura vibrante: música (samba, bossa nova, MPB), festas (Carnaval), esportes (futebol) e praias. Aprenda a falar sobre hobbies, convites e programas culturais. Use o futuro imediato para fazer planos.",
            "vocabulary": [
                {"word": "Carnaval", "translation": "Carnival", "example": "O Carnaval do Rio é o maior do mundo."},
                {"word": "Praia", "translation": "Beach", "example": "Vamos à praia no fim de semana?"},
                {"word": "Futebol", "translation": "Football/Soccer", "example": "O Brasil é o país do futebol."},
                {"word": "Samba", "translation": "Samba", "example": "Aprender a dançar samba é muito divertido."},
                {"word": "Cinema", "translation": "Cinema", "example": "Quer ir ao cinema hoje à noite?"},
                {"word": "Show", "translation": "Concert/Show", "example": "Vamos ao show de música ao vivo."}
            ],
            "grammar_points": [
                "Futuro imediato: IR + infinitivo (Eu vou viajar. Nós vamos dançar.)",
                "Convites: Quer ir...? Vamos...? Que tal...? Você topa...?",
                "Pretérito perfeito vs. imperfeito: Ontem eu fui à praia (ação) vs. Quando era criança, eu ia à praia (hábito)"
            ]
        },
        {
            "title": "Conteúdo 5: Viagens pelo Brasil",
            "content": "Novo Avenida Brasil 2 - Unidades 8-10. Explore as regiões do Brasil: Norte (Amazônia), Nordeste (praias e cultura), Sudeste (São Paulo, Rio), Sul (influência europeia) e Centro-Oeste (Brasília, Pantanal). Aprenda a planejar viagens, comprar passagens e descrever experiências passadas.",
            "vocabulary": [
                {"word": "Passagem", "translation": "Ticket", "example": "Comprei uma passagem de avião para Salvador."},
                {"word": "Mala", "translation": "Suitcase", "example": "Preciso fazer a mala para a viagem."},
                {"word": "Hospedagem", "translation": "Accommodation", "example": "A hospedagem inclui café da manhã."},
                {"word": "Paisagem", "translation": "Landscape", "example": "A paisagem da Amazônia é incrível."},
                {"word": "Roteiro", "translation": "Itinerary", "example": "Qual é o roteiro da viagem?"},
                {"word": "Souvenirs", "translation": "Souvenirs", "example": "Comprei lembranças para minha família."}
            ],
            "grammar_points": [
                "Pretérito perfeito composto: Eu tenho viajado muito. Nós temos estudado bastante.",
                "Conjunções: porque, mas, então, quando, enquanto, embora",
                "Discurso indireto: Ele disse que ia viajar. Ela perguntou se eu queria ir."
            ]
        },
        {
            "title": "Conteúdo 6: Comunicação e Tecnologia",
            "content": "Novo Avenida Brasil 2 - Unidades 11-12. O Brasil é um dos maiores mercados de redes sociais do mundo. Aprenda vocabulário sobre tecnologia, internet e comunicação digital. Também praticaremos como escrever e-mails, mensagens e comentários em português. WhatsApp é a principal ferramenta de comunicação no Brasil.",
            "vocabulary": [
                {"word": "Celular", "translation": "Cell phone", "example": "Me manda uma mensagem no celular."},
                {"word": "Internet", "translation": "Internet", "example": "A internet aqui é muito rápida."},
                {"word": "Mensagem", "translation": "Message", "example": "Recebi sua mensagem no WhatsApp."},
                {"word": "E-mail", "translation": "Email", "example": "Vou te enviar os detalhes por e-mail."},
                {"word": "Aplicativo", "translation": "App", "example": "Baixe o aplicativo no seu celular."},
                {"word": "Senha", "translation": "Password", "example": "Esqueci minha senha do Wi-Fi."}
            ],
            "grammar_points": [
                "Futuro do subjuntivo: Quando eu chegar, te ligo. Se você puder, me ajude.",
                "Pronomes oblíquos: me, te, lhe, nos (Me manda o link. Te envio depois.)",
                "Gerúndio: estou fazendo, estou mandando, estou trabalhando"
            ]
        }
    ],
    "B1": [
        {
            "title": "Conteúdo 1: Mercado de Trabalho",
            "content": "Novo Avenida Brasil 3 - Unidade 1. O mercado de trabalho brasileiro tem características únicas. Aprenda a falar sobre experiências profissionais, elaborar um currículo e participar de entrevistas de emprego em português. A CLT (Consolidação das Leis do Trabalho) rege as relações trabalhistas no Brasil.",
            "vocabulary": [
                {"word": "Currículo", "translation": "Resume/CV", "example": "Enviei meu currículo para três empresas."},
                {"word": "Entrevista", "translation": "Interview", "example": "A entrevista de emprego é amanhã."},
                {"word": "Salário", "translation": "Salary", "example": "O salário mínimo aumentou este ano."},
                {"word": "Experiência", "translation": "Experience", "example": "Tenho cinco anos de experiência na área."},
                {"word": "Contrato", "translation": "Contract", "example": "Assinei o contrato de trabalho."},
                {"word": "Férias", "translation": "Vacation", "example": "Tenho direito a 30 dias de férias."}
            ],
            "grammar_points": [
                "Subjuntivo presente: É importante que eu estude. Espero que você consiga o emprego.",
                "Conectores argumentativos: além disso, por outro lado, no entanto, portanto",
                "Voz passiva: O relatório foi entregue. Os candidatos serão entrevistados."
            ]
        },
        {
            "title": "Conteúdo 2: Educação Brasileira",
            "content": "Novo Avenida Brasil 3 - Unidades 2-3. O sistema educacional brasileiro: ensino fundamental, médio e superior. Universidades públicas e privadas, o ENEM e vestibulares. Discuta sobre educação e formação usando estruturas argumentativas.",
            "vocabulary": [
                {"word": "Faculdade", "translation": "College/University", "example": "Fiz faculdade de Administração."},
                {"word": "Vestibular", "translation": "University entrance exam", "example": "O vestibular é muito concorrido."},
                {"word": "Bolsa de estudos", "translation": "Scholarship", "example": "Ganhei uma bolsa de estudos parcial."},
                {"word": "Formatura", "translation": "Graduation", "example": "A formatura é em dezembro."},
                {"word": "Pesquisa", "translation": "Research", "example": "Estou fazendo uma pesquisa sobre cultura brasileira."},
                {"word": "Nota", "translation": "Grade", "example": "Preciso tirar nota boa na prova."}
            ],
            "grammar_points": [
                "Subjuntivo com expressões de dúvida: Talvez ele passe no vestibular. Duvido que seja fácil.",
                "Orações condicionais: Se eu estudar mais, vou passar. Se tivesse tempo, estudaria mais.",
                "Nominalização: educar → educação, formar → formação, pesquisar → pesquisa"
            ]
        },
        {
            "title": "Conteúdo 3: Meio Ambiente",
            "content": "Novo Avenida Brasil 3 - Unidades 4-5. O Brasil abriga a maior floresta tropical do mundo e uma biodiversidade única. Discuta problemas ambientais como desmatamento, poluição e sustentabilidade. Aprenda a expressar opiniões e fazer argumentações sobre temas ecológicos.",
            "vocabulary": [
                {"word": "Desmatamento", "translation": "Deforestation", "example": "O desmatamento na Amazônia é preocupante."},
                {"word": "Reciclagem", "translation": "Recycling", "example": "A reciclagem ajuda a preservar o meio ambiente."},
                {"word": "Sustentável", "translation": "Sustainable", "example": "Precisamos adotar práticas sustentáveis."},
                {"word": "Poluição", "translation": "Pollution", "example": "A poluição do ar é um problema nas grandes cidades."},
                {"word": "Biodiversidade", "translation": "Biodiversity", "example": "O Brasil tem uma enorme biodiversidade."},
                {"word": "Energia renovável", "translation": "Renewable energy", "example": "O Brasil investe em energia renovável."}
            ],
            "grammar_points": [
                "Expressões de opinião: Na minha opinião, Eu acho que, Acredito que, É evidente que",
                "Imperfeito do subjuntivo: Se todos reciclassem, o mundo seria melhor.",
                "Voz passiva com SE: Recicla-se papel. Preserva-se a natureza."
            ]
        },
        {
            "title": "Conteúdo 4: Mídia e Comunicação",
            "content": "Novo Avenida Brasil 3 - Unidades 6-8. A mídia brasileira: telenovelas, jornais, rádio e influência digital. As novelas da Globo são fenômenos culturais. Aprenda a discutir sobre meios de comunicação, fake news e o impacto das redes sociais na sociedade brasileira.",
            "vocabulary": [
                {"word": "Notícia", "translation": "News", "example": "Você viu a notícia sobre o novo presidente?"},
                {"word": "Novela", "translation": "Soap opera", "example": "As novelas brasileiras são famosas no mundo todo."},
                {"word": "Reportagem", "translation": "News report", "example": "A reportagem sobre a Amazônia foi muito interessante."},
                {"word": "Entrevista", "translation": "Interview", "example": "O jornalista fez uma entrevista exclusiva."},
                {"word": "Influenciador", "translation": "Influencer", "example": "Muitos jovens querem ser influenciadores digitais."},
                {"word": "Fake news", "translation": "Fake news", "example": "É importante verificar as informações antes de compartilhar."}
            ],
            "grammar_points": [
                "Discurso indireto no passado: Ele disse que tinha visto a notícia.",
                "Futuro do pretérito: Eu gostaria de assistir. Seria interessante. Você poderia me dizer?",
                "Conjunções concessivas: embora, apesar de que, mesmo que"
            ]
        },
        {
            "title": "Conteúdo 5: Cultura Popular",
            "content": "Novo Avenida Brasil 3 - Unidades 9-11. A riqueza cultural do Brasil: música (samba, forró, funk, sertanejo), dança, literatura (Machado de Assis, Jorge Amado), cinema e artesanato. Explore expressões idiomáticas e gírias brasileiras comuns.",
            "vocabulary": [
                {"word": "Gíria", "translation": "Slang", "example": "'Legal' é uma gíria que significa 'cool'."},
                {"word": "Cordel", "translation": "String literature", "example": "A literatura de cordel é típica do Nordeste."},
                {"word": "Maracatu", "translation": "Maracatu (dance/music)", "example": "O maracatu é uma manifestação cultural de Pernambuco."},
                {"word": "Capoeira", "translation": "Capoeira", "example": "A capoeira mistura luta, dança e música."},
                {"word": "Patrimônio", "translation": "Heritage", "example": "Ouro Preto é patrimônio histórico da humanidade."},
                {"word": "Artesanato", "translation": "Handicrafts", "example": "O artesanato nordestino é muito colorido."}
            ],
            "grammar_points": [
                "Expressões idiomáticas: estar por fora, ficar de boa, pagar mico, dar um jeitinho",
                "Infinitivo pessoal: É importante estudarmos. Para eles entenderem a cultura.",
                "Regência verbal: gostar DE, precisar DE, assistir A, obedecer A"
            ]
        },
        {
            "title": "Conteúdo 6: Sociedade e Atualidades",
            "content": "Novo Avenida Brasil 3 - Unidades 12-15. Discuta temas atuais da sociedade brasileira: desigualdade social, diversidade, política e economia. Aprenda a construir argumentos, expressar concordância e discordância, e participar de debates.",
            "vocabulary": [
                {"word": "Desigualdade", "translation": "Inequality", "example": "A desigualdade social é um grande desafio no Brasil."},
                {"word": "Cidadania", "translation": "Citizenship", "example": "Exercer a cidadania é um dever de todos."},
                {"word": "Democracia", "translation": "Democracy", "example": "O Brasil é uma democracia desde 1988."},
                {"word": "Direitos humanos", "translation": "Human rights", "example": "Todos têm direito à educação e saúde."},
                {"word": "Economia", "translation": "Economy", "example": "A economia brasileira é a maior da América Latina."},
                {"word": "Política pública", "translation": "Public policy", "example": "As políticas públicas devem beneficiar a todos."}
            ],
            "grammar_points": [
                "Argumentação: Em primeiro lugar, Além disso, Por fim, Em conclusão",
                "Concordância/discordância: Concordo com você. Discordo totalmente. Tem razão, mas...",
                "Mais-que-perfeito composto: Ele já tinha saído quando eu cheguei."
            ]
        }
    ],
    "B2": [
        {
            "title": "Conteúdo 1: Literatura Brasileira",
            "content": "Nível B2 - Aprofundamento. Explore os grandes autores da literatura brasileira: Machado de Assis (Dom Casmurro, Memórias Póstumas de Brás Cubas), Clarice Lispector (A Hora da Estrela), Jorge Amado (Gabriela, Cravo e Canela) e Guimarães Rosa (Grande Sertão: Veredas). Análise de trechos literários e contexto histórico.",
            "vocabulary": [
                {"word": "Romance", "translation": "Novel", "example": "Dom Casmurro é um dos maiores romances brasileiros."},
                {"word": "Conto", "translation": "Short story", "example": "Machado de Assis escreveu contos magistrais."},
                {"word": "Personagem", "translation": "Character", "example": "Capitu é a personagem mais enigmática da literatura."},
                {"word": "Narrador", "translation": "Narrator", "example": "O narrador em primeira pessoa pode ser não confiável."},
                {"word": "Enredo", "translation": "Plot", "example": "O enredo do romance gira em torno de ciúmes."},
                {"word": "Metáfora", "translation": "Metaphor", "example": "A literatura está cheia de metáforas poderosas."}
            ],
            "grammar_points": [
                "Subjuntivo em orações relativas: Preciso de alguém que saiba português.",
                "Colocação pronominal: Enviá-lo-ei (mesóclise), Me disse (próclise informal), Disse-me (ênclise)",
                "Figuras de linguagem: metáfora, ironia, hipérbole, metonímia"
            ]
        },
        {
            "title": "Conteúdo 2: Economia e Negócios",
            "content": "Nível B2. O Brasil como potência econômica: agronegócio, indústria, comércio exterior e startups. Vocabulário de negócios, reuniões profissionais e apresentações corporativas. O 'jeitinho brasileiro' nos negócios e as diferenças culturais no ambiente de trabalho.",
            "vocabulary": [
                {"word": "Empreendedor", "translation": "Entrepreneur", "example": "O Brasil tem muitos empreendedores criativos."},
                {"word": "Investimento", "translation": "Investment", "example": "O investimento estrangeiro cresceu 15%."},
                {"word": "Lucro", "translation": "Profit", "example": "A empresa teve um lucro recorde este trimestre."},
                {"word": "Reunião", "translation": "Meeting", "example": "A reunião com os investidores é às 14h."},
                {"word": "Proposta", "translation": "Proposal", "example": "Apresentei uma proposta comercial ao cliente."},
                {"word": "Mercado", "translation": "Market", "example": "O mercado brasileiro é promissor para startups."}
            ],
            "grammar_points": [
                "Linguagem formal de negócios: Vimos por meio desta..., Conforme acordado...",
                "Futuro do subjuntivo em contexto profissional: Quando a proposta for aprovada...",
                "Verbos de registro formal: requisitar, viabilizar, implementar, otimizar"
            ]
        },
        {
            "title": "Conteúdo 3: Arte e Arquitetura",
            "content": "Nível B2. De Aleijadinho a Niemeyer: a arte e arquitetura brasileiras. Modernismo (Semana de Arte Moderna de 1922), arte contemporânea e a influência africana e indígena. Brasília como patrimônio mundial da UNESCO.",
            "vocabulary": [
                {"word": "Obra-prima", "translation": "Masterpiece", "example": "Brasília é considerada uma obra-prima do modernismo."},
                {"word": "Escultura", "translation": "Sculpture", "example": "As esculturas de Aleijadinho são impressionantes."},
                {"word": "Exposição", "translation": "Exhibition", "example": "A exposição no MASP está imperdível."},
                {"word": "Patrimônio cultural", "translation": "Cultural heritage", "example": "Ouro Preto é patrimônio cultural da humanidade."},
                {"word": "Vanguarda", "translation": "Avant-garde", "example": "O modernismo brasileiro foi um movimento de vanguarda."},
                {"word": "Influência", "translation": "Influence", "example": "A influência africana na arte brasileira é profunda."}
            ],
            "grammar_points": [
                "Orações adjetivas restritivas e explicativas: O artista que criou... / O artista, que nasceu em MG,...",
                "Particípio duplo: aceitado/aceito, pegado/pego, entregado/entregue",
                "Perífrases verbais: estar + gerúndio, ir + infinitivo, acabar de + infinitivo"
            ]
        },
        {
            "title": "Conteúdo 4: Questões Sociais",
            "content": "Nível B2. Debates sobre temas sociais complexos: racismo estrutural, feminismo, LGBTQ+, reforma agrária e acesso à justiça no Brasil. Desenvolva argumentação sofisticada e aprenda a participar de debates formais.",
            "vocabulary": [
                {"word": "Preconceito", "translation": "Prejudice", "example": "O preconceito racial ainda é um problema grave."},
                {"word": "Igualdade", "translation": "Equality", "example": "Lutamos pela igualdade de direitos."},
                {"word": "Inclusão", "translation": "Inclusion", "example": "A inclusão social é fundamental para o desenvolvimento."},
                {"word": "Conscientização", "translation": "Awareness", "example": "É necessária maior conscientização sobre o tema."},
                {"word": "Empoderamento", "translation": "Empowerment", "example": "O empoderamento feminino transforma a sociedade."},
                {"word": "Reforma", "translation": "Reform", "example": "A reforma educacional é urgente."}
            ],
            "grammar_points": [
                "Conectores de causa e consequência: visto que, uma vez que, dado que, de modo que",
                "Subjuntivo em expressões impessoais: É necessário que haja mudanças.",
                "Registro formal para debates: Permita-me discordar. Gostaria de acrescentar..."
            ]
        },
        {
            "title": "Conteúdo 5: História do Brasil",
            "content": "Nível B2. Marcos históricos: colonização portuguesa, escravidão, independência, República, Era Vargas, ditadura militar e redemocratização. Compreenda o Brasil contemporâneo através de sua história.",
            "vocabulary": [
                {"word": "Colonização", "translation": "Colonization", "example": "A colonização portuguesa durou mais de 300 anos."},
                {"word": "Abolição", "translation": "Abolition", "example": "A abolição da escravatura foi em 1888."},
                {"word": "Independência", "translation": "Independence", "example": "A independência do Brasil foi proclamada em 1822."},
                {"word": "Ditadura", "translation": "Dictatorship", "example": "A ditadura militar durou de 1964 a 1985."},
                {"word": "Constituição", "translation": "Constitution", "example": "A Constituição de 1988 é chamada de 'Constituição Cidadã'."},
                {"word": "Redemocratização", "translation": "Re-democratization", "example": "A redemocratização trouxe eleições diretas."}
            ],
            "grammar_points": [
                "Pretérito mais-que-perfeito simples: Quando os portugueses chegaram, os indígenas já habitavam a terra.",
                "Voz passiva em narrativa histórica: O Brasil foi descoberto em 1500.",
                "Marcadores temporais: durante, ao longo de, após, a partir de, desde"
            ]
        },
        {
            "title": "Conteúdo 6: Música Popular Brasileira",
            "content": "Nível B2. MPB: de Bossa Nova a funk carioca. Tom Jobim, Chico Buarque, Caetano Veloso, Gilberto Gil e a nova geração. Análise de letras de músicas, contexto cultural e político da MPB. A tropicália como movimento cultural revolucionário.",
            "vocabulary": [
                {"word": "Letra", "translation": "Lyrics", "example": "As letras de Chico Buarque são poesia pura."},
                {"word": "Melodia", "translation": "Melody", "example": "A melodia da Bossa Nova é suave e sofisticada."},
                {"word": "Ritmo", "translation": "Rhythm", "example": "O samba tem um ritmo contagiante."},
                {"word": "Compositor", "translation": "Composer", "example": "Tom Jobim é o maior compositor brasileiro."},
                {"word": "Movimento", "translation": "Movement", "example": "A Tropicália foi um movimento cultural dos anos 60."},
                {"word": "Censura", "translation": "Censorship", "example": "Durante a ditadura, muitas músicas sofreram censura."}
            ],
            "grammar_points": [
                "Análise de textos poéticos: rima, métrica, linguagem figurada",
                "Conotação e denotação: significado literal vs. figurado em letras de música",
                "Subjuntivo em canções: 'Que seja infinito enquanto dure' (Vinícius de Moraes)"
            ]
        }
    ],
    "C1": [
        {
            "title": "Conteúdo 1: Português Acadêmico",
            "content": "Nível C1. Desenvolva habilidades para leitura e produção de textos acadêmicos em português: artigos científicos, resenhas, dissertações e teses. Normas da ABNT, citação e referenciação. Linguagem acadêmica formal e impessoal.",
            "vocabulary": [
                {"word": "Dissertação", "translation": "Dissertation", "example": "A dissertação de mestrado deve ter rigor metodológico."},
                {"word": "Hipótese", "translation": "Hypothesis", "example": "A hipótese será testada através de pesquisa empírica."},
                {"word": "Metodologia", "translation": "Methodology", "example": "A metodologia utilizada foi a análise qualitativa."},
                {"word": "Referência bibliográfica", "translation": "Bibliographic reference", "example": "As referências devem seguir as normas da ABNT."},
                {"word": "Análise crítica", "translation": "Critical analysis", "example": "O artigo apresenta uma análise crítica do tema."},
                {"word": "Conclusão", "translation": "Conclusion", "example": "Em conclusão, os dados confirmam a hipótese inicial."}
            ],
            "grammar_points": [
                "Impessoalidade: Observa-se que, Verifica-se que, Constata-se que",
                "Modalizadores: possivelmente, provavelmente, aparentemente, supostamente",
                "Estrutura argumentativa: tese, argumentos, contra-argumentos, conclusão"
            ]
        },
        {
            "title": "Conteúdo 2: Variações Linguísticas",
            "content": "Nível C1. O português brasileiro vs. europeu: diferenças fonéticas, lexicais e gramaticais. Variações regionais dentro do Brasil: sotaques e expressões do Nordeste, Sul, Sudeste e Norte. A norma culta vs. linguagem coloquial.",
            "vocabulary": [
                {"word": "Sotaque", "translation": "Accent", "example": "O sotaque carioca é diferente do paulista."},
                {"word": "Dialeto", "translation": "Dialect", "example": "Cada região tem suas expressões e dialetos."},
                {"word": "Norma culta", "translation": "Standard Portuguese", "example": "A norma culta é usada em contextos formais."},
                {"word": "Coloquial", "translation": "Colloquial", "example": "A linguagem coloquial é usada no dia a dia."},
                {"word": "Neologismo", "translation": "Neologism", "example": "A internet criou muitos neologismos."},
                {"word": "Arcaísmo", "translation": "Archaism", "example": "Algumas palavras de Camões são arcaísmos hoje."}
            ],
            "grammar_points": [
                "PT-BR vs. PT-PT: gerúndio vs. infinitivo (Estou fazendo vs. Estou a fazer)",
                "Variações pronominais: tu vs. você, vós vs. vocês, a gente vs. nós",
                "Registros linguísticos: formal, informal, técnico, literário, jurídico"
            ]
        },
        {
            "title": "Conteúdo 3: Direito e Legislação",
            "content": "Nível C1. Introdução ao vocabulário jurídico brasileiro. A Constituição Federal, o Código Civil e o sistema judiciário. Como ler e interpretar textos legais em português. Linguagem jurídica e suas particularidades.",
            "vocabulary": [
                {"word": "Jurisdição", "translation": "Jurisdiction", "example": "O caso está sob jurisdição federal."},
                {"word": "Sentença", "translation": "Sentence/Verdict", "example": "O juiz proferiu a sentença."},
                {"word": "Recurso", "translation": "Appeal", "example": "A defesa entrou com recurso no tribunal."},
                {"word": "Legislação", "translation": "Legislation", "example": "A legislação trabalhista protege os empregados."},
                {"word": "Cláusula", "translation": "Clause", "example": "A cláusula contratual prevê multa por rescisão."},
                {"word": "Jurisprudência", "translation": "Jurisprudence", "example": "A jurisprudência serve como base para decisões futuras."}
            ],
            "grammar_points": [
                "Linguagem jurídica: termos como outrossim, destarte, doravante, supracitado",
                "Voz passiva sintética em textos legais: Fica estabelecido que..., Determina-se que...",
                "Orações subordinadas em textos complexos: Considerando que..., Tendo em vista que..."
            ]
        },
        {
            "title": "Conteúdo 4: Cinema Brasileiro",
            "content": "Nível C1. O Cinema Novo (Glauber Rocha), cinema contemporâneo (Cidade de Deus, Central do Brasil, Tropa de Elite) e documentários. Análise fílmica: narrativa, estética e contexto sociopolítico. O cinema como ferramenta de reflexão social.",
            "vocabulary": [
                {"word": "Roteiro", "translation": "Screenplay", "example": "O roteiro do filme foi adaptado de um livro."},
                {"word": "Diretor", "translation": "Director", "example": "Fernando Meirelles dirigiu Cidade de Deus."},
                {"word": "Fotografia", "translation": "Cinematography", "example": "A fotografia do filme é deslumbrante."},
                {"word": "Trilha sonora", "translation": "Soundtrack", "example": "A trilha sonora contribui para a atmosfera do filme."},
                {"word": "Documentário", "translation": "Documentary", "example": "O documentário sobre a Amazônia ganhou prêmios internacionais."},
                {"word": "Premiação", "translation": "Award ceremony", "example": "O filme recebeu uma premiação em Cannes."}
            ],
            "grammar_points": [
                "Vocabulário de análise fílmica: enquadramento, plano-sequência, montagem",
                "Linguagem de resenha: O filme aborda... A obra retrata... A narrativa explora...",
                "Orações participiais: Dirigido por Glauber Rocha, o filme revolucionou o cinema."
            ]
        },
        {
            "title": "Conteúdo 5: Questões Éticas Contemporâneas",
            "content": "Nível C1. Debates sobre bioética, inteligência artificial, privacidade digital, sustentabilidade e globalização. Desenvolva a capacidade de construir argumentação complexa, analisar diferentes perspectivas e produzir textos dissertativo-argumentativos.",
            "vocabulary": [
                {"word": "Bioética", "translation": "Bioethics", "example": "A bioética questiona os limites da manipulação genética."},
                {"word": "Privacidade", "translation": "Privacy", "example": "A LGPD protege a privacidade dos dados pessoais."},
                {"word": "Inteligência artificial", "translation": "Artificial intelligence", "example": "A inteligência artificial pode transformar o mercado de trabalho."},
                {"word": "Globalização", "translation": "Globalization", "example": "A globalização aproximou culturas, mas também gerou desigualdades."},
                {"word": "Sustentabilidade", "translation": "Sustainability", "example": "A sustentabilidade deve guiar as decisões políticas."},
                {"word": "Ética", "translation": "Ethics", "example": "Questões éticas permeiam o desenvolvimento tecnológico."}
            ],
            "grammar_points": [
                "Argumentação por autoridade: Segundo especialistas... De acordo com pesquisas...",
                "Períodos compostos complexos com múltiplas subordinadas",
                "Coerência e coesão textual: retomada por pronomes, sinônimos e hiperônimos"
            ]
        },
        {
            "title": "Conteúdo 6: Tradução e Interpretação",
            "content": "Nível C1. Princípios de tradução e interpretação português-inglês/espanhol. Desafios da tradução: falsos cognatos, expressões idiomáticas e nuances culturais. Prática com textos de diferentes gêneros.",
            "vocabulary": [
                {"word": "Falso cognato", "translation": "False cognate", "example": "Actually não significa 'atualmente' em português."},
                {"word": "Tradução literal", "translation": "Literal translation", "example": "A tradução literal nem sempre funciona."},
                {"word": "Contexto", "translation": "Context", "example": "O contexto determina o significado da palavra."},
                {"word": "Nuance", "translation": "Nuance", "example": "As nuances culturais são difíceis de traduzir."},
                {"word": "Adaptação", "translation": "Adaptation", "example": "A adaptação cultural é parte do processo de tradução."},
                {"word": "Fidelidade", "translation": "Fidelity", "example": "A fidelidade ao texto original é essencial."}
            ],
            "grammar_points": [
                "Falsos cognatos comuns: pretend (fingir, não pretender), push (empurrar, não puxar)",
                "Estruturas intraduzíveis: saudade, jeitinho, ginga — conceitos culturais únicos",
                "Adaptação de registros: como manter o tom e estilo na tradução"
            ]
        }
    ],
    "C2": [
        {
            "title": "Conteúdo 1: Filosofia e Pensamento Brasileiro",
            "content": "Nível C2. Pensadores brasileiros: Machado de Assis e o pessimismo filosófico, Paulo Freire e a Pedagogia do Oprimido, Darcy Ribeiro e a formação do povo brasileiro. Análise de textos filosóficos e ensaísticos com linguagem sofisticada.",
            "vocabulary": [
                {"word": "Epistemologia", "translation": "Epistemology", "example": "A epistemologia questiona os fundamentos do conhecimento."},
                {"word": "Dialética", "translation": "Dialectics", "example": "A dialética de Paulo Freire propõe educação como liberdade."},
                {"word": "Ontologia", "translation": "Ontology", "example": "A ontologia investiga a natureza do ser."},
                {"word": "Paradigma", "translation": "Paradigm", "example": "A obra de Freire representou uma mudança de paradigma."},
                {"word": "Fenomenologia", "translation": "Phenomenology", "example": "A fenomenologia estuda a experiência vivida."},
                {"word": "Hermenêutica", "translation": "Hermeneutics", "example": "A hermenêutica é a arte da interpretação de textos."}
            ],
            "grammar_points": [
                "Linguagem filosófica: terminologia técnica e construções abstratas",
                "Períodos longos com encadeamento de ideias subordinadas",
                "Registro ensaístico: tom pessoal + argumentação rigorosa"
            ]
        },
        {
            "title": "Conteúdo 2: Linguística Aplicada",
            "content": "Nível C2. Fundamentos de linguística do português: fonologia, morfologia, sintaxe, semântica e pragmática. Análise do discurso e sociolinguística. Variação e mudança linguística no português brasileiro contemporâneo.",
            "vocabulary": [
                {"word": "Morfema", "translation": "Morpheme", "example": "O morfema '-ção' forma substantivos a partir de verbos."},
                {"word": "Fonema", "translation": "Phoneme", "example": "O sistema fonológico do português tem peculiaridades regionais."},
                {"word": "Pragmática", "translation": "Pragmatics", "example": "A pragmática estuda o uso da linguagem em contexto."},
                {"word": "Semântica", "translation": "Semantics", "example": "A semântica analisa o significado das palavras e sentenças."},
                {"word": "Sintaxe", "translation": "Syntax", "example": "A sintaxe do português permite diversas ordens de palavras."},
                {"word": "Sociolinguística", "translation": "Sociolinguistics", "example": "A sociolinguística estuda a relação entre língua e sociedade."}
            ],
            "grammar_points": [
                "Análise sintática avançada: período composto por coordenação e subordinação",
                "Processos de formação de palavras: derivação, composição, hibridismo",
                "Mudança linguística: de 'vós' a 'vocês', proclítico em vez de ênclise no PB"
            ]
        },
        {
            "title": "Conteúdo 3: Produção Textual Avançada",
            "content": "Nível C2. Domine gêneros textuais complexos: artigos de opinião, editorial, ensaio, crônica literária e texto dissertativo-argumentativo (modelo ENEM). Técnicas de persuasão, coerência e coesão avançadas.",
            "vocabulary": [
                {"word": "Tese", "translation": "Thesis", "example": "A tese central do texto defende a reforma educacional."},
                {"word": "Contra-argumento", "translation": "Counterargument", "example": "É preciso considerar os contra-argumentos."},
                {"word": "Editorial", "translation": "Editorial", "example": "O editorial do jornal criticou a decisão governamental."},
                {"word": "Crônica", "translation": "Chronicle", "example": "As crônicas de Rubem Braga são obras-primas do gênero."},
                {"word": "Persuasão", "translation": "Persuasion", "example": "A persuasão é uma técnica fundamental na argumentação."},
                {"word": "Coesão", "translation": "Cohesion", "example": "A coesão textual garante a fluidez do texto."}
            ],
            "grammar_points": [
                "Estratégias de coesão avançada: elipse, catáfora, anáfora, substituição lexical",
                "Modalização epistêmica e deôntica: é provável que, é necessário que",
                "Intertextualidade: citação direta, indireta, alusão, paráfrase"
            ]
        },
        {
            "title": "Conteúdo 4: Relações Internacionais",
            "content": "Nível C2. O Brasil no cenário internacional: BRICS, Mercosul, relações com EUA, Europa e África. Diplomacia brasileira e soft power cultural. Análise de discursos diplomáticos e documentos oficiais.",
            "vocabulary": [
                {"word": "Diplomacia", "translation": "Diplomacy", "example": "A diplomacia brasileira tem tradição pacifista."},
                {"word": "Soberania", "translation": "Sovereignty", "example": "A soberania sobre a Amazônia é um tema sensível."},
                {"word": "Multilateralismo", "translation": "Multilateralism", "example": "O Brasil defende o multilateralismo nas relações internacionais."},
                {"word": "Acordo bilateral", "translation": "Bilateral agreement", "example": "Os dois países assinaram um acordo bilateral de comércio."},
                {"word": "Geopolítica", "translation": "Geopolitics", "example": "A geopolítica mundial está em constante transformação."},
                {"word": "Soft power", "translation": "Soft power", "example": "A cultura brasileira é um instrumento de soft power."}
            ],
            "grammar_points": [
                "Linguagem diplomática formal: protocolos de cortesia e comunicação oficial",
                "Construções concessivas complexas: Ainda que, por mais que, mesmo que + subjuntivo",
                "Registro ultra-formal: Vossa Excelência, Ilustríssimo Senhor, ao ensejo"
            ]
        },
        {
            "title": "Conteúdo 5: Antropologia Cultural",
            "content": "Nível C2. A formação do povo brasileiro segundo Darcy Ribeiro: matrizes indígena, africana e europeia. Sincretismo religioso, culinário e cultural. Identidade brasileira e o conceito de 'brasilidade'. Análise de textos antropológicos.",
            "vocabulary": [
                {"word": "Sincretismo", "translation": "Syncretism", "example": "O sincretismo religioso é uma marca da cultura brasileira."},
                {"word": "Mestiçagem", "translation": "Miscegenation", "example": "A mestiçagem é parte da formação do povo brasileiro."},
                {"word": "Ancestralidade", "translation": "Ancestry", "example": "A ancestralidade africana é celebrada no candomblé."},
                {"word": "Identidade", "translation": "Identity", "example": "A identidade brasileira é plural e diversa."},
                {"word": "Aculturação", "translation": "Acculturation", "example": "O processo de aculturação modificou as tradições indígenas."},
                {"word": "Patrimônio imaterial", "translation": "Intangible heritage", "example": "O samba de roda é patrimônio imaterial da humanidade."}
            ],
            "grammar_points": [
                "Linguagem acadêmica de ciências humanas: terminologia antropológica",
                "Citação e paráfrase em textos acadêmicos: Segundo Ribeiro (1995)...",
                "Construção de parágrafos argumentativos densos e bem articulados"
            ]
        },
        {
            "title": "Conteúdo 6: Expressão e Estilo",
            "content": "Nível C2. O domínio completo da língua portuguesa: estilo pessoal na escrita, humor e ironia, recursos estilísticos avançados. Produza textos com voz autoral, fluidez nativa e domínio de todos os registros.",
            "vocabulary": [
                {"word": "Eufemismo", "translation": "Euphemism", "example": "Usar 'ele partiu' como eufemismo para morte."},
                {"word": "Ironia", "translation": "Irony", "example": "A ironia machadiana é sofisticada e sutil."},
                {"word": "Prosódia", "translation": "Prosody", "example": "A prosódia confere ritmo e musicalidade ao texto."},
                {"word": "Ambiguidade", "translation": "Ambiguity", "example": "A ambiguidade pode ser recurso estilístico ou erro."},
                {"word": "Verossimilhança", "translation": "Verisimilitude", "example": "A narrativa deve ter verossimilhança para convencer."},
                {"word": "Estilística", "translation": "Stylistics", "example": "A estilística analisa os recursos expressivos da língua."}
            ],
            "grammar_points": [
                "Recursos estilísticos: zeugma, assíndeto, polissíndeto, anacoluto",
                "Humor e ironia na escrita: técnicas de construção cômica e subversão de expectativas",
                "Domínio de todos os tempos verbais: presente histórico, futuro epistêmico, imperfeito de cortesia"
            ]
        }
    ]
}

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = 0

    for level, lessons_data in PORTUGUESE_CONTENT.items():
        course = await db.courses.find_one({"language": "portuguese", "level": level})
        if not course:
            print(f"Course portuguese-{level} not found!")
            continue
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for i, data in enumerate(lessons_data):
            if i < len(lessons):
                await db.lessons.update_one(
                    {"_id": lessons[i]["_id"]},
                    {"$set": {
                        "title": data["title"],
                        "content": data["content"],
                        "vocabulary": data["vocabulary"],
                        "grammar_points": data["grammar_points"]
                    }}
                )
                total += 1
        print(f"Updated portuguese-{level}: {min(len(lessons_data), len(lessons))} lessons")

    print(f"\nTotal Portuguese lessons updated: {total}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
