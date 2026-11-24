NIVEIS = ["A1", "A2", "B1", "B2", "C1"]

NOMES_NIVEL = {
    "A1": "Iniciante",
    "A2": "Básico",
    "B1": "Intermediário",
    "B2": "Intermediário Superior",
    "C1": "Avançado",
}

XP_POR_NIVEL = {"A1": 10, "A2": 10, "B1": 15, "B2": 15, "C1": 20}

NOMES_TIPO = {"vocabulario": "Vocabulário", "gramatica": "Gramática", "escrita": "Escrita"}

QUESTOES = [
    # ---- A1 ----
    ("She ___ a teacher.", "am|is|are|be", "is", "A1"),
    ("I have two ___.", "brother|brothers|brother's|a brother", "brothers", "A1"),
    ("What is the opposite of 'big'?", "small|tall|old|fast", "small", "A1"),
    ("___ you like coffee?", "Do|Does|Is|Are", "Do", "A1"),

    # ---- A2 ----
    ("Yesterday I ___ to the market.", "go|goes|went|going", "went", "A2"),
    ("My sister is ___ than me.", "tall|taller|tallest|more tall", "taller", "A2"),
    ("There ___ any milk in the fridge.", "isn't|aren't|don't|not", "isn't", "A2"),
    ("I'm going to the dentist ___ Monday.", "in|on|at|to", "on", "A2"),

    # ---- B1 ----
    ("If it rains tomorrow, we ___ at home.", "stay|will stay|would stay|stayed", "will stay", "B1"),
    ("I have lived here ___ 2019.", "for|since|from|during", "since", "B1"),
    ("The report ___ by the manager yesterday.", "wrote|was written|has written|is writing", "was written", "B1"),
    ("I'm not used to ___ up early.", "get|getting|got|gets", "getting", "B1"),

    # ---- B2 ----
    ("I wish I ___ more free time.", "have|had|would have|having", "had", "B2"),
    ("By the time we arrived, the film ___.", "already started|had already started|has already started|was already starting", "had already started", "B2"),
    ("She is ___ to win the competition.", "likely|probably|possibly|perhaps", "likely", "B2"),
    ("Despite ___ hard, he failed the exam.", "study|studied|studying|he studied", "studying", "B2"),

    # ---- C1 ----
    ("Had I known about the delay, I ___ earlier.", "would leave|would have left|will leave|had left", "would have left", "C1"),
    ("Choose the word closest in meaning to 'ubiquitous':", "rare|widespread|dangerous|ancient", "widespread", "C1"),
    ("Not only ___ late, but he also forgot the documents.", "he was|was he|he is|is he", "was he", "C1"),
    ("The committee decided to ___ the meeting until further notice.", "adjourn|adjust|adopt|admit", "adjourn", "C1"),
]

ATIVIDADES = [
    ("A1", "vocabulario", "Cores", "What color is the sky on a sunny day?", "blue|green|red|black", "blue", "Sky = céu e blue = azul."),
    ("A1", "vocabulario", "Família", "Your mother's mother is your ___.", "grandmother|sister|aunt|daughter", "grandmother", "Grandmother = avó."),
    ("A1", "vocabulario", "Dias da semana", "The day after Monday is ___.", "Sunday|Tuesday|Friday|Wednesday", "Tuesday", "Tuesday = terça-feira."),
    ("A1", "gramatica", "Verbo to be (he/she/it)", "He ___ from Brazil.", "am|are|is|be", "is", "Com he, she e it usamos 'is'."),
    ("A1", "gramatica", "Presente contínuo", "They ___ playing football now.", "is|am|are|be", "are", "Com they usamos 'are'. Presente contínuo: am/is/are + verbo-ing."),
    ("A1", "gramatica", "Artigos a / an", "This is ___ apple.", "a|an|the|some", "an", "Usamos 'an' antes de som de vogal: an apple."),
    ("A1", "escrita", "Escrevendo: to be", "Complete com o verbo to be: I ___ a student.", "", "am", "Com I usamos 'am': I am a student."),
    ("A1", "escrita", "Escrevendo: plural", "Escreva o plural de 'book'.", "", "books", "Regra geral: acrescente -s. Book → books."),
    ("A1", "escrita", "Escrevendo: cortesia", "Como se diz 'obrigado' em inglês?", "", "thank you|thanks", "Thank you ou thanks."),

    ("A2", "vocabulario", "Lugares", "A place where you buy medicine is a ___.", "pharmacy|library|bakery|bank", "pharmacy", "Pharmacy = farmácia."),
    ("A2", "vocabulario", "Opostos", "The opposite of 'cheap' is ___.", "expensive|slow|quiet|empty", "expensive", "Cheap = barato; expensive = caro."),
    ("A2", "vocabulario", "Refeições", "'Breakfast' is the meal you have in the ___.", "morning|evening|night|afternoon", "morning", "Breakfast = café da manhã."),
    ("A2", "gramatica", "Presente simples", "She ___ TV every night.", "watch|watches|watching|watched", "watches", "Com he/she/it, o verbo ganha -s (-es depois de ch, sh, s, x)."),
    ("A2", "gramatica", "Passado contínuo", "We ___ dinner when the phone rang.", "have|had|were having|are having", "were having", "Ação em andamento no passado: was/were + verbo-ing."),
    ("A2", "gramatica", "Superlativo", "This is the ___ book I have ever read.", "good|better|best|most good", "best", "Good → better → best (formas irregulares)."),
    ("A2", "escrita", "Escrevendo: passado", "Escreva o passado de 'go'.", "", "went", "Go é irregular: go → went → gone."),
    ("A2", "escrita", "Escrevendo: quantidade", "Complete: How ___ apples do you want?", "", "many", "Substantivos contáveis usam 'many'; incontáveis usam 'much'."),
    ("A2", "escrita", "Escrevendo: opostos", "Escreva o oposto de 'hot'.", "", "cold", "Hot = quente; cold = frio."),

    ("B1", "vocabulario", "Verbos de trabalho", "To 'postpone' a meeting means to ___ it.", "cancel|delay|start|record", "delay", "Postpone = adiar."),
    ("B1", "vocabulario", "Profissões", "A person who works for a company is an ___.", "employee|employer|engineer|expert", "employee", "Employee = funcionário; employer = empregador."),
    ("B1", "vocabulario", "Sinônimos", "Choose the synonym of 'tired':", "exhausted|excited|empty|early", "exhausted", "Exhausted = exausto, muito cansado."),
    ("B1", "gramatica", "Segunda condicional", "If I ___ rich, I would travel the world.", "am|was|were|will be", "were", "Segunda condicional: If + passado, would + verbo. Com 'if' usa-se 'were' para todas as pessoas."),
    ("B1", "gramatica", "For ou since", "She has worked here ___ five years.", "since|for|ago|during", "for", "For = duração (for five years); since = ponto de partida (since 2020)."),
    ("B1", "gramatica", "Voz passiva", "The door ___ every evening at 8.", "locks|is locked|locked|is locking", "is locked", "Voz passiva: to be + particípio passado."),
    ("B1", "escrita", "Escrevendo: particípio", "Escreva o particípio passado de 'write'.", "", "written", "Write → wrote → written."),
    ("B1", "escrita", "Escrevendo: preposição", "Complete com uma palavra: I'm interested ___ learning English.", "", "in", "Interested in = interessado em."),
    ("B1", "escrita", "Escrevendo: passado irregular", "Complete com a forma correta de 'make': She ___ a cake yesterday.", "", "made", "Make → made → made."),

    ("B2", "vocabulario", "Confiança", "'Reliable' describes someone you can ___.", "trust|forget|avoid|pay", "trust", "Reliable = confiável."),
    ("B2", "vocabulario", "Sinônimos", "'Reduce' is closest in meaning to ___.", "increase|decrease|repeat|replace", "decrease", "Reduce = reduzir, diminuir."),
    ("B2", "vocabulario", "Prazos", "A 'deadline' is ___.", "the final time to finish something|a type of job|a long meeting|a kind of document", "the final time to finish something", "Deadline = prazo final."),
    ("B2", "gramatica", "Would rather", "I'd rather you ___ smoke here.", "don't|didn't|won't|not", "didn't", "Com 'would rather + pessoa', usa-se o passado: I'd rather you didn't."),
    ("B2", "gramatica", "Verbo + gerúndio", "She suggested ___ a taxi.", "to take|taking|take|took", "taking", "Depois de 'suggest' usamos o verbo com -ing."),
    ("B2", "gramatica", "Deny + gerúndio", "He denied ___ the window.", "break|breaking|to break|broke", "breaking", "Depois de 'deny' usamos o verbo com -ing."),
    ("B2", "escrita", "Escrevendo: preposição", "Complete com uma palavra: She is good ___ math.", "", "at", "Good at = bom em."),
    ("B2", "escrita", "Escrevendo: past perfect", "Complete: They had ___ before I arrived. (verbo 'leave')", "", "left", "Past perfect: had + particípio passado (left)."),
    ("B2", "escrita", "Escrevendo: comparativo", "Complete: The more you practice, the ___ you become. (good)", "", "better", "Good → better."),

    ("C1", "vocabulario", "Precisão", "'Meticulous' means ___.", "careless|very careful and precise|lazy|angry", "very careful and precise", "Meticulous = meticuloso."),
    ("C1", "vocabulario", "Riscos", "To 'mitigate' a risk means to ___.", "increase it|reduce its effect|ignore it|measure it", "reduce its effect", "Mitigate = atenuar, reduzir o efeito."),
    ("C1", "vocabulario", "Atitudes", "'Reluctant' is closest in meaning to ___.", "unwilling|excited|ready|curious", "unwilling", "Reluctant = relutante."),
    ("C1", "gramatica", "Inversão", "Hardly ___ the room when the lights went out.", "he had entered|had he entered|he entered|did he enter", "had he entered", "Após 'hardly' no início da frase, invertemos sujeito e auxiliar."),
    ("C1", "gramatica", "Would sooner", "I'd sooner ___ at home than go to that party.", "stay|to stay|staying|stayed", "stay", "Would sooner/rather + verbo no infinitivo sem 'to'."),
    ("C1", "gramatica", "It's high time", "It's high time we ___ a decision.", "make|made|will make|are making", "made", "Depois de 'it's high time' usa-se o passado."),
    ("C1", "escrita", "Escrevendo: condicional", "Complete com uma palavra: Were it not ___ your help, I would have failed.", "", "for", "'Were it not for' = se não fosse por."),
    ("C1", "escrita", "Escrevendo: no sooner", "Complete com uma palavra: No sooner had she arrived ___ it started to rain.", "", "than", "No sooner ... than = assim que ..."),
    ("C1", "escrita", "Escrevendo: substantivo", "Escreva o substantivo de 'decide'.", "", "decision", "Decide → decision."),
]

CONQUISTAS = [
    ("primeiro_teste", "Primeiros Passos", "Conclua o teste de nível.", "🧭"),
    ("primeira_atividade", "Mãos à Obra", "Complete sua primeira atividade.", "✏️"),
    ("cinco_atividades", "Pegando o Ritmo", "Complete 5 atividades.", "🚀"),
    ("vinte_atividades", "Dedicação", "Complete 20 atividades.", "🏆"),
    ("tres_dias", "Constância", "Estude 3 dias seguidos.", "🔥"),
    ("sete_dias", "Semana Perfeita", "Estude 7 dias seguidos.", "🌟"),
    ("vocabulario_5", "Vocabulário", "Acerte 5 atividades de vocabulário.", "📚"),
    ("gramatica_5", "Gramática", "Acerte 5 atividades de gramática.", "🧩"),
    ("escrita_5", "Escrita", "Acerte 5 atividades de escrita.", "🖊️"),
    ("xp_100", "100 de XP", "Chegue a 100 pontos de XP.", "⭐"),
    ("amigo_mike", "Amigo do Mike", "Converse com o Mike pela primeira vez.", "🐶"),
]

BASE_MIKE = [
    ("oi|olá|ola|hello|hi|bom dia|boa tarde|boa noite",
     "Olá! Eu sou o Mike 🐶, seu companheiro de estudos. Pode me perguntar sobre gramática, vocabulário ou escrita em inglês!"),
    ("present perfect|presente perfeito",
     "O Present Perfect usa have/has + particípio passado e liga o passado ao presente: 'I have lived here for five years.' Use 'for' para duração (for five years) e 'since' para o ponto de partida (since 2019)."),
    ("past simple|passado simples|passado",
     "No Past Simple, verbos regulares ganham -ed (work → worked) e os irregulares mudam (go → went). Em perguntas e negativas usamos did + verbo base: 'Did you go?' e 'I didn't go.'"),
    ("present simple|presente simples|terceira pessoa",
     "O Present Simple serve para hábitos e fatos. Com he/she/it o verbo ganha -s: 'She works.' Perguntas e negativas usam do/does: 'Does she work?'"),
    ("present continuous|presente continuo|gerundio",
     "O Present Continuous usa am/is/are + verbo com -ing e fala do que está acontecendo agora: 'I am studying English.'"),
    ("to be|verbo to be",
     "Verbo to be: I am, you are, he/she/it is, we/they are. Negativa: is not (isn't). Pergunta: inverta a ordem: 'Are you ready?'"),
    ("artigo|artigos|a or an|an or a",
     "Use 'a' antes de som de consoante (a book) e 'an' antes de som de vogal (an apple, an hour). O que importa é o SOM, não a letra!"),
    ("preposicao|preposicoes|in on at|on at in",
     "At: horas e lugares exatos (at 8 pm, at home). On: dias e datas (on Monday). In: meses, anos e períodos (in July, in 2026, in the morning)."),
    ("plural",
     "Regra geral: +s (book → books). Depois de s, x, ch, sh: +es (box → boxes). Consoante + y: ies (city → cities). Irregulares: child → children, man → men."),
    ("condicional|if|conditional",
     "Primeira condicional: If + presente, will + verbo ('If it rains, we will stay'). Segunda: If + passado, would + verbo ('If I were rich, I would travel')."),
    ("phrasal verb|phrasal verbs",
     "Phrasal verbs são verbo + partícula: give up = desistir, look for = procurar, turn on = ligar. O melhor jeito de aprender é decorar dentro de frases."),
    ("vocabulario|palavras novas|memorizar|decorar",
     "Dicas de vocabulário: aprenda palavras dentro de frases, revise depois de 1, 3 e 7 dias e use as atividades de vocabulário do seu plano todos os dias."),
    ("escrita|writing|redacao|escrever|texto",
     "Para melhorar a escrita: comece com frases curtas e simples, releia procurando sujeito e verbo, e escreva 3 frases por dia usando palavras novas."),
    ("gramatica|grammar",
     "Estude um tópico gramatical por vez. Nas atividades de gramática do seu plano você pratica e vê a explicação logo depois de responder."),
    ("pronuncia|pronunciar|falar|speaking",
     "Ainda não trabalho com áudio, mas uma dica: ouça músicas e vídeos com legenda em inglês e repita em voz alta, imitando o ritmo."),
    ("plano|rotina|estudar|estudo|tempo",
     "Constância vale mais que tempo! 15 minutos por dia já ajudam muito. Você pode ajustar seus dias e minutos na página Meu Plano."),
    ("nivel|teste|a1|a2|b1|b2|c1",
     "Os níveis vão de A1 (iniciante) a C1 (avançado). Você pode refazer o teste quando quiser em Teste de Nível para atualizar seu plano."),
    ("dificil|desanimado|desanimada|desistir|cansado|cansada|motivacao",
     "Aprender um idioma é uma trilha longa, e todo mundo tem dias difíceis. Um passo pequeno por dia já conta. Você está indo bem! 🐾"),
    ("obrigado|obrigada|thanks|thank you|valeu",
     "De nada! You're welcome! 🐾"),
]

RESPOSTA_PADRAO_MIKE = ("Hmm, ainda não sei responder isso 🐾. Tente perguntar sobre: present perfect, past simple, "
                        "preposições (in/on/at), artigos, plural, condicional (if), phrasal verbs, vocabulário, "
                        "escrita ou motivação.")
