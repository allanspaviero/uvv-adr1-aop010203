# -*- coding: utf-8 -*-
"""
AOP02 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Le os CSVs da Serie Historica de Precos de Combustiveis da ANP (baixados por
baixar_anp.py), filtra o municipio de Vila Velha/ES, escolhe os 5 postos com
melhor cobertura e gera sql/02-dados.sql.

Criterios do enunciado atendidos pela selecao:
  II.a - 5 postos, 4 combustiveis (Gasolina, Gasolina Aditivada, Etanol, Diesel)
  II.b - no minimo 5 coletas por posto, em datas diferentes
  II.c - os postos cobrem no minimo 2 bairros da cidade
"""
import csv
import glob
import pathlib
import re
import sys
import unicodedata
from collections import defaultdict

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MUNICIPIO, UF = "VILA VELHA", "ES"
N_POSTOS = 5
MIN_DATAS = 5          # II.b
MIN_BAIRROS = 2        # II.c

# Produto na ANP -> tipo de combustivel exigido no enunciado.
# DIESEL S10 e o diesel efetivamente vendido na bomba e tem a maior cobertura
# na serie da ANP; e ele que representa o "Diesel" do requisito II.a.
PRODUTOS = {
    "GASOLINA": "Gasolina",
    "GASOLINA ADITIVADA": "Gasolina Aditivada",
    "ETANOL": "Etanol",
    "DIESEL S10": "Diesel",
}
TIPOS = ["Gasolina", "Gasolina Aditivada", "Etanol", "Diesel"]


def ler_csv(caminho):
    """Os arquivos da ANP alternam entre UTF-8 e Latin-1 conforme o mes."""
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(caminho, encoding=enc, newline="") as fh:
                linhas = list(csv.DictReader(fh, delimiter=";"))
            if linhas and "Municipio" in linhas[0]:
                return linhas
        except UnicodeDecodeError:
            continue
    raise SystemExit("nao consegui decodificar " + str(caminho))


def normalizar(texto):
    """Bairro vem grafado de formas diferentes entre os meses (acento, caixa,
    espaco duplo). Normaliza para uma chave unica."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip().upper()


def so_digitos(s):
    return re.sub(r"\D", "", s)


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "''")


def titulo(s):
    minusculas = {"de", "da", "do", "das", "dos", "e"}
    # A ANP repete o tipo do logradouro em alguns cadastros ("Rodovia Rodovia do Sol").
    texto = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", normalizar(s), flags=re.I)
    palavras = texto.lower().split()
    return " ".join(p if i and p in minusculas else p.capitalize()
                    for i, p in enumerate(palavras))


def carregar():
    arquivos = sorted(glob.glob(str(RAIZ / "dados" / "*.csv")))
    if not arquivos:
        raise SystemExit("nenhum CSV em dados/ - rode scripts/baixar_anp.py antes")
    postos, coletas = {}, {}
    for arq in arquivos:
        for r in ler_csv(arq):
            if r["Municipio"].strip().upper() != MUNICIPIO:
                continue
            if r["Estado - Sigla"].strip() != UF:
                continue
            tipo = PRODUTOS.get(r["Produto"].strip().upper())
            if not tipo:
                continue
            cnpj = so_digitos(r["CNPJ da Revenda"])
            if len(cnpj) != 14:
                continue
            # O cadastro do posto pode variar entre os meses; o ultimo visto vence.
            postos[cnpj] = {
                "cnpj": cnpj,
                "nome": r["Revenda"].strip(),
                "bandeira": r["Bandeira"].strip(),
                "rua": r["Nome da Rua"].strip(),
                "numero": r["Numero Rua"].strip(),
                "cep": so_digitos(r["Cep"]),
                "bairro": r["Bairro"].strip(),
            }
            dia, mes, ano = r["Data da Coleta"].split("/")
            data = ano + "-" + mes + "-" + dia
            valor = r["Valor de Venda"].strip().replace(",", ".")
            if not valor:
                continue
            # Dedup: o enunciado (e a UNIQUE da tabela) admite uma coleta por
            # posto/combustivel/data. Meses vizinhos podem repetir a mesma coleta.
            coletas.setdefault((cnpj, tipo, data), round(float(valor), 3))
    return postos, coletas


def escolher(postos, coletas):
    """Ranqueia por cobertura: so entra posto com >= MIN_DATAS datas distintas em
    TODOS os 4 combustiveis. Depois garante MIN_BAIRROS bairros distintos."""
    datas = defaultdict(lambda: defaultdict(set))
    for (cnpj, tipo, data) in coletas:
        datas[cnpj][tipo].add(data)

    aptos = []
    for cnpj, por_tipo in datas.items():
        if any(len(por_tipo.get(t, ())) < MIN_DATAS for t in TIPOS):
            continue
        aptos.append((sum(len(v) for v in por_tipo.values()), cnpj))
    aptos.sort(reverse=True)
    if len(aptos) < N_POSTOS:
        raise SystemExit(
            "so " + str(len(aptos)) + " postos de " + MUNICIPIO + " atendem "
            + str(MIN_DATAS) + " coletas em todos os 4 combustiveis - "
            "baixe mais meses em scripts/baixar_anp.py")

    escolhidos = [c for _, c in aptos[:N_POSTOS]]
    bairros = {normalizar(postos[c]["bairro"]) for c in escolhidos}
    if len(bairros) < MIN_BAIRROS:
        # Troca o ultimo colocado pelo melhor candidato de um bairro ainda ausente.
        for _, cnpj in aptos[N_POSTOS:]:
            if normalizar(postos[cnpj]["bairro"]) not in bairros:
                escolhidos[-1] = cnpj
                break
        else:
            raise SystemExit("nao ha bairros distintos suficientes entre os postos aptos")
    return escolhidos


def gerar_sql(postos, coletas, escolhidos):
    bairros, id_bairro = [], {}
    for cnpj in escolhidos:
        chave = normalizar(postos[cnpj]["bairro"])
        if chave not in id_bairro:
            id_bairro[chave] = len(bairros) + 1
            bairros.append((id_bairro[chave], titulo(chave)))

    periodo = sorted({d for (c, _, d) in coletas if c in escolhidos})

    L = [
        "-- =====================================================================",
        "-- AOP02 - Arquitetura de Dados Relacionais I - UVV",
        "-- Allan Spaviero Alpoim - matricula 202636574",
        "-- 02-dados.sql : carga de dados (DML)",
        "--",
        "-- FONTE DOS DADOS: Serie Historica de Precos de Combustiveis - ANP",
        "-- https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/",
        "--        serie-historica-de-precos-de-combustiveis",
        "-- Municipio: Vila Velha/ES   Periodo: " + periodo[0] + " a " + periodo[-1],
        "-- Arquivo gerado por scripts/gerar_dados.py - NAO EDITAR A MAO.",
        "-- =====================================================================",
        "",
        "USE precos_combustiveis;",
        "",
        "-- ---------- BAIRRO (II.c: os postos cobrem mais de um bairro) ----------",
        "INSERT INTO bairro (id_bairro, nome, cidade, uf) VALUES",
    ]
    L.append(",\n".join(
        "  (" + str(i) + ", '" + esc(n) + "', 'Vila Velha', 'ES')"
        for i, n in bairros) + ";")

    L += ["",
          "-- ---------- COMBUSTIVEL (II.a: os 4 tipos exigidos) ----------",
          "INSERT INTO combustivel (id_combustivel, tipo) VALUES"]
    L.append(",\n".join("  (" + str(i) + ", '" + t + "')"
                        for i, t in enumerate(TIPOS, 1)) + ";")

    L += ["",
          "-- ---------- POSTO (II.a: 5 postos) ----------",
          "INSERT INTO posto (id_posto, cnpj, nome, bandeira, rua, numero, cep, id_bairro) VALUES"]
    id_posto, linhas = {}, []
    for i, cnpj in enumerate(escolhidos, 1):
        p = postos[cnpj]
        id_posto[cnpj] = i
        if p["bandeira"] and normalizar(p["bandeira"]) != "BRANCA":
            bandeira = "'" + esc(titulo(p["bandeira"])) + "'"
        else:
            bandeira = "NULL"          # bandeira BRANCA = posto sem bandeira (atributo opcional)
        numero = "'" + esc(p["numero"]) + "'" if p["numero"] else "NULL"
        cep = "'" + p["cep"] + "'" if len(p["cep"]) == 8 else "NULL"
        linhas.append(
            "  (" + str(i) + ", '" + cnpj + "', '" + esc(titulo(p["nome"])) + "', "
            + bandeira + ", '" + esc(titulo(p["rua"])) + "', " + numero + ", "
            + cep + ", " + str(id_bairro[normalizar(p["bairro"])]) + ")")
    L.append(",\n".join(linhas) + ";")

    L += ["",
          "-- ---------- TELEFONE_POSTO (atributo multivalorado do MER) ----------",
          "-- A serie da ANP nao publica telefone. Os numeros abaixo sao ilustrativos",
          "-- e existem apenas para demonstrar o mapeamento do atributo multivalorado",
          "-- Telefone do projeto conceitual (AOP01) em tabela propria (1FN).",
          "INSERT INTO telefone_posto (id_posto, telefone) VALUES"]
    tels = []
    for i in range(1, len(escolhidos) + 1):
        tels.append("  (" + str(i) + ", '(27) 3200-" + format(1000 + i * 11, "04d") + "')")
        if i <= 2:   # dois postos com mais de um telefone: prova o multivalorado
            tels.append("  (" + str(i) + ", '(27) 99900-" + format(2000 + i * 11, "04d") + "')")
    L.append(",\n".join(tels) + ";")

    L += ["",
          "-- ---------- COLETA (II.b: >= 5 coletas por posto, em datas distintas) ----------",
          "INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor) VALUES"]
    id_comb = {t: i for i, t in enumerate(TIPOS, 1)}
    regs = sorted(((id_posto[c], id_comb[t], d, v)
                   for (c, t, d), v in coletas.items() if c in id_posto),
                  key=lambda r: (r[0], r[1], r[2]))
    L.append(",\n".join(
        "  (" + str(p) + ", " + str(cb) + ", '" + d + "', " + format(v, ".3f") + ")"
        for p, cb, d, v in regs) + ";")
    L += ["", "COMMIT;", ""]

    destino = RAIZ / "sql" / "02-dados.sql"
    destino.write_text("\n".join(L), encoding="utf-8")
    return destino, bairros, regs, periodo


def main():
    postos, coletas = carregar()
    escolhidos = escolher(postos, coletas)
    destino, bairros, regs, periodo = gerar_sql(postos, coletas, escolhidos)

    datas = defaultdict(set)
    for p, _, d, _ in regs:
        datas[p].add(d)

    print(str(destino.relative_to(RAIZ)) + " gerado")
    print("  periodo .... " + periodo[0] + " a " + periodo[-1])
    print("  bairros .... " + str(len(bairros)) + ": "
          + ", ".join(n for _, n in bairros))
    print("  postos ..... " + str(len(escolhidos)))
    print("  coletas .... " + str(len(regs)))
    for i, cnpj in enumerate(escolhidos, 1):
        print("    posto " + str(i) + ": " + str(len(datas[i])).rjust(3)
              + " datas | " + titulo(postos[cnpj]["nome"])[:38]
              + "  [" + titulo(postos[cnpj]["bairro"]) + "]")

    # Checagem dos minimos do enunciado - falha ruidosa se a selecao regredir.
    assert len(escolhidos) == N_POSTOS, "II.a: numero de postos"
    assert len(bairros) >= MIN_BAIRROS, "II.c: numero de bairros"
    assert all(len(v) >= MIN_DATAS for v in datas.values()), "II.b: coletas por posto"
    print("  OK - requisitos II.a, II.b e II.c atendidos")


if __name__ == "__main__":
    sys.exit(main())
