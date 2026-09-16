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
const MESES_POR_EXTENSO = ["janeiro", "fevereiro", "março", "abril", "maio",
                           "junho", "julho", "agosto", "setembro", "outubro",
                           "novembro", "dezembro"];

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

const dataPorExtenso = (iso) => {
    const [ano, mes, dia] = String(iso).split("-");
    return `${Number(dia)} de ${MESES_POR_EXTENSO[Number(mes) - 1]} de ${ano}`;
};

function formatar(coluna, valor) {
    if (valor === null || valor === undefined) return "—";
    if (coluna === "valor" || coluna === "preco_medio") return moeda(valor);
    if (coluna === "data_coleta") return dataBr(valor);
    if (coluna === "mes") return mesCurto(valor);
    return String(valor);
}

function cor(nome) {
    return getComputedStyle(document.documentElement).getPropertyValue(nome).trim();
}

/* ------------------------------------------------------------------ abas */

const abas = [...document.querySelectorAll(".abas a")];
const paineis = [...document.querySelectorAll(".painel")];

/**
 * Mostra um painel e esconde os demais.
 *
 * Os graficos precisam de um resize ao aparecer: o Chart.js mede o canvas no
 * momento de desenhar, e canvas dentro de painel escondido mede zero.
 */
function mostrarAba(id) {
    const alvo = paineis.some((painel) => painel.id === id) ? id : paineis[0].id;

    paineis.forEach((painel) => { painel.hidden = painel.id !== alvo; });
    abas.forEach((aba) => {
        if (aba.getAttribute("href") === `#${alvo}`) {
            aba.setAttribute("aria-current", "page");
        } else {
            aba.removeAttribute("aria-current");
        }
    });

    Object.values(graficos).forEach((grafico) => {
        if (grafico && !grafico.canvas.closest(".painel").hidden) grafico.resize();
    });

    // Se a pagina estiver rolada abaixo da barra de abas, volta para ela: o
    // painel novo comeca do topo, nao no meio.
    const barra = document.querySelector(".abas").offsetTop;
    if (window.scrollY > barra) window.scrollTo({ top: barra, behavior: "instant" });
}

function iniciarAbas() {
    abas.forEach((aba) => {
        aba.addEventListener("click", (evento) => {
            evento.preventDefault();
            const id = aba.getAttribute("href").slice(1);
            if (id !== location.hash.slice(1)) history.pushState(null, "", `#${id}`);
            mostrarAba(id);
        });
    });

    // popstate cobre voltar e avancar; hashchange cobre quem edita o endereco.
    const doEndereco = () => mostrarAba(location.hash.slice(1));
    window.addEventListener("popstate", doEndereco);
    window.addEventListener("hashchange", doEndereco);

    mostrarAba(location.hash.slice(1));
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
            if (destacar && destacar(coluna, linha)) celula.classList.add("menor");
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
    const cores = ["--serie-1", "--serie-2", "--serie-3", "--serie-4", "--serie-5"]
        .map(cor);
    const papel = cor("--papel");
    const tinta = cor("--tinta");
    const fraca = cor("--tinta-3");
    const linha = cor("--linha");
    const fonte = { family: "IBM Plex Sans", size: 12 };

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
                // Anel de 2px na cor do papel: mantem o ponto legivel onde duas
                // linhas se cruzam.
                pointBorderColor: papel,
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
                        font: fonte,
                        usePointStyle: true,
                        // Circulo, nao "line": a chave de linha seria desenhada com
                        // o pointBorderColor - que aqui e a cor do papel, por causa
                        // do anel dos pontos - e sumiria no fundo. O circulo usa o
                        // preenchimento, que e a cor da serie.
                        pointStyle: "circle",
                        boxWidth: 12,
                        boxHeight: 12,
                        padding: 16,
                    },
                },
                tooltip: {
                    backgroundColor: cor("--indigo"),
                    titleFont: fonte,
                    bodyFont: fonte,
                    padding: 10,
                    callbacks: {
                        label: (contexto) =>
                            `${contexto.dataset.label}: ${moeda(contexto.parsed.y)}`,
                    },
                },
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { color: cor("--filete") },
                    ticks: { color: fraca, font: { family: "IBM Plex Sans", size: 11 } },
                },
                y: {
                    grid: { color: linha, drawTicks: false },
                    border: { display: false },
                    ticks: {
                        color: fraca,
                        font: { family: "IBM Plex Sans", size: 11 },
                        callback: (valor) =>
                            "R$ " + Number(valor).toFixed(2).replace(".", ","),
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
        cartao.className = "preco";
        cartao.innerHTML =
            `<p class="preco__combustivel"></p>
             <p class="preco__valor"><small>R$</small><span></span></p>
             <p class="preco__posto"></p>
             <p class="preco__onde"></p>
             <p class="preco__quando"></p>`;
        cartao.querySelector(".preco__combustivel").textContent = linha.combustivel;
        cartao.querySelector(".preco__valor span").textContent =
            Number(linha.valor).toFixed(3).replace(".", ",");
        cartao.querySelector(".preco__posto").textContent = linha.posto;
        cartao.querySelector(".preco__onde").textContent =
            `${linha.endereco}, ${linha.bairro}`;
        cartao.querySelector(".preco__quando").textContent =
            `Coletado em ${dataBr(linha.data_coleta)}`;
        return cartao;
    }));
}

/* ------------------------------------------------------ consultas I a III */

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

/* ------------------------------------------------------------- seletores */

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

function preencherCapa() {
    const [resumo] = consultarObjetos(
        "SELECT MIN(c.data_coleta) AS inicio, MAX(c.data_coleta) AS fim, " +
        "COUNT(*) AS coletas, COUNT(DISTINCT c.id_posto) AS postos, " +
        "(SELECT COUNT(*) FROM bairro) AS bairros FROM coleta c");

    document.getElementById("capa-fatos").textContent =
        `${resumo.coletas} coletas de preço em ${resumo.postos} postos de ` +
        `${resumo.bairros} bairros, entre ${dataPorExtenso(resumo.inicio)} e ` +
        `${dataPorExtenso(resumo.fim)}, a partir da Série Histórica de Preços da ANP.`;

    document.getElementById("sobre-periodo").textContent =
        `${dataBr(resumo.inicio)} a ${dataBr(resumo.fim)}`;
}

/* ------------------------------------------------------------------ carga */

function avisarFalha(erro) {
    const aviso = document.createElement("p");
    aviso.className = "estado estado--erro";
    aviso.textContent =
        "Não foi possível abrir o banco de dados. Se você abriu este arquivo " +
        "direto do disco, o navegador bloqueia essa leitura: sirva a pasta por " +
        "HTTP (por exemplo, python -m http.server) ou acesse a versão publicada.";
    document.getElementById("cartoes-destaque").replaceChildren(aviso);
    document.getElementById("capa-fatos").textContent =
        "Os dados não puderam ser carregados.";
    console.error(erro);
}

async function iniciar() {
    iniciarAbas();

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

        preencherCapa();
        preencherSeletores();
        renderizarDestaques();
        renderizarConsultasFixas();
        renderizarConsulta4();
        renderizarGrafico1();
        renderizarGrafico2();

        // Os graficos nasceram com os paineis escondidos, onde o canvas mede
        // zero; refaz a medida do painel que esta visivel agora.
        mostrarAba(location.hash.slice(1));
    } catch (erro) {
        avisarFalha(erro);
    }
}

iniciar();
