import os
import sqlite3
from datetime import datetime, timezone, timedelta
import conteudo

PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DO_BANCO = os.path.join(PASTA_DO_PROJETO, "mike.db")

def agora():
    return datetime.now(timezone(timedelta(hours=-3)))

def agora_texto():
    return agora().strftime("%Y-%m-%d %H:%M:%S")

def conectar():
    conexao = sqlite3.connect(CAMINHO_DO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def consultar(sql, parametros=(), um=False):
    conexao = conectar()
    try:
        cursor = conexao.execute(sql, parametros)
        return cursor.fetchone() if um else cursor.fetchall()
    finally:
        conexao.close()

def executar(sql, parametros=()):
    conexao = conectar()
    try:
        cursor = conexao.execute(sql, parametros)
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()

def executar_varios(comandos):
    conexao = conectar()
    try:
        for sql, parametros in comandos:
            conexao.execute(sql, parametros)
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    senha_hash     TEXT NOT NULL,
    nivel_atual    TEXT,
    xp_total       INTEGER NOT NULL DEFAULT 0,
    data_cadastro  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado   TEXT NOT NULL,
    opcoes      TEXT NOT NULL,
    resposta    TEXT NOT NULL,
    nivel       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS testes_nivel (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id      INTEGER NOT NULL,
    pontuacao       INTEGER NOT NULL,
    nivel_resultado TEXT NOT NULL,
    data            TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS atividades (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo       TEXT NOT NULL,
    tipo         TEXT NOT NULL,
    nivel        TEXT NOT NULL,
    enunciado    TEXT NOT NULL,
    opcoes       TEXT NOT NULL,
    resposta     TEXT NOT NULL,
    explicacao   TEXT NOT NULL,
    xp           INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS planos_estudo (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id       INTEGER NOT NULL,
    nivel            TEXT NOT NULL,
    dias_por_semana  INTEGER NOT NULL,
    minutos_por_dia  INTEGER NOT NULL,
    ativo            INTEGER NOT NULL DEFAULT 1,
    data_criacao     TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS plano_itens (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    plano_id      INTEGER NOT NULL,
    atividade_id  INTEGER NOT NULL,
    dia_semana    INTEGER NOT NULL,
    FOREIGN KEY (plano_id) REFERENCES planos_estudo (id),
    FOREIGN KEY (atividade_id) REFERENCES atividades (id)
);

CREATE TABLE IF NOT EXISTS progresso (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id        INTEGER NOT NULL,
    atividade_id      INTEGER NOT NULL,
    plano_item_id     INTEGER NOT NULL,
    resposta_usuario  TEXT NOT NULL,
    acertou           INTEGER NOT NULL,
    xp_ganho          INTEGER NOT NULL,
    data              TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (atividade_id) REFERENCES atividades (id),
    FOREIGN KEY (plano_item_id) REFERENCES plano_itens (id)
);

CREATE TABLE IF NOT EXISTS conquistas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo     TEXT NOT NULL UNIQUE,
    nome       TEXT NOT NULL,
    descricao  TEXT NOT NULL,
    icone      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario_conquistas (
    usuario_id    INTEGER NOT NULL,
    conquista_id  INTEGER NOT NULL,
    data          TEXT NOT NULL,
    PRIMARY KEY (usuario_id, conquista_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (conquista_id) REFERENCES conquistas (id)
);

CREATE TABLE IF NOT EXISTS mensagens_mike (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id  INTEGER NOT NULL,
    autor       TEXT NOT NULL,
    texto       TEXT NOT NULL,
    data        TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS base_mike (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    palavras_chave  TEXT NOT NULL,
    resposta        TEXT NOT NULL
);
"""

def iniciar_banco():
    conexao = conectar()
    try:
        conexao.executescript(ESQUEMA)

        def vazia(tabela):
            return conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0] == 0

        if vazia("questoes"):
            conexao.executemany(
                "INSERT INTO questoes (enunciado, opcoes, resposta, nivel) VALUES (?, ?, ?, ?)",
                conteudo.QUESTOES)

        if vazia("atividades"):
            for nivel, tipo, titulo, enunciado, opcoes, resposta, explicacao in conteudo.ATIVIDADES:
                conexao.execute(
                    "INSERT INTO atividades (titulo, tipo, nivel, enunciado, opcoes, resposta, explicacao, xp) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (titulo, tipo, nivel, enunciado, opcoes, resposta, explicacao, conteudo.XP_POR_NIVEL[nivel]))

        if vazia("conquistas"):
            conexao.executemany(
                "INSERT INTO conquistas (codigo, nome, descricao, icone) VALUES (?, ?, ?, ?)",
                conteudo.CONQUISTAS)

        if vazia("base_mike"):
            conexao.executemany(
                "INSERT INTO base_mike (palavras_chave, resposta) VALUES (?, ?)",
                conteudo.BASE_MIKE)

        conexao.commit()
    finally:
        conexao.close()

if __name__ == "__main__":
    iniciar_banco()
    print("Banco de dados pronto em:", CAMINHO_DO_BANCO)
