"""Enrich Portuguese lessons with real educational content (like Spanish/English style)."""
import asyncio, os
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

# Rich content for each level - actual teaching material, not TOC descriptions
PT_RICH = {
"A1": [
"""Bem-vindo à sua primeira aula de português brasileiro! Nesta unidade, você vai aprender a cumprimentar pessoas e se apresentar.

Cumprimentos informais: 'Oi!' e 'Olá!' são os mais comuns. 'E aí?' é muito informal. Para perguntar como alguém está: 'Tudo bem?', 'Como vai?', 'Tudo bom?'.

Para se apresentar: 'Eu sou [nome]' ou 'Meu nome é [nome]'. Para perguntar o nome: 'Como você se chama?' ou 'Qual é o seu nome?'.

Respostas comuns: 'Prazer em conhecê-lo/la', 'Muito prazer', 'Igualmente'.

Despedidas: 'Tchau' (bye), 'Até logo' (see you later), 'Até amanhã' (see you tomorrow), 'Até mais' (see you soon), 'Boa noite' (good night).

Nota cultural: No Brasil, os cumprimentos são calorosos. É comum dar um beijo no rosto (ou dois, dependendo da região) entre amigos e familiares.""",

"""Aprenda os números de 0 a 100 em português e como falar sobre idade.

Números de 0 a 10: zero, um, dois, três, quatro, cinco, seis, sete, oito, nove, dez.
Números de 11 a 20: onze, doze, treze, quatorze, quinze, dezesseis, dezessete, dezoito, dezenove, vinte.
Dezenas: trinta, quarenta, cinquenta, sessenta, setenta, oitenta, noventa, cem.

Para falar a idade usamos o verbo TER: 'Quantos anos você tem?' - 'Eu tenho vinte e cinco anos'. Em português dizemos literalmente 'I have 25 years' e não 'I am 25 years old'.

Nota: O número 'um' muda para 'uma' no feminino: 'um livro' mas 'uma casa'. 'Dois' muda para 'duas': 'dois meninos' mas 'duas meninas'.

Moeda: O real brasileiro (R$). 'Quanto custa?' - 'Custa dez reais'. 'Custa um real e cinquenta centavos'.""",

"""Nesta aula você vai aprender o vocabulário da família em português e os hotéis.

Família imediata: pai (father), mãe (mother), irmão (brother), irmã (sister), filho (son), filha (daughter). Os pais = parents, os irmãos = siblings.

Família estendida: avô/avó (grandfather/grandmother), tio/tia (uncle/aunt), primo/prima (cousin), sobrinho/sobrinha (nephew/niece).

Para falar da sua família: 'Minha família é grande/pequena', 'Eu tenho dois irmãos e uma irmã', 'Meu pai se chama João'.

No hotel: 'Eu gostaria de reservar um quarto' (I'd like to book a room). 'Para quantas noites?' (For how many nights?). 'Quarto de solteiro ou de casal?' (Single or double room?). 'O café da manhã está incluído?' (Is breakfast included?).

Possessivos: meu/minha (my), seu/sua (your), nosso/nossa (our). 'Minha mãe é professora', 'Nossos avós moram no Rio'.""",

"""Nesta lição, aprenda sobre comida brasileira e como pedir no restaurante.

Refeições: café da manhã (breakfast), almoço (lunch), jantar (dinner), lanche (snack). O almoço é a refeição principal no Brasil, geralmente entre 12h e 14h.

No restaurante: 'Posso ver o cardápio?' (Can I see the menu?). 'Eu quero/gostaria de...' (I want/would like...). 'A conta, por favor' (The bill, please). 'Está delicioso!' (It's delicious!).

Comidas típicas: feijoada (black bean stew with pork), pão de queijo (cheese bread), açaí (açaí berry bowl), coxinha (chicken croquette), brigadeiro (chocolate truffle).

Bebidas: água (water), suco de laranja (orange juice), café (coffee), cerveja (beer), caipirinha (national cocktail with cachaça, lime and sugar).

Verbo QUERER: eu quero, você quer, nós queremos. 'Eu quero um suco de maracujá, por favor'. Verbo GOSTAR DE: 'Eu gosto de comida brasileira'. 'Você gosta de feijoada?'.""",

"""Aprenda a se locomover nas cidades brasileiras e a pedir direções.

Meios de transporte: ônibus (bus), metrô (subway), táxi (taxi), Uber, avião (airplane), trem (train), bicicleta (bicycle), a pé (on foot).

Pedindo direções: 'Com licença, onde fica...?' (Excuse me, where is...?). 'Como eu chego ao/à...?' (How do I get to...?). 'É longe daqui?' (Is it far from here?). 'É perto' (It's near).

Direções: vire à direita (turn right), vire à esquerda (turn left), siga em frente (go straight), na esquina (at the corner), no semáforo (at the traffic light), na segunda rua (on the second street).

Lugares: o banco (bank), o hospital (hospital), a farmácia (pharmacy), o supermercado (supermarket), a padaria (bakery), o posto de gasolina (gas station).

Verbo IR: eu vou, você vai, nós vamos. 'Eu vou ao supermercado'. Contrações: em + o = no, em + a = na, de + o = do, de + a = da. 'Eu moro no Rio de Janeiro'.""",

"""Aprenda a descrever sua rotina diária em português brasileiro.

Manhã: 'Eu acordo às sete horas' (I wake up at 7). 'Eu tomo banho' (I take a shower). 'Eu tomo café da manhã' (I have breakfast). 'Eu saio de casa às oito' (I leave home at 8).

Tarde: 'Eu almoço ao meio-dia' (I have lunch at noon). 'Eu trabalho das 9 às 18 horas' (I work from 9 to 6). 'Eu faço exercício' (I exercise).

Noite: 'Eu janto às 20 horas' (I have dinner at 8pm). 'Eu assisto TV' (I watch TV). 'Eu durmo às 23 horas' (I sleep at 11pm).

Horas: 'Que horas são?' (What time is it?). 'São oito horas' (It's 8 o'clock). 'É meio-dia' (It's noon). 'São três e meia' (It's 3:30). 'São dez para as cinco' (It's 4:50).

Frequência: sempre (always), geralmente (usually), às vezes (sometimes), nunca (never), todo dia (every day), nos fins de semana (on weekends)."""
],
"A2": [
"""Aprenda a descrever sua casa e apartamento em português.

Cômodos da casa: sala de estar (living room), quarto (bedroom), cozinha (kitchen), banheiro (bathroom), varanda (balcony), garagem (garage), escritório (office).

Descrevendo: 'Meu apartamento tem dois quartos e um banheiro' (My apartment has 2 bedrooms and 1 bathroom). 'A cozinha é grande e moderna' (The kitchen is big and modern). 'O banheiro fica no final do corredor' (The bathroom is at the end of the hallway).

Mobília: sofá (sofa), mesa (table), cadeira (chair), cama (bed), armário (wardrobe), geladeira (fridge), fogão (stove), estante (bookshelf).

Pretérito perfeito: eu falei (I spoke), eu comi (I ate), eu parti (I left). Para verbos -AR: -ei, -ou, -amos, -aram. Para verbos -ER: -i, -eu, -emos, -eram. 'Eu mudei de casa ontem' (I moved house yesterday). 'Nós compramos um sofá novo'.""",

"""Situações práticas de compras em português brasileiro.

No supermercado: 'Eu preciso comprar frutas e legumes' (I need to buy fruits and vegetables). 'Onde fica o setor de laticínios?' (Where is the dairy section?). 'Quanto custa um quilo de tomate?' (How much is a kilo of tomatoes?).

Na loja de roupas: 'Posso experimentar?' (Can I try it on?). 'Tem em outro tamanho?' (Do you have it in another size?). 'Está muito caro' (It's too expensive). 'Tem desconto?' (Is there a discount?). 'Vou levar' (I'll take it).

Formas de pagamento: dinheiro (cash), cartão de crédito/débito (credit/debit card), PIX (instant payment), à vista (cash/upfront), parcelado (installments). 'Pode ser no cartão?' - 'Em quantas vezes?' (In how many installments?).

Pretérito perfeito irregular: fui (I went), fiz (I did/made), tive (I had), estive (I was), disse (I said), trouxe (I brought). 'Eu fui ao shopping ontem'. 'Ela fez um bolo delicioso'.""",

"""Vocabulário de saúde e como se comunicar com médicos em português.

Partes do corpo: cabeça (head), olhos (eyes), boca (mouth), braço (arm), mão (hand), perna (leg), pé (foot), costas (back), peito (chest), estômago (stomach).

No consultório: 'Eu estou com dor de cabeça' (I have a headache). 'Estou com febre' (I have a fever). 'Dói aqui' (It hurts here). 'Desde quando você está assim?' (Since when have you been like this?). 'Tome este remédio de 8 em 8 horas' (Take this medicine every 8 hours).

Expressões com ESTAR COM: estar com fome (to be hungry), estar com sede (to be thirsty), estar com dor (to be in pain), estar com febre (to have a fever), estar com gripe (to have the flu).

Imperativo: tome (take), beba (drink), descanse (rest), durma (sleep), evite (avoid). 'Beba bastante água', 'Descanse por dois dias'. O pretérito imperfeito: eu era, eu tinha, eu fazia, eu ia — para hábitos no passado.""",

"""A cultura e o lazer no Brasil são vibrantes e diversos.

Esportes: futebol (soccer - a paixão nacional), vôlei (volleyball), surfe (surfing), capoeira (martial art/dance). 'O Brasil ganhou cinco Copas do Mundo'. 'Você torce para qual time?' (Which team do you support?).

Música: samba, bossa nova, MPB (Música Popular Brasileira), forró, sertanejo, funk, pagode. 'Eu gosto muito de bossa nova'. 'Vamos a um show de samba?'.

Festas: Carnaval (February/March), Festa Junina (June), Réveillon (New Year). 'O Carnaval do Rio é o maior do mundo'. 'Na Festa Junina, dançamos quadrilha e comemos comidas típicas'.

Fazendo convites: 'Quer ir ao cinema?' (Do you want to go to the movies?). 'Vamos à praia?' (Shall we go to the beach?). 'Que tal um churrasco no domingo?' (How about a BBQ on Sunday?). Futuro com IR: 'Eu vou viajar amanhã'. 'Nós vamos ao show'.""",

"""Aprenda a planejar e descrever viagens pelo Brasil.

Destinos populares: Rio de Janeiro (praias, Cristo Redentor, Pão de Açúcar), São Paulo (gastronomia, cultura, museus), Salvador (centro histórico, cultura afro-brasileira), Florianópolis (praias paradisíacas), Amazônia (floresta tropical, ecoturismo).

No aeroporto: 'Onde é o check-in?' (Where is check-in?). 'Meu voo é às 10 horas' (My flight is at 10). 'Janela ou corredor?' (Window or aisle?). 'A que horas embarcamos?' (What time do we board?).

Reservando hotel: 'Eu gostaria de reservar um quarto para duas noites' (I'd like to book a room for two nights). 'Tem quarto disponível?' (Do you have a room available?). 'O café da manhã está incluído?' (Is breakfast included?).

Contando experiências: 'Eu viajei para o Nordeste' (I traveled to the Northeast). 'A viagem foi incrível!' (The trip was amazing!). 'Nós visitamos praias lindas' (We visited beautiful beaches). Conectores: porque, mas, então, quando, enquanto.""",

"""O Brasil é um dos maiores mercados de tecnologia e comunicação do mundo.

Tecnologia no dia a dia: 'Qual é o seu número de celular?' (What's your cell number?). 'Me manda uma mensagem no WhatsApp' (Send me a WhatsApp message). 'Qual é a senha do Wi-Fi?' (What's the Wi-Fi password?). 'Estou sem internet' (I don't have internet).

Redes sociais: WhatsApp é o aplicativo mais usado no Brasil para comunicação. Instagram, TikTok e YouTube são muito populares. 'Me segue no Instagram!' (Follow me on Instagram!).

E-mails formais: 'Prezado(a) Sr./Sra...' (Dear Mr./Mrs...). 'Venho por meio deste...' (I hereby...). 'Atenciosamente' (Sincerely). 'Aguardo retorno' (I await your response).

Gerúndio (ações em progresso): 'Eu estou trabalhando' (I am working). 'Ela está estudando' (She is studying). 'Nós estamos viajando' (We are traveling). Pronomes: me, te, lhe, nos — 'Me liga depois' (Call me later), 'Te envio amanhã' (I'll send it to you tomorrow)."""
],
"B1": [
"""Aprenda vocabulário e estruturas para o mercado de trabalho brasileiro.

O currículo brasileiro: dados pessoais, objetivo profissional, formação acadêmica, experiência profissional, idiomas, cursos complementares. 'Tenho experiência em atendimento ao cliente' (I have experience in customer service).

Na entrevista: 'Fale sobre você' (Tell me about yourself). 'Quais são seus pontos fortes?' (What are your strengths?). 'Onde você se vê em cinco anos?' (Where do you see yourself in 5 years?). 'Por que você quer trabalhar aqui?' (Why do you want to work here?).

Direitos trabalhistas: CLT (Consolidação das Leis do Trabalho), 13º salário (13th salary bonus), FGTS (workers' fund), férias de 30 dias (30-day vacation). 'O salário mínimo é de R$ 1.518,00' (minimum wage).

Subjuntivo presente: 'É importante que eu estude mais' (It's important that I study more). 'Espero que você consiga o emprego' (I hope you get the job). Conectores: além disso, por outro lado, no entanto, portanto.""",

"""O sistema educacional brasileiro e como falar sobre educação.

Níveis de ensino: educação infantil (preschool), ensino fundamental (elementary/middle - 9 anos), ensino médio (high school - 3 anos), ensino superior (university). 'Eu me formei em Administração' (I graduated in Business Administration).

Vestibular e ENEM: 'O ENEM é a principal prova de acesso à universidade' (ENEM is the main university entrance exam). 'Ele passou no vestibular da USP' (He passed the USP entrance exam). 'Ela ganhou uma bolsa de estudos' (She got a scholarship).

Universidades: públicas (gratuitas - USP, UNICAMP, UFRJ) e privadas (pagas). 'Estudar em uma universidade pública é o sonho de muitos brasileiros'.

Orações condicionais: 'Se eu estudar mais, vou passar no vestibular' (If I study more, I'll pass). 'Se tivesse mais tempo, faria um mestrado' (If I had more time, I would do a master's). Subjuntivo com dúvida: 'Talvez ele passe na prova'. 'Duvido que seja fácil'.""",

"""O meio ambiente e a sustentabilidade no Brasil.

A Amazônia: 'A Amazônia é a maior floresta tropical do mundo' (The Amazon is the world's largest tropical forest). 'O desmatamento ameaça a biodiversidade' (Deforestation threatens biodiversity). '20% do oxigênio do mundo vem da Amazônia' (20% of the world's oxygen comes from the Amazon).

Problemas ambientais: poluição do ar (air pollution), desmatamento (deforestation), queimadas (wildfires), poluição dos rios (river pollution), extinção de espécies (species extinction).

Soluções: reciclagem (recycling), energia solar (solar energy), energia eólica (wind energy), transporte público (public transport), produtos orgânicos (organic products). 'O Brasil produz 80% da sua energia de fontes renováveis' (Brazil produces 80% of its energy from renewable sources).

Expressando opinião: 'Na minha opinião...' (In my opinion), 'Eu acredito que...' (I believe that), 'É evidente que...' (It's evident that). Imperfeito do subjuntivo: 'Se todos reciclassem, o mundo seria melhor'.""",

"""A mídia e a comunicação no Brasil contemporâneo.

Telenovelas: 'As novelas da Globo são assistidas por milhões de brasileiros' (Globo soap operas are watched by millions). 'A novela das 9 é a mais popular' (The 9 o'clock soap opera is the most popular). Novelas famosas: 'Avenida Brasil', 'A Força do Querer'.

Jornalismo: 'O Jornal Nacional é o telejornal mais assistido' (Jornal Nacional is the most watched news). Jornais: Folha de S. Paulo, O Globo, Estado de S. Paulo. 'Você leu a notícia de hoje?' (Did you read today's news?).

Redes sociais e fake news: 'É importante verificar as informações antes de compartilhar' (It's important to verify information before sharing). 'Nem tudo que está na internet é verdade' (Not everything on the internet is true).

Discurso indireto: 'Ele disse que tinha visto a notícia' (He said he had seen the news). 'Ela perguntou se eu assistia novelas' (She asked if I watched soap operas). Futuro do pretérito: 'Eu gostaria de assistir' (I would like to watch), 'Seria interessante' (It would be interesting).""",

"""Explore a riqueza da cultura popular brasileira.

Música: Samba (Rio de Janeiro), Forró (Nordeste), Sertanejo (interior), MPB (Música Popular Brasileira), Funk carioca, Pagode. Artistas: Tom Jobim, Caetano Veloso, Gilberto Gil, Anitta, Jorge Ben Jor. 'A Bossa Nova nasceu nos anos 50 no Rio' (Bossa Nova was born in the 50s in Rio).

Dança: samba, forró, frevo, maracatu, axé, funk. 'No Carnaval, todos dançam samba nas ruas' (During Carnival, everyone dances samba in the streets).

Capoeira: 'A capoeira mistura luta, dança e música' (Capoeira mixes fighting, dance and music). 'Foi criada por africanos escravizados no Brasil' (It was created by enslaved Africans in Brazil).

Expressões idiomáticas: 'Dar um jeitinho' (find a creative solution), 'Ficar de boa' (to chill), 'Pagar mico' (to embarrass yourself), 'Estar por fora' (to be out of the loop). Infinitivo pessoal: 'É importante estudarmos' (It's important for us to study).""",

"""Temas atuais da sociedade brasileira para debates e discussões.

Desigualdade social: 'O Brasil é um dos países mais desiguais do mundo' (Brazil is one of the most unequal countries). 'A favela e o asfalto coexistem nas grandes cidades' (Slums and wealthy areas coexist in big cities).

Diversidade: 'O Brasil é um país multicultural e multirracial' (Brazil is multicultural and multiracial). 'A cultura brasileira é uma mistura de influências indígenas, africanas e europeias' (Brazilian culture is a mix of indigenous, African, and European influences).

Democracia: 'O Brasil é uma república federativa democrática desde 1988' (Brazil has been a democratic federal republic since 1988). 'Votar é obrigatório para cidadãos entre 18 e 70 anos' (Voting is mandatory for citizens between 18 and 70).

Argumentação: 'Em primeiro lugar...' (First of all), 'Além disso...' (Furthermore), 'Por fim...' (Finally), 'Em conclusão...' (In conclusion). Concordar/discordar: 'Concordo com você' (I agree), 'Discordo totalmente' (I totally disagree), 'Tem razão, mas...' (You're right, but...)."""
],
"B2": [
"""Explore os grandes autores da literatura brasileira e suas obras.

Machado de Assis (1839-1908): Considerado o maior escritor brasileiro. Obras: 'Dom Casmurro' - romance sobre ciúmes e dúvida. 'Memórias Póstumas de Brás Cubas' - narrado por um defunto. 'A personagem Capitu: ela traiu ou não traiu Bentinho? É o grande mistério da literatura brasileira'.

Clarice Lispector (1920-1977): Prosa introspectiva e filosófica. 'A Hora da Estrela' conta a história de Macabéa, uma nordestina em São Paulo.

Jorge Amado (1912-2001): Retratou a Bahia e o povo brasileiro. 'Gabriela, Cravo e Canela' mistura sensualidade e política.

Guimarães Rosa (1908-1967): Revolucionou a linguagem. 'Grande Sertão: Veredas' usa uma linguagem inventiva baseada no falar sertanejo.

Análise literária: narrador (narrator), personagem (character), enredo (plot), cenário (setting), tema (theme), clímax (climax). Subjuntivo em relativas: 'Preciso de alguém que saiba português'. Colocação pronominal: 'Enviar-lhe-ei o livro'.""",

"""O Brasil como potência econômica e o mundo dos negócios.

Setores da economia: agronegócio (soja, café, carne), indústria (automóveis, aço, petróleo), serviços (tecnologia, turismo, finanças). 'O Brasil é o maior produtor mundial de café' (Brazil is the world's largest coffee producer).

Negócios: 'Marcamos uma reunião para terça-feira' (We scheduled a meeting for Tuesday). 'Apresentei a proposta ao cliente' (I presented the proposal to the client). 'O investimento terá retorno em dois anos' (The investment will pay off in two years).

Startups: 'O ecossistema de startups brasileiro é o maior da América Latina'. Termos: pitch, MVP (produto mínimo viável), venture capital, escalabilidade.

Cultura empresarial: No Brasil, relações pessoais são importantes nos negócios. Reuniões podem começar com conversa informal. 'Jeitinho brasileiro' — a capacidade de encontrar soluções criativas para problemas burocráticos.

Linguagem formal: 'Vimos por meio desta informar...' (We hereby inform...). Futuro do subjuntivo: 'Quando a proposta for aprovada...' (When the proposal is approved...).""",

"""A arte e arquitetura brasileiras: de Aleijadinho a Niemeyer.

Período colonial: Aleijadinho (1738-1814) criou esculturas barrocas em Ouro Preto e Congonhas. 'Os Doze Profetas de Congonhas são considerados sua obra-prima' (The Twelve Prophets are considered his masterpiece).

Modernismo: A Semana de Arte Moderna de 1922 revolucionou a cultura brasileira. Artistas: Tarsila do Amaral ('Abaporu'), Anita Malfatti, Di Cavalcanti, Villa-Lobos (música).

Arquitetura: Oscar Niemeyer projetou Brasília (1960), Patrimônio Mundial da UNESCO. 'As curvas de Niemeyer são reconhecidas mundialmente'. Catedral de Brasília, Congresso Nacional, Museu de Arte Contemporânea de Niterói.

Arte contemporânea: Vik Muniz (fotografias com materiais inusitados), Beatriz Milhazes (pinturas vibrantes), Ernesto Neto (instalações sensoriais). Museus: MASP (São Paulo), MAM (Rio de Janeiro).

Orações adjetivas: 'O artista que criou...' (restritiva) vs. 'O artista, que nasceu em MG,...' (explicativa). Particípio: aceitado/aceito, entregado/entregue.""",

"""Debates sobre questões sociais complexas do Brasil contemporâneo.

Racismo estrutural: 'O Brasil foi o último país das Américas a abolir a escravidão (1888)'. 'Cotas raciais nas universidades foram implementadas para reduzir a desigualdade'. 'O Dia da Consciência Negra é celebrado em 20 de novembro'.

Feminismo: 'As mulheres representam 51% da população brasileira'. 'A Lei Maria da Penha (2006) protege mulheres contra violência doméstica'. 'A desigualdade salarial entre homens e mulheres ainda é um problema'.

Direitos LGBTQ+: 'O STF reconheceu a união estável homoafetiva em 2011'. 'São Paulo tem a maior Parada do Orgulho LGBT do mundo'.

Reforma agrária: 'O MST (Movimento dos Trabalhadores Rurais Sem Terra) luta pela distribuição de terras'.

Argumentação avançada: 'Visto que...' (Given that), 'Uma vez que...' (Since), 'De modo que...' (So that). Registro formal: 'Permita-me discordar' (Allow me to disagree). 'Gostaria de acrescentar...' (I would like to add...).""",

"""Os principais marcos da história do Brasil, da colonização à atualidade.

Colonização (1500-1822): Pedro Álvares Cabral chegou ao Brasil em 22 de abril de 1500. Os portugueses exploraram pau-brasil, açúcar e ouro. 'O ciclo do ouro transformou Minas Gerais no século XVIII'.

Escravidão e Abolição: 'Mais de 4 milhões de africanos foram trazidos ao Brasil'. Lei Áurea (1888): 'A Princesa Isabel assinou a lei que aboliu a escravidão'. 'O Brasil foi o último país das Américas a abolir a escravidão'.

Independência (1822): 'Dom Pedro I proclamou a independência às margens do Rio Ipiranga'. República (1889): 'O Marechal Deodoro da Fonseca proclamou a República'.

Ditadura militar (1964-1985): 'O golpe de 1964 instaurou uma ditadura que durou 21 anos'. 'As Diretas Já (1984) foram o maior movimento popular pela democracia'.

Pretérito mais-que-perfeito: 'Quando os portugueses chegaram, os indígenas já habitavam a terra'. Voz passiva histórica: 'O Brasil foi descoberto em 1500'.""",

"""A Música Popular Brasileira (MPB) e sua importância cultural.

Bossa Nova (1950s-60s): Tom Jobim e Vinícius de Moraes criaram 'Garota de Ipanema' — a segunda música mais gravada do mundo. 'A Bossa Nova mistura samba e jazz'. João Gilberto revolucionou o violão brasileiro.

Tropicália (1960s): Caetano Veloso e Gilberto Gil misturaram rock, psicodelia e música brasileira. 'A Tropicália foi um movimento de resistência durante a ditadura'.

MPB: Chico Buarque — poeta e compositor genial. 'As letras de Chico Buarque são poesia pura'. 'Construção' é considerada uma das maiores músicas brasileiras.

Samba: Cartola, Noel Rosa, Clara Nunes, Beth Carvalho. 'O samba nasceu nas comunidades afro-brasileiras do Rio de Janeiro'.

Música contemporânea: Anitta (pop/funk internacional), Marisa Monte, Seu Jorge. 'A música brasileira é exportada para o mundo todo'.

Análise de letras: 'Que seja infinito enquanto dure' (Vinícius de Moraes). Conotação e denotação: significado literal vs. figurado."""
],
"C1": [
"""Desenvolva habilidades para leitura e produção de textos acadêmicos em português.

Estrutura de uma dissertação: Introdução (contextualização, problema de pesquisa, objetivos, justificativa), Fundamentação Teórica, Metodologia, Resultados, Discussão, Conclusão, Referências.

Linguagem acadêmica: 'Observa-se que...' (It is observed that), 'Verifica-se que...' (It is verified that), 'Os dados indicam que...' (The data indicate that). Evite primeira pessoa: use 'foi realizado' em vez de 'eu realizei'.

Citação: 'Segundo Freire (1970), a educação é um ato político'. 'De acordo com a pesquisa de Silva (2020)...'. Normas ABNT: referências bibliográficas, citação direta e indireta.

Conectores acadêmicos: 'Nesse sentido...' (In this sense), 'Cabe ressaltar que...' (It is worth noting that), 'Em contrapartida...' (On the other hand), 'Conclui-se que...' (It is concluded that).

Modalizadores: possivelmente, provavelmente, aparentemente, supostamente. 'É provável que os resultados confirmem a hipótese'.""",

"""As variações do português: brasileiro vs. europeu, e as diferenças regionais.

PT-BR vs. PT-PT: Gerúndio vs. infinitivo: 'Estou fazendo' (BR) vs. 'Estou a fazer' (PT). Pronomes: 'Eu te amo' (BR) vs. 'Eu amo-te' (PT). Vocabulário: ônibus (BR) vs. autocarro (PT), trem (BR) vs. comboio (PT), celular (BR) vs. telemóvel (PT).

Sotaques brasileiros: Carioca (Rio - 'sh' em final de sílaba: 'mesmosh'), Paulista (São Paulo - 'r' retroflexo: 'porrrta'), Nordestino ('ti' e 'di' abertos: 'tchia', 'djia'), Sulista (influência italiana e alemã), Mineiro (palavras cortadas: 'Uai, sô').

Gírias regionais: 'Bah, tchê!' (RS), 'Uai!' (MG), 'Oxe!' (NE), 'Mano!' (SP), 'Meu rei!' (BA).

Norma culta vs. coloquial: 'Nós vamos' (culta) vs. 'A gente vai' (coloquial). 'Vou ao cinema' (culta) vs. 'Vou no cinema' (coloquial).

Registros: formal (acadêmico, jurídico), informal (conversas), técnico (profissional), literário (romances, poesia).""",

"""Introdução ao vocabulário jurídico brasileiro e ao sistema legal.

Sistema judiciário: STF (Supremo Tribunal Federal), STJ (Superior Tribunal de Justiça), tribunais estaduais, juízes, promotores, advogados. 'O STF é a última instância do judiciário brasileiro'.

Termos jurídicos: sentença (verdict), recurso (appeal), ação (lawsuit), réu (defendant), autor (plaintiff), habeas corpus, mandado de segurança, liminar (injunction).

Constituição Federal (1988): 'Todos são iguais perante a lei' (All are equal before the law). Direitos fundamentais: liberdade, igualdade, saúde, educação, moradia, segurança.

Direito do consumidor: O Código de Defesa do Consumidor (1990) protege compradores. 'O consumidor tem direito à informação clara sobre produtos'.

Linguagem jurídica: 'Fica estabelecido que...' (It is hereby established), 'Nos termos da lei...' (Under the terms of the law), 'Sem prejuízo de...' (Without prejudice to). Voz passiva sintética: 'Determina-se que...', 'Fica assegurado que...'.""",

"""O cinema brasileiro: do Cinema Novo à produção contemporânea.

Cinema Novo (1960s): Glauber Rocha — 'Deus e o Diabo na Terra do Sol', 'Terra em Transe'. Lema: 'Uma câmera na mão e uma ideia na cabeça'. O Cinema Novo retratou a pobreza e a injustiça social.

Cinema contemporâneo: 'Cidade de Deus' (2002) — drama sobre favelas cariocas, indicado ao Oscar. 'Central do Brasil' (1998) — Fernanda Montenegro quase ganhou o Oscar. 'Tropa de Elite' (2007) — corrupção policial.

Documentários: 'Edifício Master' (Eduardo Coutinho), 'Estamira', 'Democracia em Vertigem' (indicado ao Oscar).

Festivais: Festival de Gramado, Mostra Internacional de Cinema de São Paulo, Festival de Brasília.

Vocabulário de cinema: roteiro (screenplay), diretor (director), elenco (cast), fotografia (cinematography), trilha sonora (soundtrack), estreia (premiere). Resenha: 'O filme aborda...', 'A obra retrata...', 'A narrativa explora...'.""",

"""Debates sobre questões éticas contemporâneas em português avançado.

Inteligência Artificial: 'A IA pode substituir empregos humanos?' 'Quais são os limites éticos da automação?' 'A LGPD (Lei Geral de Proteção de Dados) regulamenta o uso de dados pessoais no Brasil'.

Bioética: 'A manipulação genética levanta questões morais'. 'O aborto é um tema controverso no Brasil'. 'A eutanásia não é legalizada no país'.

Sustentabilidade: 'O agronegócio é vital para a economia, mas causa desmatamento'. 'Como equilibrar desenvolvimento e preservação ambiental?'

Globalização: 'A globalização aproximou culturas, mas também gerou desigualdades'. 'As redes sociais conectam pessoas, mas podem causar dependência digital'.

Argumentação por autoridade: 'Segundo especialistas da ONU...', 'De acordo com pesquisas recentes...'. Períodos compostos complexos com subordinadas. Coerência textual: retomada por sinônimos e hiperônimos.""",

"""Princípios de tradução e os desafios de traduzir entre português e outros idiomas.

Falsos cognatos: 'actually' não é 'atualmente' (actually = na verdade). 'push' não é 'puxar' (push = empurrar). 'pretend' não é 'pretender' (pretend = fingir). 'parents' não é 'parentes' (parents = pais).

Expressões intraduzíveis: 'Saudade' — sentimento de falta de algo ou alguém. Não tem tradução exata. 'Cafuné' — carinho nos cabelos. 'Jeitinho brasileiro' — forma criativa de resolver problemas.

Desafios da tradução: adaptar humor e ironia, manter o ritmo do texto, respeitar referências culturais. 'Uma boa tradução preserva o sentido, não apenas as palavras'.

Técnicas: tradução literal (word-for-word), tradução livre (sense-for-sense), adaptação (cultural adaptation), transposição (mudança de categoria gramatical).

Registros na tradução: como manter o tom formal/informal. 'Você' pode ser traduzido como 'you', mas perde a distinção formal/informal do inglês britânico (you) vs. do espanhol (tú/usted)."""
],
"C2": [
"""Pensadores brasileiros e suas contribuições para a filosofia e as ciências humanas.

Paulo Freire (1921-1997): 'Pedagogia do Oprimido' (1968) propõe educação como prática de liberdade. 'Ninguém educa ninguém, ninguém educa a si mesmo, os homens se educam entre si, mediatizados pelo mundo'. Método Paulo Freire: alfabetização através da conscientização política.

Machado de Assis e a filosofia: pessimismo filosófico, ironia como ferramenta de análise social. 'O narrador não confiável em Brás Cubas questiona a própria natureza da verdade'.

Darcy Ribeiro (1922-1997): 'O Povo Brasileiro' analisa a formação étnica e cultural do Brasil. 'Somos um povo novo, surgido do encontro de indígenas, africanos e europeus'.

Gilberto Freyre (1900-1987): 'Casa-Grande & Senzala' examina as relações raciais na sociedade colonial. Conceito de 'democracia racial' — hoje amplamente criticado.

Linguagem filosófica: terminologia técnica, construções abstratas, períodos longos com encadeamento de subordinadas.""",

"""Fundamentos de linguística do português: como a língua funciona.

Fonologia: o português brasileiro tem cerca de 33 fonemas. O 'r' tem múltiplas realizações: [h] (carioca: 'porta'), [ɾ] (retroflexo caipira), [r] (vibrante gaúcho). O 't' e 'd' antes de 'i' viram [tʃ] e [dʒ] em muitas regiões: 'tia' = [tʃia].

Morfologia: prefixos (des-, in-, re-), sufixos (-ção, -mente, -ável), processos: derivação (feliz → felicidade), composição (guarda-chuva), hibridismo (televisão: grego + latim).

Sintaxe: ordem SVO predominante, mas flexível. 'O menino comeu o bolo' vs. 'O bolo, o menino comeu'. Topicalização é muito comum na fala: 'Esse livro, eu já li'.

Sociolinguística: variação diastrática (classe social), diatópica (região), diafásica (registro/situação). 'A gente vai' vs. 'Nós iremos' — mesma mensagem, registros diferentes.

Mudança linguística: de 'vós' a 'vocês', proclítico em vez de ênclise ('Me dá' em vez de 'Dê-me'). O português está sempre evoluindo.""",

"""Domine gêneros textuais complexos em português.

Dissertação argumentativa (estilo ENEM): Introdução (contextualização + tese), dois parágrafos de desenvolvimento (argumento + exemplo + conclusão parcial), conclusão (proposta de intervenção com agente, ação, meio, finalidade e detalhamento).

Exemplo de tese: 'A persistência da violência contra a mulher no Brasil é resultado da combinação entre machismo estrutural e ineficiência do aparato legal'.

Crônica: gênero híbrido entre jornalismo e literatura. Rubem Braga, Fernando Sabino, Luis Fernando Verissimo. Tom pessoal, observação do cotidiano, humor. 'A crônica é o gênero mais brasileiro de todos'.

Editorial: texto opinativo de um jornal. Impessoal, mas com posicionamento claro. 'Este jornal defende que...' 'A medida é insuficiente para resolver...'.

Coesão avançada: elipse (omissão), catáfora (antecipação), anáfora (retomada), substituição lexical. Modalização: 'É provável que...', 'É necessário que...'. Intertextualidade: citação, alusão, paráfrase.""",

"""O Brasil no cenário internacional: diplomacia, comércio e soft power.

BRICS: Brasil, Rússia, Índia, China e África do Sul. 'O Brasil busca protagonismo entre as economias emergentes'. Mercosul: bloco econômico com Argentina, Uruguai e Paraguai.

Diplomacia: Itamaraty (Ministério das Relações Exteriores). 'A tradição diplomática brasileira é pacifista e multilateral'. O Brasil busca um assento permanente no Conselho de Segurança da ONU.

Soft power: 'A cultura brasileira — música, futebol, carnaval, gastronomia — é um instrumento de influência global'. 'O Brasil exporta entretenimento, moda e estilo de vida'.

Comércio: principais parceiros: China, EUA, Argentina, UE. Exportações: soja, minério de ferro, petróleo, carne, café, celulose.

Linguagem diplomática: 'Vossa Excelência' (Your Excellency), 'Ao ensejo, renovo os protestos de elevada estima e consideração'. Construções concessivas: 'Ainda que haja dificuldades, o diálogo deve continuar'.""",

"""A formação do povo brasileiro: uma perspectiva antropológica.

Três matrizes: indígena (Tupi, Guarani, Yanomami — mais de 300 etnias), africana (Yorubá, Bantu, Fon — trazidos pela escravidão), europeia (portugueses principalmente, depois italianos, alemães, japoneses, árabes).

Sincretismo religioso: Candomblé mistura tradições africanas com catolicismo. Iemanjá = Nossa Senhora. Ogum = São Jorge. 'O sincretismo é uma marca da identidade brasileira'.

Culinária: acarajé (africana), mandioca e açaí (indígena), pão e vinho (europeia). 'A feijoada é um símbolo do sincretismo culinário brasileiro'.

Identidade: 'O que é ser brasileiro?' Gilberto Freyre falou de 'democracia racial' — conceito hoje questionado. Darcy Ribeiro descreveu os brasileiros como 'um povo novo', diferente de suas matrizes originárias.

Patrimônio imaterial: samba de roda, frevo, capoeira, arte Kusiwa (indígena) — reconhecidos pela UNESCO. Citação acadêmica: 'Segundo Ribeiro (1995), o Brasil é fruto de um processo de transfiguração étnica'.""",

"""O domínio completo da língua portuguesa: estilo, humor e sofisticação.

Ironia machadiana: Machado de Assis usava ironia sutil para criticar a sociedade. 'Marcela amou-me durante quinze meses e onze contos de réis' (Brás Cubas). A ironia revela a hipocrisia das relações humanas.

Humor brasileiro: stand-up comedy, memes, piadas regionais. Trocadilhos: 'O que o pato disse para a pata? — Vem Quá!' (quá = quack + vem cá). 'Por que o livro de matemática se suicidou? Porque tinha muitos problemas'.

Eufemismos: 'Ele partiu' (morreu), 'Ela está descansando' (dormindo/morta), 'Pessoa em situação de rua' (morador de rua).

Registros: ultra-formal (jurídico: 'Outrossim, cumpre informar'), formal (acadêmico: 'Observa-se que'), semiformal (e-mail profissional), informal (WhatsApp), íntimo (família/amigos).

Domínio completo: presente histórico ('Em 1500, Cabral chega ao Brasil'), futuro epistêmico ('Deve ser verdade'), imperfeito de cortesia ('Eu queria pedir um favor'). Proverbs: 'Quem com ferro fere, com ferro será ferido'. 'Água mole em pedra dura, tanto bate até que fura'."""
]
}

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = 0
    for level, contents in PT_RICH.items():
        course = await db.courses.find_one({"language": "portuguese", "level": level})
        if not course: continue
        lessons = await db.lessons.find({"course_id": str(course["_id"])}).sort("_id", 1).to_list(None)
        for i, content in enumerate(contents):
            if i < len(lessons):
                await db.lessons.update_one({"_id": lessons[i]["_id"]}, {"$set": {"content": content}})
                total += 1
        print(f"Enriched portuguese-{level}: {min(len(contents), len(lessons))} lessons")
    print(f"\nTotal: {total}")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
