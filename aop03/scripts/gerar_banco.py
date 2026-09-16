# -*- coding: utf-8 -*-
"""
AOP03 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Monta o banco SQLite que o site consome e copia as consultas para dentro dele.

O site nao reimplementa consulta nenhuma: ele le os proprios arquivos .sql do
projeto fisico e os executa no navegador via sql.js. Este script existe apenas
para transformar o schema e a carga do MySQL (AOP02) em um arquivo .db estatico,
que o navegador consegue abrir sem servidor.

A traducao MySQL -> SQLite nao e reescrita aqui: reaproveita para_sqlite() e
carregar() de aop02/scripts/validar.py, que ja estao testados.

    python aop03/scripts/gerar_banco.py
"""
import pathlib
import re
import shutil
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AOP02 = RAIZ / "aop02"
AOP03 = RAIZ / "aop03"
SITE = AOP03 / "site"

sys.path.insert(0, str(AOP02 / "scripts"))
import validar  # noqa: E402  (o sys.path precisa vir antes)

BANCO = SITE / "dados" / "banco.db"
DESTINO_SQL = SITE / "consultas"


def construir_banco():
    """Cria banco.db a partir do DDL e da carga do projeto fisico."""
    BANCO.parent.mkdir(parents=True, exist_ok=True)
    BANCO.unlink(missing_ok=True)

    con = sqlite3.connect(BANCO)
    # O SQLite nao traz o operador REGEXP, usado pelos CHECK do schema MySQL.
    # Registrar aqui garante que as restricoes sejam de fato validadas na carga;
    # o navegador recebe o banco ja pronto e so executa SELECT.
    con.create_function(
        "regexp", 2,
        lambda padrao, valor: valor is not None
        and re.fullmatch(padrao, str(valor)) is not None,
    )
    con.execute("PRAGMA foreign_keys = ON")

    validar.carregar(con, AOP02 / "sql" / "01-schema.sql", traduzir=True)
    validar.carregar(con, AOP02 / "sql" / "02-dados.sql")
    con.commit()

    contagens = {
        tabela: con.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
        for tabela in ("bairro", "posto", "telefone_posto", "combustivel", "coleta")
    }
    con.close()
    return contagens


def copiar_consultas():
    """Leva os .sql para dentro do site, sem alterar uma linha sequer.

    E o mesmo arquivo que o usuario ve ao clicar em 'ver a consulta SQL' e o
    mesmo que o sql.js executa - por isso a copia e literal.
    """
    DESTINO_SQL.mkdir(parents=True, exist_ok=True)
    origens = sorted((AOP02 / "sql").glob("03-consulta-*.sql"))
    origens += sorted((AOP03 / "sql").glob("05-grafico-*.sql"))
    for origem in origens:
        shutil.copy2(origem, DESTINO_SQL / origem.name)
    return [o.name for o in origens]


def main():
    contagens = construir_banco()
    copiados = copiar_consultas()

    print(f"banco:     {BANCO.relative_to(RAIZ)}  ({BANCO.stat().st_size // 1024} KB)")
    for tabela, total in contagens.items():
        print(f"  {tabela:16} {total:>4} linhas")
    print(f"consultas: {len(copiados)} arquivos em {DESTINO_SQL.relative_to(RAIZ)}")
    for nome in copiados:
        print(f"  {nome}")


if __name__ == "__main__":
    main()
