# -*- coding: utf-8 -*-
"""
AOP02 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Auto-verificacao dos scripts SQL SEM precisar de um servidor MySQL instalado.

Traduz o minimo necessario do DDL MySQL para SQLite, carrega os dados reais da
ANP, executa as 4 consultas do item II.d e confere:
  - os minimos do enunciado (5 postos, 4 combustiveis, >=2 bairros, >=5 datas)
  - que as restricoes realmente rejeitam dado invalido (CHECK, UNIQUE, FK, NOT NULL)
  - que cada consulta devolve linhas com as colunas exigidas

Isto e uma verificacao de logica, nao um substituto do MySQL: o entregavel final
roda em MySQL 8.0 / Workbench, onde ficam os prints.

    python scripts/validar.py
"""
import pathlib
import re
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SQL = RAIZ / "sql"


def para_sqlite(ddl):
    """Traducao minima do DDL MySQL para SQLite."""
    ddl = re.sub(r"^\s*(DROP DATABASE|CREATE DATABASE|USE)\b.*?;", "", ddl,
                 flags=re.S | re.M | re.I)
    ddl = re.sub(r"\)\s*ENGINE\s*=\s*InnoDB", ")", ddl, flags=re.I)
    # AUTO_INCREMENT no MySQL == INTEGER PRIMARY KEY (alias de rowid) no SQLite.
    ddl = re.sub(r"(\w+)\s+INT\s+NOT NULL AUTO_INCREMENT",
                 r"\1 INTEGER PRIMARY KEY", ddl, flags=re.I)
    ddl = re.sub(r"\s*CONSTRAINT \w+\s+PRIMARY KEY \(\w+\),", "", ddl, flags=re.I)
    return ddl


def carregar(con, caminho, traduzir=False):
    texto = caminho.read_text(encoding="utf-8")
    if traduzir:
        texto = para_sqlite(texto)
    else:
        # executescript ja gerencia a transacao; USE/COMMIT sao so do MySQL.
        texto = re.sub(r"^\s*(USE|COMMIT)\b.*?;", "", texto, flags=re.M | re.I)
    con.executescript(texto)


def consultas(caminho):
    """Separa o arquivo de consultas em comandos executaveis, descartando USE."""
    texto = re.sub(r"--[^\n]*", "", caminho.read_text(encoding="utf-8"))
    return [c.strip() for c in texto.split(";")
            if c.strip() and not c.strip().upper().startswith("USE")]


def rejeita(con, sql, rotulo):
    """A restricao precisa BARRAR este comando. Se passar, o schema esta frouxo."""
    try:
        con.execute(sql)
        con.rollback()
        raise AssertionError("restricao NAO barrou: " + rotulo)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        con.rollback()
        print("    ok  barrou: " + rotulo)


def main():
    con = sqlite3.connect(":memory:")
    con.create_function("regexp", 2, lambda p, v: v is not None and re.fullmatch(p, str(v)) is not None)
    con.execute("PRAGMA foreign_keys = ON")

    print("1. carregando 01-schema.sql e 02-dados.sql")
    carregar(con, SQL / "01-schema.sql", traduzir=True)
    carregar(con, SQL / "02-dados.sql")
    q = lambda s: con.execute(s).fetchall()

    print("2. conferindo os minimos do enunciado")
    n_postos = q("SELECT COUNT(*) FROM posto")[0][0]
    n_comb = q("SELECT COUNT(*) FROM combustivel")[0][0]
    n_bairros = q("SELECT COUNT(DISTINCT id_bairro) FROM posto")[0][0]
    n_coletas = q("SELECT COUNT(*) FROM coleta")[0][0]
    n_tels = q("SELECT COUNT(*) FROM telefone_posto")[0][0]
    datas = q("SELECT id_posto, COUNT(DISTINCT data_coleta) FROM coleta GROUP BY id_posto")
    print("    postos=%d  combustiveis=%d  bairros=%d  coletas=%d  telefones=%d"
          % (n_postos, n_comb, n_bairros, n_coletas, n_tels))
    print("    datas distintas por posto: " + str([d[1] for d in datas]))
    assert n_postos == 5, "II.a: exige 5 postos"
    assert n_comb == 4, "II.a: exige 4 combustiveis"
    assert n_bairros >= 2, "II.c: exige ao menos 2 bairros"
    assert len(datas) == 5 and all(d[1] >= 5 for d in datas), "II.b: exige >=5 datas por posto"
    assert n_tels > n_postos, "telefone multivalorado: algum posto precisa ter 2+ numeros"

    print("3. conferindo o atributo derivado Qtd_Amostras (view)")
    view = q("SELECT id_posto, qtd_amostras FROM vw_posto_amostras ORDER BY id_posto")
    real = q("SELECT id_posto, COUNT(*) FROM coleta GROUP BY id_posto ORDER BY id_posto")
    assert view == real, "a view divergiu do COUNT real: %s != %s" % (view, real)
    print("    ok  view bate com o COUNT em coleta: " + str([v[1] for v in view]))

    print("4. conferindo que as restricoes barram dado invalido")
    rejeita(con, "INSERT INTO coleta (id_posto,id_combustivel,data_coleta,valor)"
                 " VALUES (1,1,'2026-01-01',-1)", "CHECK valor > 0")
    rejeita(con, "INSERT INTO coleta (id_posto,id_combustivel,data_coleta,valor)"
                 " SELECT id_posto,id_combustivel,data_coleta,valor FROM coleta LIMIT 1",
            "UNIQUE (posto, combustivel, data)")
    rejeita(con, "INSERT INTO coleta (id_posto,id_combustivel,data_coleta,valor)"
                 " VALUES (999,1,'2026-01-01',5.5)", "FK coleta -> posto")
    rejeita(con, "INSERT INTO coleta (id_posto,id_combustivel,data_coleta,valor)"
                 " VALUES (1,1,'2026-01-01',NULL)", "NOT NULL valor")
    rejeita(con, "INSERT INTO combustivel (tipo) VALUES ('Gasolina')",
            "UNIQUE combustivel.tipo")
    rejeita(con, "INSERT INTO posto (cnpj,nome,rua,id_bairro)"
                 " VALUES ('abc','X','Y',1)", "CHECK cnpj com 14 digitos")

    print("5. executando as 4 consultas do item II.d")
    exigidas = [
        {"posto", "endereco", "bairro", "combustivel", "valor", "data_coleta"},
        {"posto", "bairro", "combustivel", "preco_medio", "qtd_amostras"},
        {"posto", "bairro", "combustivel", "valor", "data_coleta"},
        {"posto", "bairro", "combustivel", "valor", "data_coleta"},
    ]
    arquivos = sorted(SQL.glob("03-consulta-*.sql"))
    assert len(arquivos) == 4, "esperava 4 arquivos de consulta, achei " + str(len(arquivos))
    cmds = []
    for arq in arquivos:
        c = consultas(arq)
        assert len(c) == 1, arq.name + " deveria ter exatamente 1 consulta, tem " + str(len(c))
        cmds.append(c[0])
    for i, (cmd, campos) in enumerate(zip(cmds, exigidas), 1):
        cur = con.execute(cmd)
        linhas = cur.fetchall()
        cols = {d[0] for d in cur.description}
        assert linhas, "consulta %d nao retornou linhas" % i
        faltando = campos - cols
        assert not faltando, "consulta %d sem os campos exigidos: %s" % (i, faltando)
        print("    ok  consulta %d: %d linhas, colunas %s" % (i, len(linhas), sorted(cols)))

    # A consulta I precisa devolver exatamente 1 menor + 1 maior por combustivel.
    cur = con.execute(cmds[0])
    linhas = cur.fetchall()
    assert len(linhas) == 2 * n_comb, "consulta I deveria ter %d linhas, tem %d" % (2 * n_comb, len(linhas))
    # A consulta III precisa devolver uma linha por posto x combustivel.
    assert len(con.execute(cmds[2]).fetchall()) == n_postos * n_comb, "consulta III"
    # A consulta IV precisa vir ordenada por data.
    iv = con.execute(cmds[3]).fetchall()
    assert [r[4] for r in iv] == sorted(r[4] for r in iv), "consulta IV fora de ordem"
    print("    ok  cardinalidades e ordenacao das consultas conferem")

    print("6. executando 04-tabelas-povoadas.sql")
    povoadas = consultas(SQL / "04-tabelas-povoadas.sql")
    for cmd in povoadas:
        assert con.execute(cmd).fetchall(), "consulta sem linhas em 04-tabelas-povoadas.sql"
    print("    ok  " + str(len(povoadas)) + " consultas, todas com linhas")

    print("\nTUDO OK - schema, dados e consultas validados (" + str(n_coletas) + " coletas)")


if __name__ == "__main__":
    sys.exit(main())
