"""Baixa os CSVs mensais de precos de revenda da ANP (serie historica de precos de combustiveis).

A ANP nao mantem um padrao unico de nome de arquivo entre os meses, entao tentamos
uma lista de padroes conhecidos para cada mes/grupo e ficamos com o primeiro que responder.
Fonte: https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis
"""
import urllib.request, urllib.parse, pathlib, sys

BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan"
ANO = "2026"
MESES = ["01", "02", "03", "04", "05", "06", "07", "08"]
GRUPOS = {"gasolina-etanol": "Gasolina Etanol", "diesel-gnv": "Diesel GNV"}
DEST = pathlib.Path(__file__).resolve().parent.parent / "dados"


def candidatos(mes, slug, titulo):
    return [
        f"{mes}-dados-abertos-precos-{ANO}-{mes}-{slug}.csv",
        f"{mes}-dados-abertos-precos-{slug}.csv",
        f"{mes}-Dados Abertos - Pre\u00e7os {ANO}.{mes} - {titulo}.csv",
        f"{mes}-cados-abertos-preco-{slug}.csv",  # typo real presente no acervo da ANP
        f"{mes}-dados-abertos-precos-{slug}",
    ]


def baixar(mes, slug, titulo):
    alvo = DEST / f"{ANO}-{mes}-{slug}.csv"
    if alvo.exists() and alvo.stat().st_size > 0:
        print(f"cache  {alvo.name}  {alvo.stat().st_size:,} bytes")
        return True
    for nome in candidatos(mes, slug, titulo):
        url = f"{BASE}/{ANO}/{urllib.parse.quote(nome)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                dados = r.read()
        except Exception:
            continue
        if not dados.startswith(b"\xef\xbb\xbfRegiao") and not dados.startswith(b"Regiao"):
            continue  # nao e o CSV esperado
        alvo.write_bytes(dados)
        print(f"ok     {alvo.name}  {len(dados):,} bytes  <- {nome}")
        return True
    print(f"FALHOU {ANO}-{mes} {slug}", file=sys.stderr)
    return False


if __name__ == "__main__":
    DEST.mkdir(exist_ok=True)
    for m in MESES:
        for slug, titulo in GRUPOS.items():
            baixar(m, slug, titulo)
