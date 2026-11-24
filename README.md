## 📌 Sobre o Projeto

O **Mike na Trilha do Saber** é um projeto acadêmico desenvolvido como parte da disciplina **Laboratório de Inovação IV**, do curso de **Análise e Desenvolvimento de Sistemas**, na instituição **Faculdade Senac DF**.

O projeto tem como objetivo oferecer uma plataforma web educacional gratuita para o aprendizado de inglês, buscando tornar o estudo mais acessível, organizado e motivador por meio de testes de nível, planos de estudo personalizados, acompanhamento do progresso, gamificação e o suporte do Mike, mascote e assistente virtual.

## 🎯 Objetivos

### Objetivo Geral

- Desenvolver uma plataforma web gratuita que ajude pessoas a aprender inglês de forma acessível, organizada e motivadora.

### Objetivos Específicos

- Identificar o nível de inglês do estudante (A1 a C1) por meio de um teste de nível.
- Gerar planos de estudo adaptados ao nível e à disponibilidade (dias por semana e minutos por dia) de cada usuário.
- Oferecer atividades de vocabulário, gramática e escrita, com explicações após cada resposta.
- Permitir o acompanhamento do desempenho e da evolução do estudante.
- Incentivar a continuidade dos estudos com XP, sequência de dias e conquistas.
- Disponibilizar o Mike, assistente virtual que responde dúvidas sobre inglês.

## ⚙️ Funcionalidades

- Cadastro e login com senha protegida (hash) e controle de acesso às páginas.
- Teste de nível com 20 questões e resultado de A1 a C1.
- Plano de estudos personalizado, com atividades distribuídas pelos dias da semana.
- Atividades de vocabulário, gramática e escrita, com XP e explicações.
- Acompanhamento do progresso: visão geral, habilidades e histórico.
- Gamificação: XP, sequência de dias estudados e 11 conquistas.
- Mike, assistente virtual com dicas de inglês (respostas por regras, sem IA externa nesta versão).

## 🛠️ Tecnologias Utilizadas

- **Linguagens:** HTML, CSS, JavaScript e Python.
- **Frameworks e bibliotecas:** Flask.
- **Banco de dados:** SQLite.
- **Ferramentas:** Visual Studio Code, Git, GitHub, GitHub Pages, PythonAnywhere e Microsoft Loop.

## 📁 Estrutura do Projeto

```text
laboratorio-de-inovacao-iv/
│
├── app.py                 # Flask: rotas do sistema
├── banco.py               # Conexão e comandos do SQLite
├── conteudo.py            # Questões, atividades, conquistas e dicas do Mike
├── testar_fluxo.py        # Teste automático do sistema
├── requirements.txt       # Dependências (Flask)
│
├── templates/             # Páginas HTML
├── static/
│   ├── css/style.css      # Estilos
│   ├── js/script.js       # JavaScript
│   └── img/               # Logos e imagens do Mike
│
├── docs/                  # Página de apresentação (GitHub Pages)
├── README.md
└── .gitignore
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.10 ou superior.
- Visual Studio Code (recomendado).
- Flask (instalado pelo `requirements.txt`).

### Instalação

1. Clone este repositório:

```bash
git clone https://github.com/amandasjsantos/mike-na-trilha-do-saber.git
```

2. Acesse a pasta do projeto:

```bash
cd mike-na-trilha-do-saber
```

3. Crie e ative o ambiente virtual (Windows) e instale as dependências:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python app.py
```

5. Abra no navegador: http://127.0.0.1:5000

## 🖥️ Demonstração

- GitHub Pages (apresentação): https://amandasjsantos.github.io/mike-na-trilha-do-saber/
- Sistema completo (PythonAnywhere): https://amandasjsantos.pythonanywhere.com

## 📋 Documentação

A documentação do projeto (planejamento, MVP, especificação técnica e protótipos) está no Microsoft Loop.

## 👥 Equipe de Desenvolvimento

| Integrante | Responsabilidade |
|---|---|
| Amanda Santos de Jesus | Liderança, documentação, front-end, back-end, banco de dados, publicação e apresentação |

## 🎓 Informações Acadêmicas

| Informação | Descrição |
|---|---|
| Instituição | Faculdade Senac DF |
| Curso | Análise e Desenvolvimento de Sistemas |
| Disciplina | Laboratório de Inovação IV |
| Professor(a) | Maristela Nunes de Oliveira |
| Período | 4º Semestre |
| Ano | 2026 |

## 📌 Status do Projeto

Versão inicial (MVP) concluída. Próximas etapas: integração do Mike com inteligência artificial e ampliação dos conteúdos.

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.

---

Desenvolvido por **Amanda Santos de Jesus**.

**Faculdade Senac DF — 2026**
