import os
import re
import secrets
import sqlite3
import unicodedata
from datetime import timedelta
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, g, abort, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
import conteudo
from banco import (iniciar_banco, consultar, executar, executar_varios,
                   agora, agora_texto)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "chave-apenas-para-testes-locais-troque-em-producao")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True

iniciar_banco()

DIAS_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

PADRAO_DIAS = {1: [0], 2: [0, 3], 3: [0, 2, 4], 4: [0, 1, 3, 4],
               5: [0, 1, 2, 3, 4], 6: [0, 1, 2, 3, 4, 5], 7: [0, 1, 2, 3, 4, 5, 6]}

FRASES = ["O progresso pode ser lento, mas nunca se perde.",
          "Grandes conquistas começam com um pequeno passo.",
          "Um pouco de inglês por dia leva você longe.",
          "Errar faz parte de aprender. Continue!"]

def normalizar(texto):
    texto = unicodedata.normalize("NFD", (texto or "").lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace("’", "'")
    texto = re.sub(r"[^a-z0-9' ]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()

def resposta_correta(resposta_do_aluno, gabarito):
    aceitas = [normalizar(g_) for g_ in gabarito.split("|")]
    return normalizar(resposta_do_aluno) in aceitas

def usuario_logado():
    if "usuario" not in g:
        usuario_id = session.get("usuario_id")
        g.usuario = consultar("SELECT * FROM usuarios WHERE id = ?", (usuario_id,), um=True) if usuario_id else None
    return g.usuario

def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if usuario_logado() is None:
            session.clear()
            flash("Faça login para acessar esta página.", "erro")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return verificar

def gerar_csrf():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]

@app.before_request
def verificar_csrf():
    if request.method == "POST":
        enviado = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token") or ""
        esperado = session.get("csrf", "")
        if not esperado or not enviado or not secrets.compare_digest(enviado, esperado):
            abort(400)

@app.context_processor
def variaveis_para_todos_os_templates():
    return dict(usuario=usuario_logado(), csrf_token=gerar_csrf(),
                NOMES_NIVEL=conteudo.NOMES_NIVEL, NOMES_TIPO=conteudo.NOMES_TIPO,
                DIAS_SEMANA=DIAS_SEMANA)

@app.template_filter("data_br")
def data_br(texto):
    return f"{texto[8:10]}/{texto[5:7]}/{texto[0:4]} {texto[11:16]}"

def datas_de_estudo(usuario_id):
    linhas = consultar(
        "SELECT date(data) FROM progresso WHERE usuario_id = ? "
        "UNION SELECT date(data) FROM testes_nivel WHERE usuario_id = ?",
        (usuario_id, usuario_id))
    return {linha[0] for linha in linhas}

def calcular_sequencia(datas):
    dia = agora().date()
    if dia.isoformat() not in datas:
        dia = dia - timedelta(days=1)
    sequencia = 0
    while dia.isoformat() in datas:
        sequencia += 1
        dia = dia - timedelta(days=1)
    return sequencia

def ultimos_7_dias(datas):
    hoje = agora().date()
    dias = [hoje - timedelta(days=i) for i in range(6, -1, -1)]
    return [(DIAS_SEMANA[d.weekday()], d.isoformat() in datas) for d in dias]

def resumo_plano(usuario_id):
    plano = consultar("SELECT * FROM planos_estudo WHERE usuario_id = ? AND ativo = 1", (usuario_id,), um=True)
    if plano is None:
        return None, 0, 0
    contagem = consultar(
        "SELECT COUNT(*) AS total, "
        "SUM(CASE WHEN EXISTS (SELECT 1 FROM progresso p WHERE p.plano_item_id = pi.id) THEN 1 ELSE 0 END) AS feitas "
        "FROM plano_itens pi WHERE pi.plano_id = ?", (plano["id"],), um=True)
    return plano, contagem["total"], contagem["feitas"] or 0

def verificar_conquistas(usuario_id):
    total = consultar("SELECT COUNT(*) AS n FROM progresso WHERE usuario_id = ?", (usuario_id,), um=True)["n"]
    acertos_por_tipo = {l["tipo"]: l["n"] for l in consultar(
        "SELECT a.tipo, COUNT(*) AS n FROM progresso p JOIN atividades a ON a.id = p.atividade_id "
        "WHERE p.usuario_id = ? AND p.acertou = 1 GROUP BY a.tipo", (usuario_id,))}
    testes = consultar("SELECT COUNT(*) AS n FROM testes_nivel WHERE usuario_id = ?", (usuario_id,), um=True)["n"]
    mensagens = consultar("SELECT COUNT(*) AS n FROM mensagens_mike WHERE usuario_id = ? AND autor = 'usuario'",
                          (usuario_id,), um=True)["n"]
    xp = consultar("SELECT xp_total FROM usuarios WHERE id = ?", (usuario_id,), um=True)["xp_total"]
    sequencia = calcular_sequencia(datas_de_estudo(usuario_id))

    regras = {
        "primeiro_teste": testes >= 1,
        "primeira_atividade": total >= 1,
        "cinco_atividades": total >= 5,
        "vinte_atividades": total >= 20,
        "tres_dias": sequencia >= 3,
        "sete_dias": sequencia >= 7,
        "vocabulario_5": acertos_por_tipo.get("vocabulario", 0) >= 5,
        "gramatica_5": acertos_por_tipo.get("gramatica", 0) >= 5,
        "escrita_5": acertos_por_tipo.get("escrita", 0) >= 5,
        "xp_100": xp >= 100,
        "amigo_mike": mensagens >= 1,
    }
    ja_ganhas = {l["codigo"] for l in consultar(
        "SELECT c.codigo FROM usuario_conquistas uc JOIN conquistas c ON c.id = uc.conquista_id "
        "WHERE uc.usuario_id = ?", (usuario_id,))}

    novas = []
    for codigo, ganhou in regras.items():
        if ganhou and codigo not in ja_ganhas:
            conquista = consultar("SELECT id, nome FROM conquistas WHERE codigo = ?", (codigo,), um=True)
            executar("INSERT INTO usuario_conquistas (usuario_id, conquista_id, data) VALUES (?, ?, ?)",
                     (usuario_id, conquista["id"], agora_texto()))
            novas.append(conquista["nome"])
    return novas

def avisar_conquistas(nomes):
    for nome in nomes:
        flash(f"🏅 Nova conquista desbloqueada: {nome}!", "sucesso")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if usuario_logado():
        return redirect(url_for("painel"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        erros = []
        if len(nome) < 2 or len(nome) > 80:
            erros.append("Informe seu nome completo (2 a 80 caracteres).")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or len(email) > 120:
            erros.append("Informe um e-mail válido.")
        if len(senha) < 6:
            erros.append("A senha precisa ter pelo menos 6 caracteres.")
        for erro in erros:
            flash(erro, "erro")
        if erros:
            return render_template("cadastro.html", nome=nome, email=email)

        try:
            novo_id = executar(
                "INSERT INTO usuarios (nome, email, senha_hash, data_cadastro) VALUES (?, ?, ?, ?)",
                (nome, email, generate_password_hash(senha), agora_texto()))
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "erro")
            return render_template("cadastro.html", nome=nome, email=email)

        session.clear()
        session["usuario_id"] = novo_id
        flash("Conta criada com sucesso! Vamos descobrir o seu nível de inglês.", "sucesso")
        return redirect(url_for("teste_intro"))

    return render_template("cadastro.html", nome="", email="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if usuario_logado():
        return redirect(url_for("painel"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = consultar("SELECT * FROM usuarios WHERE email = ?", (email,), um=True)

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            if usuario["nivel_atual"] is None:
                return redirect(url_for("teste_intro"))
            return redirect(url_for("painel"))

        flash("E-mail ou senha incorretos.", "erro")
        return render_template("login.html", email=email)

    return render_template("login.html", email="")

@app.route("/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Você saiu da sua conta. Até logo!", "sucesso")
    return redirect(url_for("index"))

@app.route("/painel")
@login_obrigatorio
def painel():
    usuario = usuario_logado()
    datas = datas_de_estudo(usuario["id"])
    plano, total, feitas = resumo_plano(usuario["id"])
    conquistas_recentes = consultar(
        "SELECT c.nome, c.icone FROM usuario_conquistas uc JOIN conquistas c ON c.id = uc.conquista_id "
        "WHERE uc.usuario_id = ? ORDER BY uc.data DESC LIMIT 3", (usuario["id"],))
    meta_xp = (usuario["xp_total"] // 100 + 1) * 100
    return render_template("painel.html", sequencia=calcular_sequencia(datas),
                           semana=ultimos_7_dias(datas), plano=plano, total=total, feitas=feitas,
                           conquistas_recentes=conquistas_recentes, meta_xp=meta_xp,
                           frase=FRASES[agora().day % len(FRASES)])

@app.route("/teste-nivel")
@login_obrigatorio
def teste_intro():
    total = consultar("SELECT COUNT(*) AS n FROM questoes", um=True)["n"]
    return render_template("teste_intro.html", total=total)

@app.route("/teste-nivel/fazer")
@login_obrigatorio
def teste_fazer():
    linhas = consultar("SELECT id, enunciado, opcoes FROM questoes ORDER BY id")
    questoes = [{"id": l["id"], "enunciado": l["enunciado"], "opcoes": l["opcoes"].split("|")} for l in linhas]
    return render_template("teste_fazer.html", questoes=questoes)

@app.route("/teste-nivel/enviar", methods=["POST"])
@login_obrigatorio
def teste_enviar():
    usuario = usuario_logado()
    acertos_por_nivel = {n: 0 for n in conteudo.NIVEIS}
    total_acertos = 0

    for questao in consultar("SELECT id, resposta, nivel FROM questoes"):
        enviada = request.form.get(f"q_{questao['id']}", "")
        if resposta_correta(enviada, questao["resposta"]):
            acertos_por_nivel[questao["nivel"]] += 1
            total_acertos += 1

    nivel = "A1"
    for n in conteudo.NIVEIS:
        if acertos_por_nivel[n] >= 3:
            nivel = n
        else:
            break

    executar_varios([
        ("INSERT INTO testes_nivel (usuario_id, pontuacao, nivel_resultado, data) VALUES (?, ?, ?, ?)",
         (usuario["id"], total_acertos, nivel, agora_texto())),
        ("UPDATE usuarios SET nivel_atual = ? WHERE id = ?", (nivel, usuario["id"])),
    ])
    avisar_conquistas(verificar_conquistas(usuario["id"]))
    return redirect(url_for("teste_resultado"))


@app.route("/teste-nivel/resultado")
@login_obrigatorio
def teste_resultado():
    teste = consultar("SELECT * FROM testes_nivel WHERE usuario_id = ? ORDER BY id DESC LIMIT 1",
                      (usuario_logado()["id"],), um=True)
    if teste is None:
        return redirect(url_for("teste_intro"))
    return render_template("teste_resultado.html", teste=teste)

@app.route("/plano/criar", methods=["POST"])
@login_obrigatorio
def plano_criar():
    usuario = usuario_logado()
    if usuario["nivel_atual"] is None:
        flash("Faça o teste de nível antes de criar seu plano.", "erro")
        return redirect(url_for("teste_intro"))

    try:
        dias = int(request.form.get("dias", ""))
        minutos = int(request.form.get("minutos", ""))
    except ValueError:
        dias, minutos = 0, 0
    if dias not in PADRAO_DIAS or minutos not in (15, 30, 45, 60):
        flash("Escolha uma quantidade válida de dias e minutos.", "erro")
        return redirect(url_for("meu_plano"))

    atividades = consultar("SELECT id, tipo FROM atividades WHERE nivel = ? ORDER BY id", (usuario["nivel_atual"],))
    por_tipo = {t: [a["id"] for a in atividades if a["tipo"] == t] for t in conteudo.NOMES_TIPO}
    sequencia = []
    for i in range(max(len(v) for v in por_tipo.values())):
        for tipo in ("vocabulario", "gramatica", "escrita"):
            if i < len(por_tipo[tipo]):
                sequencia.append(por_tipo[tipo][i])

    por_dia = minutos // 15
    comandos, posicao = [], 0
    plano_id = None

    executar("UPDATE planos_estudo SET ativo = 0 WHERE usuario_id = ?", (usuario["id"],))
    plano_id = executar(
        "INSERT INTO planos_estudo (usuario_id, nivel, dias_por_semana, minutos_por_dia, ativo, data_criacao) "
        "VALUES (?, ?, ?, ?, 1, ?)", (usuario["id"], usuario["nivel_atual"], dias, minutos, agora_texto()))

    for dia_semana in PADRAO_DIAS[dias]:
        for _ in range(por_dia):
            atividade_id = sequencia[posicao % len(sequencia)]
            comandos.append(("INSERT INTO plano_itens (plano_id, atividade_id, dia_semana) VALUES (?, ?, ?)",
                             (plano_id, atividade_id, dia_semana)))
            posicao += 1
    executar_varios(comandos)

    flash("Seu plano de estudos foi criado!", "sucesso")
    return redirect(url_for("meu_plano"))

@app.route("/meu-plano")
@login_obrigatorio
def meu_plano():
    usuario = usuario_logado()
    plano, total, feitas = resumo_plano(usuario["id"])
    dias = {}
    if plano:
        itens = consultar(
            "SELECT pi.id, pi.dia_semana, a.titulo, a.tipo, a.xp, "
            "(SELECT COUNT(*) FROM progresso p WHERE p.plano_item_id = pi.id) AS feito "
            "FROM plano_itens pi JOIN atividades a ON a.id = pi.atividade_id "
            "WHERE pi.plano_id = ? ORDER BY pi.dia_semana, pi.id", (plano["id"],))
        for item in itens:
            dias.setdefault(item["dia_semana"], []).append(item)
    return render_template("plano.html", plano=plano, total=total, feitas=feitas,
                           dias=dias, hoje=agora().weekday())

@app.route("/atividade/<int:item_id>", methods=["GET", "POST"])
@login_obrigatorio
def atividade(item_id):
    usuario = usuario_logado()
    item = consultar(
        "SELECT pi.id AS item_id, a.id AS atividade_id, a.titulo, a.tipo, a.enunciado, a.opcoes, "
        "a.resposta, a.explicacao, a.xp "
        "FROM plano_itens pi JOIN atividades a ON a.id = pi.atividade_id "
        "JOIN planos_estudo pl ON pl.id = pi.plano_id "
        "WHERE pi.id = ? AND pl.usuario_id = ?", (item_id, usuario["id"]), um=True)
    if item is None:
        abort(404)

    anterior = consultar("SELECT * FROM progresso WHERE plano_item_id = ? AND usuario_id = ?",
                         (item_id, usuario["id"]), um=True)

    if request.method == "POST":
        if anterior:
            return redirect(url_for("atividade", item_id=item_id))
        resposta = request.form.get("resposta", "").strip()[:200]
        if not resposta:
            flash("Responda antes de enviar.", "erro")
            return redirect(url_for("atividade", item_id=item_id))

        acertou = 1 if resposta_correta(resposta, item["resposta"]) else 0
        xp = item["xp"] if acertou else 0
        executar_varios([
            ("INSERT INTO progresso (usuario_id, atividade_id, plano_item_id, resposta_usuario, acertou, xp_ganho, data) "
             "VALUES (?, ?, ?, ?, ?, ?, ?)",
             (usuario["id"], item["atividade_id"], item_id, resposta, acertou, xp, agora_texto())),
            ("UPDATE usuarios SET xp_total = xp_total + ? WHERE id = ?", (xp, usuario["id"])),
        ])
        avisar_conquistas(verificar_conquistas(usuario["id"]))
        return redirect(url_for("atividade", item_id=item_id))

    opcoes = item["opcoes"].split("|") if item["opcoes"] else []
    return render_template("atividade.html", item=item, opcoes=opcoes, anterior=anterior)

@app.route("/progresso")
@login_obrigatorio
def progresso():
    usuario = usuario_logado()
    uid = usuario["id"]
    datas = datas_de_estudo(uid)
    plano, total_plano, feitas_plano = resumo_plano(uid)

    resumo = consultar("SELECT COUNT(*) AS total, COALESCE(SUM(acertou), 0) AS acertos "
                       "FROM progresso WHERE usuario_id = ?", (uid,), um=True)

    habilidades = {t: {"total": 0, "acertos": 0} for t in conteudo.NOMES_TIPO}
    for l in consultar("SELECT a.tipo, COUNT(*) AS total, SUM(p.acertou) AS acertos FROM progresso p "
                       "JOIN atividades a ON a.id = p.atividade_id WHERE p.usuario_id = ? GROUP BY a.tipo", (uid,)):
        habilidades[l["tipo"]] = {"total": l["total"], "acertos": l["acertos"]}

    xp_por_dia = {l[0]: l[1] for l in consultar(
        "SELECT date(data), SUM(xp_ganho) FROM progresso WHERE usuario_id = ? GROUP BY date(data)", (uid,))}
    hoje = agora().date()
    grafico = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)
        grafico.append((DIAS_SEMANA[dia.weekday()], xp_por_dia.get(dia.isoformat(), 0)))
    maior = max([xp for _, xp in grafico] + [1])

    historico = consultar(
        "SELECT p.data, p.acertou, p.xp_ganho, a.titulo, a.tipo FROM progresso p "
        "JOIN atividades a ON a.id = p.atividade_id WHERE p.usuario_id = ? ORDER BY p.id DESC LIMIT 15", (uid,))
    testes = consultar("SELECT * FROM testes_nivel WHERE usuario_id = ? ORDER BY id DESC", (uid,))

    return render_template("progresso.html", resumo=resumo, habilidades=habilidades, grafico=grafico,
                           maior=maior, historico=historico, testes=testes, sequencia=calcular_sequencia(datas),
                           plano=plano, total_plano=total_plano, feitas_plano=feitas_plano)

@app.route("/conquistas")
@login_obrigatorio
def conquistas():
    lista = consultar(
        "SELECT c.nome, c.descricao, c.icone, uc.data FROM conquistas c "
        "LEFT JOIN usuario_conquistas uc ON uc.conquista_id = c.id AND uc.usuario_id = ? ORDER BY c.id",
        (usuario_logado()["id"],))
    return render_template("conquistas.html", lista=lista, ganhas=sum(1 for c in lista if c["data"]))

def responder_mike(mensagem):
    texto = " " + normalizar(mensagem) + " "
    melhor, melhor_pontos = conteudo.RESPOSTA_PADRAO_MIKE, 0
    for linha in consultar("SELECT palavras_chave, resposta FROM base_mike"):
        pontos = sum(1 for palavra in linha["palavras_chave"].split("|")
                     if " " + normalizar(palavra) + " " in texto)
        if pontos > melhor_pontos:
            melhor, melhor_pontos = linha["resposta"], pontos
    return melhor

@app.route("/mike")
@login_obrigatorio
def mike():
    historico = consultar("SELECT autor, texto FROM mensagens_mike WHERE usuario_id = ? "
                          "ORDER BY id DESC LIMIT 50", (usuario_logado()["id"],))[::-1]
    return render_template("mike.html", historico=historico)

@app.route("/mike/enviar", methods=["POST"])
@login_obrigatorio
def mike_enviar():
    dados = request.get_json(silent=True) or {}
    texto = str(dados.get("texto", "")).strip()[:300]
    if not texto:
        return jsonify({"erro": "Digite uma mensagem."}), 400

    uid = usuario_logado()["id"]
    resposta = responder_mike(texto)
    executar_varios([
        ("INSERT INTO mensagens_mike (usuario_id, autor, texto, data) VALUES (?, 'usuario', ?, ?)",
         (uid, texto, agora_texto())),
        ("INSERT INTO mensagens_mike (usuario_id, autor, texto, data) VALUES (?, 'mike', ?, ?)",
         (uid, resposta, agora_texto())),
    ])
    novas = verificar_conquistas(uid)
    return jsonify({"resposta": resposta, "conquistas": novas})

@app.route("/perfil")
@login_obrigatorio
def perfil():
    return render_template("perfil.html")

@app.errorhandler(400)
def erro_400(e):
    return render_template("erro.html", codigo=400, mensagem="Pedido inválido. Volte e tente novamente."), 400

@app.errorhandler(404)
def erro_404(e):
    return render_template("erro.html", codigo=404, mensagem="Página não encontrada."), 404

@app.errorhandler(500)
def erro_500(e):
    return render_template("erro.html", codigo=500, mensagem="Algo deu errado no servidor."), 500

if __name__ == "__main__":
    app.run(debug=True)
