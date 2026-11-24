const formTeste = document.getElementById("form-teste");
if (formTeste) {
  const questoes = formTeste.querySelectorAll(".questao");
  const btnAnterior = document.getElementById("btn-anterior");
  const btnProxima = document.getElementById("btn-proxima");
  const btnFinalizar = document.getElementById("btn-finalizar");
  const contador = document.getElementById("contador");
  const barra = document.getElementById("barra-teste");
  let atual = 0;

  function mostrarQuestao(indice) {
    atual = indice;
    questoes.forEach((q, i) => q.classList.toggle("ativa", i === atual));
    contador.textContent = `${atual + 1}/${questoes.length}`;
    barra.style.width = `${(atual / questoes.length) * 100}%`;
    btnAnterior.disabled = atual === 0;
    atualizarBotoes();
  }

  function atualizarBotoes() {
    const respondida = questoes[atual].querySelector("input:checked") !== null;
    const ultima = atual === questoes.length - 1;
    btnProxima.hidden = ultima;
    btnFinalizar.hidden = !ultima;
    btnProxima.disabled = !respondida;
    btnFinalizar.disabled = !respondida;
  }

  btnProxima.addEventListener("click", () => mostrarQuestao(atual + 1));
  btnAnterior.addEventListener("click", () => mostrarQuestao(atual - 1));
  formTeste.addEventListener("change", atualizarBotoes); // marcou uma alternativa
  mostrarQuestao(0);
}

document.querySelectorAll(".aba-botao").forEach((botao) => {
  botao.addEventListener("click", () => {
    document
      .querySelectorAll(".aba-botao")
      .forEach((b) => b.classList.toggle("ativo", b === botao));
    document
      .querySelectorAll(".aba")
      .forEach((aba) =>
        aba.classList.toggle("ativa", aba.id === "aba-" + botao.dataset.aba),
      ); // data-aba="geral"
  });
});

const formChat = document.getElementById("form-chat");
if (formChat) {
  const areaMensagens = document.getElementById("mensagens");
  const campo = document.getElementById("texto-chat");
  const botaoEnviar = formChat.querySelector("button");
  const tokenCsrf = document.querySelector('meta[name="csrf-token"]').content;

  function adicionarBolha(texto, classe) {
    const bolha = document.createElement("div");
    bolha.className = "bolha " + classe;
    bolha.textContent = texto;
    if (classe === "bolha-mike") {
      const linha = document.createElement("div");
      linha.className = "linha-mike";
      const avatar = document.createElement("img");
      avatar.className = "avatar-mike";
      avatar.src = areaMensagens.dataset.avatar;
      avatar.alt = "Mike";
      linha.appendChild(avatar);
      linha.appendChild(bolha);
      areaMensagens.appendChild(linha);
    } else {
      areaMensagens.appendChild(bolha);
    }
    areaMensagens.scrollTop = areaMensagens.scrollHeight;
    return bolha;
  }

  areaMensagens.scrollTop = areaMensagens.scrollHeight;

  formChat.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const texto = campo.value.trim();
    if (!texto) return;

    adicionarBolha(texto, "bolha-aluno");
    campo.value = "";
    botaoEnviar.disabled = true;
    const digitando = adicionarBolha("Mike está digitando… 🐾", "bolha-mike");

    try {
      const resposta = await fetch("/mike/enviar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": tokenCsrf,
        },
        body: JSON.stringify({ texto: texto }),
      });
      const dados = await resposta.json();
      digitando.textContent = resposta.ok
        ? dados.resposta
        : dados.erro || "Algo deu errado.";
      if (dados.conquistas && dados.conquistas.length > 0) {
        adicionarBolha(
          "🏅 Nova conquista: " + dados.conquistas.join(", ") + "!",
          "bolha-mike",
        );
      }
    } catch (erro) {
      digitando.textContent = "Não consegui responder agora. Tente novamente.";
    }
    botaoEnviar.disabled = false;
    campo.focus();
  });
}
