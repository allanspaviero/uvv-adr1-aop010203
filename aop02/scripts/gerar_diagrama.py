# -*- coding: utf-8 -*-
"""
AOP02 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Gera docs/modelo-logico.drawio: o diagrama do modelo relacional (3FN) em
draw.io, como PLANO B caso o Reverse Engineer do MySQL Workbench nao esteja
disponivel. O diagrama oficial da entrega deve ser o EER do Workbench.

    python scripts/gerar_diagrama.py
"""
import pathlib
import xml.sax.saxutils as x

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# (tabela, x, y, [(coluna, marca)]) - marca: PK, FK, PK/FK, U (unique) ou ''
TABELAS = [
    ("bairro", 40, 40, [
        ("id_bairro INT AUTO_INCREMENT", "PK"),
        ("nome VARCHAR(60) NOT NULL", "U"),
        ("cidade VARCHAR(60) NOT NULL", "U"),
        ("uf CHAR(2) NOT NULL", "U"),
    ]),
    ("posto", 40, 240, [
        ("id_posto INT AUTO_INCREMENT", "PK"),
        ("cnpj CHAR(14) NOT NULL", "U"),
        ("nome VARCHAR(120) NOT NULL", ""),
        ("bandeira VARCHAR(60) NULL", ""),
        ("rua VARCHAR(120) NOT NULL", ""),
        ("numero VARCHAR(15) NULL", ""),
        ("cep CHAR(8) NULL", ""),
        ("id_bairro INT NOT NULL", "FK"),
    ]),
    ("telefone_posto", 40, 540, [
        ("id_posto INT NOT NULL", "PK/FK"),
        ("telefone VARCHAR(20) NOT NULL", "PK"),
    ]),
    ("combustivel", 560, 40, [
        ("id_combustivel INT AUTO_INCREMENT", "PK"),
        ("tipo VARCHAR(30) NOT NULL", "U"),
    ]),
    ("coleta", 560, 240, [
        ("id_coleta INT AUTO_INCREMENT", "PK"),
        ("id_posto INT NOT NULL", "FK/U"),
        ("id_combustivel INT NOT NULL", "FK/U"),
        ("data_coleta DATE NOT NULL", "U"),
        ("valor DECIMAL(6,3) NOT NULL", ""),
    ]),
]

# (origem, destino, rotulo) - o lado N aponta para o lado 1
RELACOES = [
    ("posto", "bairro", "N:1  fk_posto_bairro"),
    ("telefone_posto", "posto", "N:1  fk_telefone_posto"),
    ("coleta", "posto", "N:1  fk_coleta_posto"),
    ("coleta", "combustivel", "N:1  fk_coleta_combustivel"),
]

L_LINHA, L_TITULO, LARGURA = 26, 30, 300
CAB = ("swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;"
       "horizontalStack=0;resizeParent=1;resizeParentMax=0;html=1;"
       "fillColor=#dae8fc;strokeColor=#6c8ebf;")
LINHA = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
         "spacingLeft=6;spacingRight=6;overflow=hidden;points=[[0,0.5],[1,0.5]];"
         "portConstraint=eastwest;html=1;")
ARESTA = ("edgeStyle=entityRelationEdgeStyle;html=1;rounded=0;exitX=1;exitY=0.5;"
          "entryX=1;entryY=0.5;endArrow=ERmandOne;startArrow=ERoneToMany;")


def main():
    c = ['<mxfile host="app.diagrams.net">',
         '  <diagram name="Modelo Logico - 3FN" id="aop02">',
         '    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" page="1" '
         'pageWidth="1100" pageHeight="900" math="0" shadow="0">',
         '      <root><mxCell id="0"/><mxCell id="1" parent="0"/>']

    def cell(cid, valor, estilo, px, py, w, h, pai="1"):
        c.append('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
                 % (cid, x.escape(valor, {'"': "&quot;"}), estilo, pai))
        c.append('          <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/>'
                 % (px, py, w, h))
        c.append('        </mxCell>')

    for nome, px, py, colunas in TABELAS:
        altura = L_TITULO + L_LINHA * len(colunas)
        cell(nome, nome.upper(), CAB, px, py, LARGURA, altura)
        for i, (col, marca) in enumerate(colunas):
            rotulo = ("[%s] %s" % (marca, col)) if marca else col
            estilo = LINHA + ("fontStyle=1;" if "PK" in marca else "")
            cell("%s_%d" % (nome, i), rotulo, estilo, 0, L_TITULO + L_LINHA * i,
                 LARGURA, L_LINHA, nome)

    for i, (orig, dest, rotulo) in enumerate(RELACOES):
        c.append('        <mxCell id="rel%d" value="%s" style="%s" edge="1" '
                 'parent="1" source="%s" target="%s">'
                 % (i, x.escape(rotulo), ARESTA, orig, dest))
        c.append('          <mxGeometry relative="1" as="geometry"/>')
        c.append('        </mxCell>')

    nota = ("AOP02 - Modelo Logico Relacional (3FN)\\n"
            "Allan Spaviero Alpoim - 202636574\\n\\n"
            "PK = chave primaria   FK = chave estrangeira   U = UNIQUE\\n"
            "Qtd_Amostras (derivado do MER) = view vw_posto_amostras\\n"
            "Telefone (multivalorado do MER) = tabela telefone_posto")
    cell("nota", nota,
         "shape=note;whiteSpace=wrap;html=1;align=left;spacingLeft=10;"
         "fillColor=#fff2cc;strokeColor=#d6b656;verticalAlign=top;",
         560, 470, 300, 160)

    c += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>', '']
    destino = RAIZ / "docs" / "modelo-logico.drawio"
    destino.write_text("\n".join(c), encoding="utf-8")

    # Sanidade: o XML precisa ser parseavel e ter uma caixa por tabela.
    import xml.etree.ElementTree as ET
    raiz = ET.parse(destino).getroot()
    caixas = [e for e in raiz.iter("mxCell") if e.get("style", "").startswith("swimlane")]
    assert len(caixas) == len(TABELAS), "esperava %d tabelas, gerei %d" % (len(TABELAS), len(caixas))
    print(str(destino.relative_to(RAIZ)) + " gerado - "
          + str(len(TABELAS)) + " tabelas, " + str(len(RELACOES)) + " relacionamentos")


if __name__ == "__main__":
    main()
