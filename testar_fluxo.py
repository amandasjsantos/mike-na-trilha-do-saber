import os
import re
import banco

banco.CAMINHO_DO_BANCO = os.path.join(banco.PASTA_DO_PROJETO, "mike_teste.db")
if os.path.exists(banco.CAMINHO_DO_BANCO):
    os.remove(banco.CAMINHO_DO_BANCO)

import app as sistema

cliente = sistema.app.test_client()
falhas = []

def conferir(descricao, condicao):
    print(("  OK    " if condicao else "  FALHA ") + descricao)
    if not condicao:
        falhas.append(descricao)

def token():
    cliente.get("/")
    with cliente.session_transaction() as s:
        return s["csrf"]

def post(url, **dados):
    dados["csrf_token"] = token()
    return cliente.post(url, data=dados, follow_redirects=True)

print("\n[1] Páginas públicas")
for rota in ["/", "/login", "/cadastro"]:
    conferir(f"GET {rota} abre (200)", cliente.get(rota).status_code == 200)
conferir("Página restrita redireciona quem não logou", cliente.get("/painel").status_code == 302)
conferir("POST sem CSRF é bloqueado (400)", cliente.post("/login", data={"email": "a@a.com"}).status_code == 400)

print("\n[2] Cadastro e login")
r = post("/cadastro", nome="Ana Teste", email="ana@teste.com", senha="123")
conferir("Senha curta é recusada", "pelo menos 6 caracteres" in r.get_data(as_text=True))
r = post("/cadastro", nome="Ana Teste", email="ana@teste.com", senha="senha123")
conferir("Cadastro válido leva ao teste de nível", "Teste de Nível" in r.get_data(as_text=True))
post("/sair")
r = post("/cadastro", nome="Ana Teste", email="ana@teste.com", senha="senha123")
conferir("E-mail repetido é recusado", "já está cadastrado" in r.get_data(as_text=True))
r = post("/login", email="ana@teste.com", senha="errada")
conferir("Senha errada é recusada", "incorretos" in r.get_data(as_text=True))
r = post("/login", email="ana@teste.com", senha="senha123")
conferir("Login correto funciona", "Teste de Nível" in r.get_data(as_text=True))
hash_guardado = banco.consultar("SELECT senha_hash FROM usuarios", um=True)[0]
conferir("Senha guardada como hash (não em texto)", "senha123" not in hash_guardado)

print("\n[3] Teste de nível")
r = cliente.get("/teste-nivel/fazer")
html = r.get_data(as_text=True)
conferir("Teste mostra 20 questões", html.count('class="questao') == 20)
conferir("Respostas corretas NÃO vão para o navegador", "value=\"is\"" in html and "gabarito" not in html)
respostas = {f"q_{q['id']}": q["resposta"] for q in banco.consultar("SELECT id, resposta FROM questoes")}
r = post("/teste-nivel/enviar", **respostas)
conferir("Gabarito completo dá nível C1", "C1" in r.get_data(as_text=True) and "20 de 20" in r.get_data(as_text=True))
conferir("Nível salvo no usuário", banco.consultar("SELECT nivel_atual FROM usuarios", um=True)[0] == "C1")

respostas_a1 = {f"q_{q['id']}": q["resposta"] for q in banco.consultar("SELECT id, resposta FROM questoes WHERE nivel='A1'")}
post("/teste-nivel/enviar", **respostas_a1)
conferir("Só A1 certo dá nível A1", banco.consultar("SELECT nivel_atual FROM usuarios", um=True)[0] == "A1")
post("/teste-nivel/enviar", **{f"q_{q['id']}": q["resposta"] for q in banco.consultar("SELECT id, resposta FROM questoes WHERE nivel IN ('A1','A2','B1')")})
conferir("A1+A2+B1 certos dá nível B1", banco.consultar("SELECT nivel_atual FROM usuarios", um=True)[0] == "B1")

print("\n[4] Plano de estudos")
r = cliente.get("/meu-plano")
conferir("Meu Plano abre sem plano", r.status_code == 200 and "Criar meu plano" in r.get_data(as_text=True))
r = post("/plano/criar", dias="3", minutos="30")
conferir("Plano criado", "atividades concluídas" in r.get_data(as_text=True))
itens = banco.consultar("SELECT id FROM plano_itens")
conferir("3 dias x 2 atividades = 6 itens", len(itens) == 6)
r = post("/plano/criar", dias="9", minutos="30")
conferir("Valores inválidos são recusados", "válida" in r.get_data(as_text=True))

print("\n[5] Atividades, XP e conquistas")
primeiro = itens[0]["id"]
r = cliente.get(f"/atividade/{primeiro}")
conferir("Atividade abre", r.status_code == 200)
ativ = banco.consultar("SELECT a.resposta FROM plano_itens pi JOIN atividades a ON a.id=pi.atividade_id WHERE pi.id=?", (primeiro,), um=True)
r = post(f"/atividade/{primeiro}", resposta=ativ["resposta"].split("|")[0])
conferir("Resposta certa mostra 'Correto'", "Correto" in r.get_data(as_text=True))
xp = banco.consultar("SELECT xp_total FROM usuarios", um=True)[0]
conferir("XP somado (10 pontos no nível B1 = 15)", xp == 15)
post(f"/atividade/{primeiro}", resposta="qualquer")
conferir("Não dá para responder duas vezes", banco.consultar("SELECT COUNT(*) FROM progresso", um=True)[0] == 1)
r = post(f"/atividade/{itens[1]['id']}", resposta="resposta errada")
conferir("Resposta errada não dá XP", banco.consultar("SELECT xp_total FROM usuarios", um=True)[0] == 15)
conferir("Conquistas 'Primeiros Passos' e 'Mãos à Obra' ganhas",
         banco.consultar("SELECT COUNT(*) FROM usuario_conquistas", um=True)[0] >= 2)

print("\n[6] Segurança entre usuários")
post("/sair")
post("/cadastro", nome="Bia Teste", email="bia@teste.com", senha="senha123")
conferir("Outro aluno não acessa atividade alheia (404)", cliente.get(f"/atividade/{primeiro}").status_code == 404)

print("\n[7] Progresso, conquistas, Mike e perfil")
post("/sair")
post("/login", email="ana@teste.com", senha="senha123")
for rota in ["/painel", "/progresso", "/conquistas", "/mike", "/perfil", "/teste-nivel", "/teste-nivel/resultado", "/meu-plano"]:
    conferir(f"GET {rota} abre (200)", cliente.get(rota).status_code == 200)
tk = token()
r = cliente.post("/mike/enviar", json={"texto": "Como funciona o present perfect?"}, headers={"X-CSRF-Token": tk})
conferir("Mike responde sobre present perfect", "have/has" in r.get_json()["resposta"])
r = cliente.post("/mike/enviar", json={"texto": "asdfgh"}, headers={"X-CSRF-Token": tk})
conferir("Mike responde algo quando não entende", "ainda não sei" in r.get_json()["resposta"])
r = cliente.post("/mike/enviar", json={"texto": "  "}, headers={"X-CSRF-Token": tk})
conferir("Mensagem vazia é recusada (400)", r.status_code == 400)
conferir("Conquista 'Amigo do Mike' ganha", banco.consultar("SELECT COUNT(*) FROM usuario_conquistas uc JOIN conquistas c ON c.id=uc.conquista_id WHERE c.codigo='amigo_mike'", um=True)[0] == 1)
conferir("Página 404 amigável", cliente.get("/nao-existe").status_code == 404)

print("\nRESULTADO:", "TUDO CERTO" if not falhas else f"{len(falhas)} falha(s)")
os.remove(banco.CAMINHO_DO_BANCO)
