# -*- coding: utf-8 -*-
"""
AOP03 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Gera a planilha e os CSVs do item II.e a partir do banco do site.

O item II.e pede planilhas com os mesmos dados das consultas, acrescidas de dois
graficos de evolucao do preco medio. Por isso cada aba de consulta sai da
execucao literal do .sql correspondente, e os graficos sao objetos nativos do
Excel - abrem interativos, nao como imagem colada.

    python aop03/scripts/gerar_planilhas.py
"""
import csv
import pathlib
import re
import sqlite3

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = RAIZ / "aop03" / "site"
BANCO = SITE / "dados" / "banco.db"
CONSULTAS = SITE / "consultas"
SAIDA = SITE / "dados"

AUTOR = "Allan Spaviero Alpoim"
MATRICULA = "202636574"

AZUL = "1A3A6B"
CINZA = "F2F4F7"

# Ordem e rotulo das abas. A chave e o arquivo .sql executado para preenche-la.
ABAS = [
    ("03-consulta-1-menor-maior-preco.sql", "I - Menor e maior preco",
     "Consulta I (II.d.I) - menor e maior preco de cada tipo de combustivel"),
    ("03-consulta-2-media-e-amostras.sql", "II - Media e amostras",
     "Consulta II (II.d.II) - preco medio e quantidade de amostras por posto e combustivel"),
    ("03-consulta-3-preco-mais-recente.sql", "III - Preco mais recente",
     "Consulta III (II.d.III) - ultimo preco registrado em cada posto para cada combustivel"),
    ("03-consulta-4-evolucao-preco.sql", "IV - Evolucao no tempo",
     "Consulta IV (II.d.IV) - evolucao do preco de um combustivel em um posto especifico"),
]


def executar(con, arquivo):
    """Roda o .sql do projeto e devolve (colunas, linhas).

    USE e COMMIT sao sintaxe de sessao do MySQL e nao existem no SQLite; o
    restante da consulta e executado exatamente como esta no arquivo.
    """
    texto = (CONSULTAS / arquivo).read_text(encoding="utf-8")
    texto = re.sub(r"^\s*(USE|COMMIT)\b.*?;", "", texto, flags=re.M | re.I)
    cursor = con.execute(texto)
    return [d[0] for d in cursor.description], cursor.fetchall()


def escrever_aba(ws, titulo, colunas, linhas):
    """Escreve titulo, cabecalho e dados da consulta em uma aba."""
    ws.cell(1, 1, titulo).font = Font(bold=True, color=AZUL, size=12)
    inicio = 3

    for coluna, nome in enumerate(colunas, start=1):
        celula = ws.cell(inicio, coluna, nome.replace("_", " ").capitalize())
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", fgColor=AZUL)
        celula.alignment = Alignment(horizontal="center")

    for deslocamento, linha in enumerate(linhas, start=1):
        for coluna, valor in enumerate(linha, start=1):
            ws.cell(inicio + deslocamento, coluna, valor)

    for coluna, nome in enumerate(colunas, start=1):
        larguras = [len(nome)] + [len(str(linha[coluna - 1])) for linha in linhas]
        ws.column_dimensions[get_column_letter(coluna)].width = min(max(larguras) + 3, 42)

    ws.freeze_panes = ws.cell(inicio + 1, 1)


def pivotar(linhas, indice_chave, indice_serie, indice_valor):
    """Transforma linhas longas em tabela mes x serie, como o grafico precisa."""
    chaves, series, valores = [], [], {}
    for linha in linhas:
        chave, serie = linha[indice_chave], linha[indice_serie]
        if chave not in chaves:
            chaves.append(chave)
        if serie not in series:
            series.append(serie)
        valores[(chave, serie)] = linha[indice_valor]
    return chaves, series, valores


def bloco_de_grafico(ws, linha0, titulo, chaves, series, valores, ancora):
    """Escreve o bloco pivotado e ancora um grafico de linhas ao lado dele.

    Devolve a primeira linha livre depois do bloco.
    """
    ws.cell(linha0, 1, titulo).font = Font(bold=True, color=AZUL, size=12)
    cabecalho = linha0 + 1

    celula_mes = ws.cell(cabecalho, 1, "Mes")
    celula_mes.font = Font(bold=True)
    celula_mes.fill = PatternFill("solid", fgColor=CINZA)
    for coluna, serie in enumerate(series, start=2):
        celula = ws.cell(cabecalho, coluna, serie)
        celula.font = Font(bold=True)
        celula.fill = PatternFill("solid", fgColor=CINZA)
        largura = min(max(len(str(serie)) + 3, 12), 34)
        ws.column_dimensions[get_column_letter(coluna)].width = largura

    for deslocamento, chave in enumerate(chaves, start=1):
        ws.cell(cabecalho + deslocamento, 1, chave)
        for coluna, serie in enumerate(series, start=2):
            ws.cell(cabecalho + deslocamento, coluna, valores.get((chave, serie)))

    ultima = cabecalho + len(chaves)

    grafico = LineChart()
    grafico.title = titulo
    grafico.y_axis.title = "Preco medio (R$/litro)"
    grafico.x_axis.title = "Mes da coleta"
    grafico.height, grafico.width = 8, 17
    grafico.add_data(
        Reference(ws, min_col=2, max_col=1 + len(series),
                  min_row=cabecalho, max_row=ultima),
        titles_from_data=True,
    )
    grafico.set_categories(
        Reference(ws, min_col=1, min_row=cabecalho + 1, max_row=ultima))
    ws.add_chart(grafico, ancora)

    return ultima + 2


def aba_sobre(wb, periodo, total_coletas):
    """Capa da planilha, para quem abre o arquivo sem conhecer o projeto."""
    ws = wb.create_sheet("Sobre", 0)
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 82
    titulo = ws.cell(1, 1, "Precos de combustiveis em Vila Velha/ES")
    titulo.font = Font(bold=True, size=14, color=AZUL)

    informacoes = [
        ("Projeto", "Projeto de Extensao - Arquitetura de Dados Relacionais I - UVV"),
        ("Autor", f"{AUTOR} - matricula {MATRICULA}"),
        ("Municipio", "Vila Velha / ES"),
        ("Periodo coberto", periodo),
        ("Coletas de preco", total_coletas),
        ("Combustiveis", "Gasolina, Gasolina Aditivada, Etanol e Diesel"),
        ("Fonte dos dados", "Serie Historica de Precos de Combustiveis - ANP"),
        ("Endereco da fonte",
         "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
         "serie-historica-de-precos-de-combustiveis"),
        ("Como ler",
         "Cada aba traz o resultado de uma das consultas do banco de dados. "
         "As duas ultimas abas trazem os graficos de evolucao do preco medio."),
    ]
    for linha, (rotulo, valor) in enumerate(informacoes, start=3):
        ws.cell(linha, 1, rotulo).font = Font(bold=True)
        ws.cell(linha, 2, valor).alignment = Alignment(wrap_text=True, vertical="top")


def gravar_csv(destino, colunas, linhas):
    """CSV com ponto-e-virgula e BOM: e o que o Excel em portugues abre direito."""
    with destino.open("w", newline="", encoding="utf-8-sig") as saida:
        escritor = csv.writer(saida, delimiter=";")
        escritor.writerow(colunas)
        escritor.writerows(linhas)


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(BANCO)
    wb = Workbook()
    wb.remove(wb.active)

    resumo = []

    for numero, (arquivo, nome_aba, titulo) in enumerate(ABAS, start=1):
        colunas, linhas = executar(con, arquivo)
        escrever_aba(wb.create_sheet(nome_aba), titulo, colunas, linhas)
        destino = SAIDA / f"consulta-{numero}.csv"
        gravar_csv(destino, colunas, linhas)
        resumo.append((nome_aba, len(linhas), destino.name))

    # Grafico I (II.e.I): uma linha por combustivel ao longo dos meses.
    colunas, linhas = executar(con, "05-grafico-1-media-por-combustivel.sql")
    ws = wb.create_sheet("Grafico I - combustivel")
    chaves, series, valores = pivotar(linhas, 0, 1, 2)
    bloco_de_grafico(ws, 1, "Evolucao do preco medio de cada combustivel",
                     chaves, series, valores, "H2")
    destino = SAIDA / "grafico-1-media-por-combustivel.csv"
    gravar_csv(destino, colunas, linhas)
    resumo.append(("Grafico I - combustivel", len(linhas), destino.name))

    # Grafico II (II.e.II): um bloco e um grafico por combustivel, com uma linha
    # por posto. Vinte series num unico grafico seriam ilegiveis.
    colunas, linhas = executar(con, "05-grafico-2-media-por-combustivel-e-posto.sql")
    ws = wb.create_sheet("Grafico II - por posto")
    linha_atual = 1
    for combustivel in dict.fromkeys(linha[1] for linha in linhas):
        do_combustivel = [linha for linha in linhas if linha[1] == combustivel]
        chaves, series, valores = pivotar(do_combustivel, 0, 2, 4)
        bloco_de_grafico(ws, linha_atual,
                         f"Preco medio de {combustivel} em cada posto",
                         chaves, series, valores, f"H{linha_atual + 1}")
        linha_atual += 18  # espaco para o grafico ancorado ao lado do bloco
    destino = SAIDA / "grafico-2-media-por-combustivel-e-posto.csv"
    gravar_csv(destino, colunas, linhas)
    resumo.append(("Grafico II - por posto", len(linhas), destino.name))

    periodo = con.execute(
        "SELECT MIN(data_coleta) || ' a ' || MAX(data_coleta) FROM coleta").fetchone()[0]
    total = con.execute("SELECT COUNT(*) FROM coleta").fetchone()[0]
    aba_sobre(wb, periodo, total)
    con.close()

    destino = SAIDA / "precos-combustiveis-vila-velha.xlsx"
    wb.save(destino)

    print(f"planilha:  {destino.relative_to(RAIZ)}  ({destino.stat().st_size // 1024} KB)")
    for nome, total_linhas, nome_csv in resumo:
        print(f"  {nome:26} {total_linhas:>4} linhas   csv={nome_csv}")


if __name__ == "__main__":
    main()
