# -*- coding: utf-8 -*-
"""
AOP03 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Auto-verificacao da entrega: confere que o site tem tudo o que o enunciado pede.

Executa as seis consultas sobre o banco que o site consome e afirma, para cada
requisito, o numero de linhas e as colunas obrigatorias. Depois confere que a
planilha, os CSVs e os arquivos do site estao no lugar.

    python aop03/scripts/verificar.py

Sai com codigo 1 se qualquer verificacao falhar.
"""
import pathlib
import re
import sqlite3
import sys
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = RAIZ / "aop03" / "site"
BANCO = SITE / "dados" / "banco.db"
CONSULTAS = SITE / "consultas"

falhas = []


def conferir(condicao, descricao, detalhe=""):
    marca = "OK  " if condicao else "FALHA"
    print(f"  [{marca}] {descricao}{'   ' + detalhe if detalhe else ''}")
    if not condicao:
        falhas.append(descricao)


def executar(con, arquivo):
    texto = (CONSULTAS / arquivo).read_text(encoding="utf-8")
    texto = re.sub(r"^\s*(USE|COMMIT)\b[^;]*;", "", texto, flags=re.M | re.I)
    cursor = con.execute(texto)
    return [d[0] for d in cursor.description], cursor.fetchall()


# Por requisito: arquivo, linhas esperadas e as colunas que o enunciado exige.
REQUISITOS = [
    ("II.d.I", "03-consulta-1-menor-maior-preco.sql", 8,
     ["posto", "endereco", "bairro", "combustivel", "valor", "data_coleta"]),
    ("II.d.II", "03-consulta-2-media-e-amostras.sql", 20,
     ["posto", "bairro", "combustivel", "preco_medio", "qtd_amostras"]),
    ("II.d.III", "03-consulta-3-preco-mais-recente.sql", 20,
     ["posto", "bairro", "combustivel", "valor", "data_coleta"]),
    ("II.d.IV", "03-consulta-4-evolucao-preco.sql", 31,
     ["posto", "bairro", "combustivel", "valor", "data_coleta"]),
    ("II.e.I", "05-grafico-1-media-por-combustivel.sql", 32,
     ["mes", "combustivel", "preco_medio"]),
    ("II.e.II", "05-grafico-2-media-por-combustivel-e-posto.sql", 160,
     ["mes", "combustivel", "posto", "preco_medio"]),
]

ARQUIVOS_DO_SITE = [
    "index.html", "style.css", "app.js",
    "vendor/sql-wasm.js", "vendor/sql-wasm.wasm", "vendor/chart.umd.js",
    "dados/banco.db", "dados/precos-combustiveis-vila-velha.xlsx",
    "dados/consulta-1.csv", "dados/consulta-2.csv",
    "dados/consulta-3.csv", "dados/consulta-4.csv",
    "dados/grafico-1-media-por-combustivel.csv",
    "dados/grafico-2-media-por-combustivel-e-posto.csv",
]


def verificar_dados(con):
    print("\nDados minimos do enunciado")
    total = lambda tabela: con.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]

    conferir(total("posto") >= 5, "II.a - pelo menos 5 postos",
             f"{total('posto')} postos")
    conferir(total("combustivel") == 4, "II.a - os 4 tipos de combustivel",
             f"{total('combustivel')} tipos")
    conferir(total("bairro") >= 2, "II.c - postos em pelo menos 2 bairros",
             f"{total('bairro')} bairros")

    minimo_datas = con.execute(
        "SELECT MIN(datas) FROM (SELECT COUNT(DISTINCT data_coleta) AS datas "
        "FROM coleta GROUP BY id_posto)").fetchone()[0]
    conferir(minimo_datas >= 5, "II.b - >= 5 coletas por posto, em datas distintas",
             f"minimo de {minimo_datas} datas por posto")


def verificar_consultas(con):
    print("\nConsultas exigidas")
    for requisito, arquivo, esperado, obrigatorias in REQUISITOS:
        colunas, linhas = executar(con, arquivo)
        conferir(len(linhas) == esperado,
                 f"{requisito} - {arquivo} devolve {esperado} linhas",
                 f"devolveu {len(linhas)}")
        faltando = [c for c in obrigatorias if c not in colunas]
        conferir(not faltando, f"{requisito} - traz as colunas exigidas",
                 f"faltando {faltando}" if faltando else "")


def verificar_consulta_4_parametrizavel(con):
    """O site troca o posto e o combustivel do WHERE da consulta IV.

    Se o formato do arquivo mudar e a substituicao deixar de casar, o site passa
    a mostrar sempre o mesmo posto sem avisar - por isso a verificacao aqui.
    """
    print("\nParametrizacao da consulta IV (o site reescreve o WHERE)")
    original = (CONSULTAS / "03-consulta-4-evolucao-preco.sql").read_text(encoding="utf-8")
    trocado = re.sub(r"(\bp\.id_posto\s*=\s*)\d+", r"\g<1>5", original, count=1)
    trocado = re.sub(r"(\bcb\.tipo\s*=\s*)'[^']*'", r"\g<1>'Etanol'", trocado, count=1)

    conferir(trocado != original, "o WHERE aceita a substituicao de posto e combustivel")
    conferir("p.id_posto        = c.id_posto" in trocado,
             "o JOIN por id_posto continua intacto apos a substituicao")

    limpo = re.sub(r"^\s*(USE|COMMIT)\b[^;]*;", "", trocado, flags=re.M | re.I)
    linhas = con.execute(limpo).fetchall()
    conferir(len(linhas) > 0 and all(l[0] == "Posto Perim Ltda" for l in linhas),
             "a consulta reescrita devolve o posto escolhido",
             f"{len(linhas)} linhas")
    conferir(all(l[2] == "Etanol" for l in linhas),
             "a consulta reescrita devolve o combustivel escolhido")


def verificar_arquivos():
    print("\nArquivos do site")
    for caminho in ARQUIVOS_DO_SITE:
        arquivo = SITE / caminho
        existe = arquivo.exists() and arquivo.stat().st_size > 0
        conferir(existe, f"{caminho}",
                 f"{arquivo.stat().st_size // 1024} KB" if existe else "ausente")

    planilha = SITE / "dados" / "precos-combustiveis-vila-velha.xlsx"
    if planilha.exists():
        with zipfile.ZipFile(planilha) as pacote:
            nomes = pacote.namelist()
        graficos = [n for n in nomes if n.startswith("xl/charts/chart")]
        conferir(len(graficos) >= 2,
                 "II.e - a planilha embute os graficos como objetos do Excel",
                 f"{len(graficos)} graficos")


def main():
    if not BANCO.exists():
        print("banco.db nao existe. Rode antes: python aop03/scripts/gerar_banco.py")
        return 1

    print(f"Verificando a entrega em {SITE.relative_to(RAIZ)}")
    con = sqlite3.connect(BANCO)
    verificar_dados(con)
    verificar_consultas(con)
    verificar_consulta_4_parametrizavel(con)
    con.close()
    verificar_arquivos()

    print()
    if falhas:
        print(f"{len(falhas)} verificacao(oes) falharam:")
        for falha in falhas:
            print(f"  - {falha}")
        return 1
    print("Tudo certo: o site atende aos itens II.a, II.b, II.c, II.d e II.e.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
