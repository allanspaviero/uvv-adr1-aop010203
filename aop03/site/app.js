/* =====================================================================
   AOP03 - Arquitetura de Dados Relacionais I - UVV
   Allan Spaviero Alpoim - matricula 202636574

   O site nao reimplementa nenhuma consulta. Ele abre o banco de dados no
   navegador (SQLite compilado para WebAssembly) e executa os mesmos arquivos
   .sql do projeto fisico - os mesmos que aparecem em "ver a consulta SQL".
   ===================================================================== */

"use strict";

const ARQUIVOS_SQL = {
    c1: "03-consulta-1-menor-maior-preco.sql",
    c2: "03-consulta-2-media-e-amostras.sql",
    c3: "03-consulta-3-preco-mais-recente.sql",
    c4: "03-consulta-4-evolucao-preco.sql",
    g1: "05-grafico-1-media-por-combustivel.sql",
    g2: "05-grafico-2-media-por-combustivel-e-posto.sql",
};

const ROTULOS = {
    combustivel: "Combustível",
    extremo: "",
    posto: "Posto",
    endereco: "Endereço",
    bairro: "Bairro",
    valor: "Preço",
    data_coleta: "Data da coleta",
    preco_medio: "Preço médio",
    qtd_amostras: "Amostras",
    mes: "Mês",
};

const COLUNAS_NUMERICAS = new Set(["valor", "preco_medio", "qtd_amostras"]);
const MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
               "jul", "ago", "set", "out", "nov", "dez"];

let banco = null;
let sql = {};          // texto de cada arquivo .sql, por chave
const graficos = {};   // instancias do Chart.js, por id do canvas

/* --------------------------------------------------------------- formato */

const moeda = (valor) =>
    "R$ " + Number(valor).toFixed(3).replace(".", ",");

const dataBr = (iso) => {
    const [ano, mes, dia] = String(iso).split("-");
    return `${dia}/${mes}/${ano}`;
};

const mesCurto = (iso) => {
    const [ano, mes] = String(iso).split("-");
    return `${MESES[Number(mes) - 1]}/${ano}`;
};

function formatar(coluna, valor) {
    if (valor === null || valor === undefined) return "—";
    if (coluna === "valor" || coluna === "preco_medio") return moeda(valor);
    if (coluna === "data_coleta") return dataBr(valor);
    if (coluna === "mes") return mesCurto(valor);
    return String(valor);
}

/* ------------------------------------------------------------ tema claro/escuro */

function temaAtual() {
    const marcado = document.documentElement.getAttribute("data-theme");
    if (marcado) return marcado;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function aplicarTema(tema) {
    document.documentElement.setAttribute("data-theme", tema);
    document.getElementById("botao-tema").textContent =
        tema === "dark" ? "Tema claro" : "Tema escuro";
    // A cor das linhas vem do CSS, entao os graficos precisam ser redesenhados.
    redesenharGraficos();
}

function iniciarTema() {
    let guardado = null;
    try {
        guardado = localStorage.getItem("tema");
    } catch (erro) {
        guardado = null;   // navegacao privada ou armazenamento bloqueado
    }
    if (guardado === "dark" || guardado === "light") {
        document.documentElement.setAttribute("data-theme", guardado);
    }
    const botao = document.getElementById("botao-tema");
    botao.textContent = temaAtual() === "dark" ? "Tema claro" : "Tema escuro";
    botao.addEventListener("click", () => {
        const novo = temaAtual() === "dark" ? "light" : "dark";
        try {
            localStorage.setItem("tema", novo);
        } catch (erro) {
            /* preferencia so vale para esta visita */
        }
        aplicarTema(novo);
    });
}

function cor(nome) {
    return getComputedStyle(document.documentElement).getPropertyValue(nome).trim();
}

function paleta() {
    return ["--serie-1", "--serie-2", "--serie-3", "--serie-4", "--serie-5"].map(cor);
}

/* ------------------------------------------------------------- consultas */

/** Remove o que so existe na sessao do MySQL e executa o resto sem tocar. */
function executar(texto) {
    const limpo = texto.replace(/^\s*(USE|COMMIT)\b[^;]*;/gim, "");
    const resultado = banco.exec(limpo);
    return resultado.length
        ? { colunas: resultado[0].columns, linhas: resultado[0].values }
        : { colunas: [], linhas: [] };
}

function consultarObjetos(texto) {
    const { colunas, linhas } = executar(texto);
    return linhas.map((linha) =>
        Object.fromEntries(colunas.map((coluna, i) => [coluna, linha[i]])));
}

/* --------------------------------------------------------------- tabelas */

function montarTabela(idTabela, colunas, linhas, destacar) {
    const tabela = document.getElementById(idTabela);
    const cabecalho = document.createElement("thead");
    const corpo = document.createElement("tbody");

    const linhaCabecalho = document.createElement("tr");
    colunas.forEach((coluna) => {
        const celula = document.createElement("th");
        celula.textContent = ROTULOS[coluna] ?? coluna;
        if (COLUNAS_NUMERICAS.has(coluna)) celula.className = "numero";
        linhaCabecalho.appendChild(celula);
    });
    cabecalho.appendChild(linhaCabecalho);

    linhas.forEach((linha) => {
        const tr = document.createElement("tr");
        colunas.forEach((coluna, i) => {
            const celula = document.createElement("td");
            celula.textContent = formatar(coluna, linha[i]);
            if (COLUNAS_NUMERICAS.has(coluna)) celula.className = "numero";
            if (destacar && destacar(coluna, linha)) celula.classList.add("destaque-menor");
            tr.appendChild(celula);
        });
        corpo.appendChild(tr);
    });

    tabela.replaceChildren(cabecalho, corpo);
}

function mostrarSql(idElemento, texto) {
    document.getElementById(idElemento).textContent = texto.trim();
}

/* -------------------------------------------------------------- graficos */

function desenharLinhas(idCanvas, rotulos, series, formatarRotulo = mesCurto) {
    const cores = paleta();
    const superficie = cor("--superficie");
    const tinta = cor("--tinta-2");
    const fraca = cor("--tinta-fraca");
    const grade = cor("--grade");

    if (graficos[idCanvas]) graficos[idCanvas].destroy();

    graficos[idCanvas] = new Chart(document.getElementById(idCanvas), {
        type: "line",
        data: {
            labels: rotulos.map(formatarRotulo),
            datasets: series.map((serie, i) => ({
                label: serie.nome,
                data: serie.valores,
                borderColor: cores[i % cores.length],
                backgroundColor: cores[i % cores.length],
                borderWidth: 2,
                borderCapStyle: "round",
                borderJoinStyle: "round",
                tension: 0,
                spanGaps: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointHitRadius: 14,
                // Anel de 2px na cor da superficie: mantem o ponto legivel onde
                // duas linhas se cruzam.
                pointBorderColor: superficie,
                pointBorderWidth: 2,
                pointBackgroundColor: cores[i % cores.length],
            })),
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: tinta,
                        usePointStyle: true,
                        // Circulo, nao "line": a chave de linha seria desenhada com
                        // o pointBorderColor - que aqui e a cor da superficie, por
                        // causa do anel dos pontos - e sumiria no fundo. O circulo
                        // usa o preenchimento, que e a cor da serie.
                        pointStyle: "circle",
                        boxWidth: 12,
                        boxHeight: 12,
                        padding: 16,
                    },
                },
                tooltip: {
                    callbacks: {
                        label: (contexto) =>
                            `${contexto.dataset.label}: ${moeda(contexto.parsed.y)}`,
                    },
                },
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { color: cor("--eixo") },
                    ticks: { color: fraca },
                },
                y: {
                    grid: { color: grade, drawTicks: false },
                    border: { display: false },
                    ticks: {
                        color: fraca,
                        callback: (valor) => "R$ " + Number(valor).toFixed(2).replace(".", ","),
                    },
                },
            },
        },
    });
}

/* ------------------------------------------------------------- destaques */

function renderizarDestaques() {
    const linhas = consultarObjetos(sql.c1).filter((l) => l.extremo === "MENOR PRECO");
    const container = document.getElementById("cartoes-destaque");
    container.replaceChildren(...linhas.map((linha) => {
        const cartao = document.createElement("div");
        cartao.className = "cartao";
        cartao.innerHTML =
            `<p class="cartao__combustivel"></p>
             <p class="cartao__preco"></p>
             <p class="cartao__posto"></p>
             <p class="cartao__local"></p>
             <p class="cartao__data"></p>`;
        cartao.querySelector(".cartao__combustivel").textContent = linha.combustivel;
        cartao.querySelector(".cartao__preco").textContent = moeda(linha.valor);
        cartao.querySelector(".cartao__posto").textContent = linha.posto;
        cartao.querySelector(".cartao__local").textContent =
            `${linha.endereco} — ${linha.bairro}`;
        cartao.querySelector(".cartao__data").textContent =
            `Coletado em ${dataBr(linha.data_coleta)}`;
        return cartao;
    }));
}

/* ------------------------------------------------------- consultas I a III */

function renderizarConsultasFixas() {
    const c1 = executar(sql.c1);
    montarTabela("tabela-1", c1.colunas, c1.linhas,
                 (coluna, linha) => coluna === "valor" && linha[1] === "MENOR PRECO");
    mostrarSql("sql-1", sql.c1);

    const c2 = executar(sql.c2);
    montarTabela("tabela-2", c2.colunas, c2.linhas);
    mostrarSql("sql-2", sql.c2);

    const c3 = executar(sql.c3);
    montarTabela("tabela-3", c3.colunas, c3.linhas);
    mostrarSql("sql-3", sql.c3);
}

/* ------------------------------------------------------------ consulta IV */

/**
 * Troca o posto e o combustivel do WHERE da consulta IV.
 *
 * O arquivo original fixa `p.id_posto = 1` e `cb.tipo = 'Gasolina'`; o site
 * substitui esses dois literais pela escolha do usuario e exibe o resultado da
 * substituicao, para que o SQL mostrado seja o SQL executado.
 */
function sqlConsulta4(idPosto, tipo) {
    return sql.c4
        .replace(/(\bp\.id_posto\s*=\s*)\d+/, `$1${Number(idPosto)}`)
        .replace(/(\bcb\.tipo\s*=\s*)'[^']*'/, `$1'${tipo.replace(/'/g, "''")}'`);
}

function renderizarConsulta4() {
    const idPosto = document.getElementById("seletor-posto").value;
    const tipo = document.getElementById("seletor-combustivel").value;
    const texto = sqlConsulta4(idPosto, tipo);
    const { colunas, linhas } = executar(texto);

    montarTabela("tabela-4", colunas, linhas);
    mostrarSql("sql-4", texto);

    const iData = colunas.indexOf("data_coleta");
    const iValor = colunas.indexOf("valor");
    desenharLinhas(
        "gr-evolucao",
        linhas.map((linha) => linha[iData]),
        [{ nome: tipo, valores: linhas.map((linha) => linha[iValor]) }],
        dataBr,   // a consulta IV plota coletas individuais, nao medias mensais
    );
}

/* -------------------------------------------------------------- graficos */

function renderizarGrafico1() {
    const linhas = consultarObjetos(sql.g1);
    const meses = [...new Set(linhas.map((l) => l.mes))].sort();
    const tipos = [...new Set(linhas.map((l) => l.combustivel))];
    const series = tipos.map((tipo) => ({
        nome: tipo,
        valores: meses.map((mes) => {
            const achado = linhas.find((l) => l.mes === mes && l.combustivel === tipo);
            return achado ? achado.preco_medio : null;
        }),
    }));
    desenharLinhas("gr-combustivel", meses, series);
    mostrarSql("sql-g1", sql.g1);
}

function renderizarGrafico2() {
    const tipo = document.getElementById("seletor-grafico-combustivel").value;
    const linhas = consultarObjetos(sql.g2).filter((l) => l.combustivel === tipo);
    const meses = [...new Set(linhas.map((l) => l.mes))].sort();
    const postos = [...new Set(linhas.map((l) => l.posto))];
    const series = postos.map((posto) => ({
        nome: posto,
        valores: meses.map((mes) => {
            const achado = linhas.find((l) => l.mes === mes && l.posto === posto);
            return achado ? achado.preco_medio : null;
        }),
    }));
    desenharLinhas("gr-posto", meses, series);
    mostrarSql("sql-g2", sql.g2);
}

function redesenharGraficos() {
    if (!banco) return;
    renderizarGrafico1();
    renderizarGrafico2();
    renderizarConsulta4();
}

/* --------------------------------------------------------------- seletores */

function preencherSeletores() {
    const postos = consultarObjetos(
        "SELECT p.id_posto, p.nome, b.nome AS bairro FROM posto p " +
        "INNER JOIN bairro b ON b.id_bairro = p.id_bairro ORDER BY p.nome");
    const combustiveis = consultarObjetos(
        "SELECT tipo FROM combustivel ORDER BY id_combustivel");

    const seletorPosto = document.getElementById("seletor-posto");
    seletorPosto.replaceChildren(...postos.map((posto) => {
        const opcao = document.createElement("option");
        opcao.value = posto.id_posto;
        opcao.textContent = `${posto.nome} — ${posto.bairro}`;
        return opcao;
    }));

    [document.getElementById("seletor-combustivel"),
     document.getElementById("seletor-grafico-combustivel")].forEach((seletor) => {
        seletor.replaceChildren(...combustiveis.map((item) => {
            const opcao = document.createElement("option");
            opcao.value = item.tipo;
            opcao.textContent = item.tipo;
            return opcao;
        }));
    });

    seletorPosto.addEventListener("change", renderizarConsulta4);
    document.getElementById("seletor-combustivel")
        .addEventListener("change", renderizarConsulta4);
    document.getElementById("seletor-grafico-combustivel")
        .addEventListener("change", renderizarGrafico2);
}

function preencherSelos() {
    const [{ inicio, fim, total }] = consultarObjetos(
        "SELECT MIN(data_coleta) AS inicio, MAX(data_coleta) AS fim, " +
        "COUNT(*) AS total FROM coleta");
    const periodo = `${dataBr(inicio)} a ${dataBr(fim)}`;
    document.getElementById("selo-periodo").textContent = `Período: ${periodo}`;
    document.getElementById("selo-coletas").textContent =
        `${total} coletas de preço`;
    document.getElementById("sobre-periodo").textContent = periodo;
}

/* ------------------------------------------------------------------ carga */

function avisarFalha(erro) {
    const aviso = document.createElement("p");
    aviso.className = "estado estado--erro";
    aviso.textContent =
        "Não foi possível carregar o banco de dados. Se você abriu este arquivo " +
        "direto do disco, o navegador bloqueia a leitura do banco: sirva a pasta " +
        "por HTTP (por exemplo, python -m http.server) ou acesse a versão publicada.";
    document.getElementById("cartoes-destaque").replaceChildren(aviso);
    console.error(erro);
}

async function iniciar() {
    iniciarTema();

    try {
        const [SQL, bytes, textos] = await Promise.all([
            initSqlJs({ locateFile: (arquivo) => `vendor/${arquivo}` }),
            fetch("dados/banco.db").then((resposta) => {
                if (!resposta.ok) throw new Error(`banco.db: HTTP ${resposta.status}`);
                return resposta.arrayBuffer();
            }),
            Promise.all(Object.entries(ARQUIVOS_SQL).map(([chave, nome]) =>
                fetch(`consultas/${nome}`).then((resposta) => {
                    if (!resposta.ok) throw new Error(`${nome}: HTTP ${resposta.status}`);
                    return resposta.text();
                }).then((texto) => [chave, texto]))),
        ]);

        banco = new SQL.Database(new Uint8Array(bytes));
        sql = Object.fromEntries(textos);

        preencherSelos();
        preencherSeletores();
        renderizarDestaques();
        renderizarConsultasFixas();
        renderizarConsulta4();
        renderizarGrafico1();
        renderizarGrafico2();
    } catch (erro) {
        avisarFalha(erro);
    }
}

iniciar();
