# -*- coding: utf-8 -*-
"""
AOP02 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Monta o PDF de entrega a partir dos prints da raiz do projeto, com a
contextualizacao de cada secao (exigencia do item III.d).

    python scripts/gerar_pdf.py
"""
import pathlib
import sys

from PIL import Image
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image as RLImage, KeepTogether, PageBreak,
                               Paragraph, SimpleDocTemplate, Spacer)

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "AOP02-AllanSpavieroAlpoim.pdf"

AUTOR = "Allan Spaviero Alpoim"
MATRICULA = "202636574"

MARGEM = 1.8 * cm
LARGURA_UTIL = A4[0] - 2 * MARGEM
ALTURA_MAX = 13.5 * cm     # deixa espaco para titulo + texto na mesma pagina
# As figuras usam largura um pouco menor que a do texto para que duas subsecoes
# caibam na mesma pagina. Nao ha perda de qualidade: os pixels embarcados sao os
# mesmos, a densidade sobe de ~280 para ~300 DPI.
LARGURA_FIG = 16.2 * cm

_ss = getSampleStyleSheet()

# Capa conforme ABNT NBR 14724:2011: elementos centralizados, fonte 12,
# entrelinha 1,5 - instituicao e autor no alto, titulo ao centro,
# local e ano de deposito ao pe da folha.
CAPA = ParagraphStyle("capa", parent=_ss["Normal"], fontName="Helvetica",
                      fontSize=12, leading=18, alignment=1)
CAPA_TIT = ParagraphStyle("capatit", parent=CAPA, fontName="Helvetica-Bold",
                          fontSize=14, leading=21)
H = ParagraphStyle("h", parent=_ss["Heading1"], fontSize=14, leading=18,
                   spaceBefore=6, spaceAfter=8, textColor="#1a3a6b",
                   keepWithNext=1)
H2 = ParagraphStyle("h2", parent=_ss["Heading2"], fontSize=11.5, leading=15,
                    spaceBefore=5, spaceAfter=4, textColor="#1a3a6b",
                    keepWithNext=1)
P = ParagraphStyle("p", parent=_ss["Normal"], fontSize=10, leading=13.8,
                   alignment=TA_JUSTIFY, spaceAfter=5)
LEG = ParagraphStyle("leg", parent=_ss["Normal"], fontSize=8.5, leading=11,
                     alignment=1, textColor="#555555", spaceBefore=3)


def figura(nome, legenda):
    """Insere o print reescalado para caber na pagina, com legenda."""
    caminho = RAIZ / nome
    if not caminho.exists():
        raise SystemExit("print nao encontrado: " + nome)
    larg_px, alt_px = Image.open(caminho).size
    escala = min(LARGURA_FIG / larg_px, ALTURA_MAX / alt_px)
    img = RLImage(str(caminho), width=larg_px * escala, height=alt_px * escala)
    img.hAlign = "CENTER"
    return [img, Paragraph(legenda, LEG)]


def agrupar_figura(s):
    """Prende a figura recem-inserida ao ultimo paragrafo que a explica.

    Sem isso, uma figura que nao cabe no resto da pagina desce sozinha e deixa
    um vao entre o texto e a imagem. Agrupar a secao inteira resolveria o vao,
    mas desperdicaria meia pagina a cada quebra; prender apenas o paragrafo
    final mantem texto e figura juntos sem inflar o documento.
    """
    fig = s[-2:]            # figura() devolve [imagem, legenda]
    texto = s[-3:-2]        # o paragrafo imediatamente anterior
    del s[-3:]
    # Se esse paragrafo for o unico da subsecao, o titulo tambem entra no bloco:
    # keepWithNext nao atravessa um KeepTogether e deixaria o titulo orfao no
    # pe da pagina, com a subsecao inteira na pagina seguinte.
    if s and getattr(s[-1], "style", None) is not None             and s[-1].style.name in ("h", "h2"):
        texto = s[-1:] + texto
        del s[-1:]
    # Um unico nivel de KeepTogether: aninhar um dentro do outro faz o reportlab
    # considerar o bloco maior que a pagina e empurrar tudo, inflando o documento.
    s.append(KeepTogether(texto + [Spacer(1, 0.08 * cm)] + fig))
    s.append(Spacer(1, 0.18 * cm))


def construir():
    s = []

    # ---------------- Capa (ABNT NBR 14724:2011) ----------------
    # Local e ano ocupam as duas ultimas linhas da folha; o espaco restante e
    # distribuido proporcionalmente entre os demais blocos da capa.
    ALTURA_UTIL = A4[1] - 1.3 * cm - 1.3 * cm
    linha, linha_tit = 18.0, 21.0          # leading dos estilos CAPA e CAPA_TIT
    texto = 2 * linha + linha + linha_tit + linha + 2 * linha + 0.35 * cm
    # A folga precisa ser generosa: com apenas 0,2 cm o reportlab empurrava a
    # ultima linha ('2026') para uma segunda folha em branco.
    vao = ALTURA_UTIL - texto - 1.0 * cm
    # proporcao entre os tres vaos: instituicao->autor, autor->titulo, titulo->local
    a, b, c = (vao * 0.18, vao * 0.30, vao * 0.52)

    s.append(Paragraph("UNIVERSIDADE VILA VELHA", CAPA))
    s.append(Paragraph("ARQUITETURA DE DADOS RELACIONAIS I", CAPA))
    s.append(Spacer(1, a))
    s.append(Paragraph(AUTOR.upper(), CAPA))
    s.append(Spacer(1, b))
    s.append(Paragraph(
        "AOP02 &mdash; PROJETO L&Oacute;GICO E F&Iacute;SICO:", CAPA_TIT))
    s.append(Spacer(1, 0.35 * cm))
    s.append(Paragraph("Banco de Dados de Pre&ccedil;os de Combust&iacute;veis", CAPA))
    s.append(Spacer(1, c))
    s.append(Paragraph("VILA VELHA", CAPA))
    s.append(Paragraph("2026", CAPA))
    s.append(PageBreak())

    # ---------------- Introducao ----------------
    s.append(Paragraph("1. Apresenta&ccedil;&atilde;o", H))
    s.append(Paragraph(
        "Este documento apresenta o projeto l&oacute;gico e o projeto f&iacute;sico do banco de "
        "dados de pre&ccedil;os de combust&iacute;veis, convertidos a partir do modelo "
        "conceitual entregue na AOP01. O projeto l&oacute;gico &eacute; o modelo relacional "
        "normalizado at&eacute; a 3&ordf; Forma Normal; o projeto f&iacute;sico &eacute; sua "
        "implementa&ccedil;&atilde;o em <b>MySQL 8.0.46</b>, com as tabelas povoadas e as "
        "consultas exigidas pelo enunciado em funcionamento.", P))
    s.append(Paragraph(
        "Todos os scripts SQL trazem, no cabe&ccedil;alho de coment&aacute;rio, o nome e a "
        "matr&iacute;cula do autor, vis&iacute;veis nas capturas de tela deste documento.", P))

    s.append(Paragraph("1.1 Convers&atilde;o do modelo conceitual", H2))
    s.append(Paragraph(
        "O modelo ER da AOP01 definia as entidades <b>Posto</b>, <b>Combust&iacute;vel</b> e "
        "<b>Coleta</b>. Sua convers&atilde;o ao modelo relacional exigiu quatro "
        "decis&otilde;es de normaliza&ccedil;&atilde;o:", P))
    s.append(Paragraph(
        "<b>a)</b> O atributo <b>multivalorado</b> <i>Telefone</i> deu origem &agrave; tabela "
        "<font face='Courier'>telefone_posto</font>. A 1&ordf; Forma Normal pro&iacute;be "
        "armazenar v&aacute;rios valores numa &uacute;nica coluna.", P))
    s.append(Paragraph(
        "<b>b)</b> O atributo <b>composto</b> <i>Endere&ccedil;o</i> foi decomposto nas colunas "
        "<font face='Courier'>rua</font>, <font face='Courier'>numero</font> e "
        "<font face='Courier'>cep</font> da tabela <font face='Courier'>posto</font>.", P))
    s.append(Paragraph(
        "<b>c)</b> A parcela <i>Bairro</i> desse endere&ccedil;o foi promovida a tabela "
        "pr&oacute;pria. Mantida como texto dentro de <font face='Courier'>posto</font>, os "
        "atributos <font face='Courier'>cidade</font> e <font face='Courier'>uf</font> "
        "dependeriam transitivamente da chave do posto &mdash; viola&ccedil;&atilde;o da "
        "3&ordf; Forma Normal.", P))
    s.append(Paragraph(
        "<b>d)</b> O atributo <b>derivado</b> <i>Qtd_Amostras</i> n&atilde;o foi armazenado. "
        "Ele &eacute; calculado pela vis&atilde;o "
        "<font face='Courier'>vw_posto_amostras</font>, que conta as coletas de cada posto.", P))
    s.append(Paragraph(
        "Os dois relacionamentos 1:N do modelo conceitual, <i>Registra</i> e "
        "<i>Referente_Cbstvl</i>, tornaram-se chaves estrangeiras obrigat&oacute;rias na "
        "tabela <font face='Courier'>coleta</font>, pois o lado (1,1) de cada um deles "
        "determina a obrigatoriedade da refer&ecirc;ncia.", P))

    s.append(Paragraph("1.2 Origem dos dados", H2))
    s.append(Paragraph(
        "Os dados s&atilde;o reais e prov&ecirc;m da <b>S&eacute;rie Hist&oacute;rica de "
        "Pre&ccedil;os de Combust&iacute;veis da ANP</b>, referentes ao munic&iacute;pio de "
        "Vila Velha/ES no per&iacute;odo de <b>07/01/2026 a 26/08/2026</b>. Foram "
        "selecionados <b>5 postos</b> distribu&iacute;dos por <b>3 bairros</b> "
        "(Praia de Itaparica, Divino Esp&iacute;rito Santo e Itaparica), totalizando "
        "<b>569 coletas</b> de pre&ccedil;o nos quatro combust&iacute;veis exigidos "
        "&mdash; Gasolina, Gasolina Aditivada, Etanol e Diesel &mdash; com 27 a 31 datas "
        "distintas por posto.", P))
    s.append(Paragraph(
        "Dessa forma os requisitos II.a (5 postos e 4 combust&iacute;veis), II.b (m&iacute;nimo "
        "de 5 coletas por posto em datas diferentes) e II.c (m&iacute;nimo de 2 bairros) "
        "est&atilde;o atendidos com folga.", P))

    # ---------------- Projeto Logico ----------------
    s.append(Paragraph("2. Projeto L&oacute;gico &mdash; modelo relacional (3FN)", H))
    s.append(Paragraph(
        "O diagrama abaixo foi gerado no <b>MySQL Workbench</b> pela funcionalidade "
        "<i>Reverse Engineer</i>, a partir do banco f&iacute;sico j&aacute; implementado. Ele "
        "apresenta as cinco tabelas com seus atributos, tipos de dados, chaves "
        "prim&aacute;rias, chaves estrangeiras e os relacionamentos entre elas.", P))
    s.append(Paragraph(
        "Observa-se a tabela <font face='Courier'>coleta</font> ao centro, referenciando "
        "<font face='Courier'>posto</font> e <font face='Courier'>combustivel</font>; a tabela "
        "<font face='Courier'>bairro</font> referenciada por <font face='Courier'>posto</font>; "
        "e <font face='Courier'>telefone_posto</font> com chave prim&aacute;ria composta, "
        "materializando o atributo multivalorado do modelo conceitual.", P))
    s += figura("projetologico-diagramaeer-mysqlworkbench.png",
                "Figura 1 &mdash; Diagrama EER do modelo relacional, gerado no MySQL Workbench.")
    agrupar_figura(s)

    # ---------------- DDL ----------------
    s.append(Paragraph("3. Projeto F&iacute;sico &mdash; defini&ccedil;&atilde;o do banco (DDL)", H))
    s.append(Paragraph(
        "O script <font face='Courier'>01-schema.sql</font> cria o banco "
        "<font face='Courier'>precos_combustiveis</font> e suas cinco tabelas no mecanismo "
        "InnoDB. O cabe&ccedil;alho do script, vis&iacute;vel na captura, documenta a "
        "correspond&ecirc;ncia entre cada constru&ccedil;&atilde;o do modelo conceitual e sua "
        "contrapartida relacional.", P))
    s.append(Paragraph(
        "O projeto emprega os tipos de restri&ccedil;&atilde;o trabalhados na disciplina: "
        "<b>PRIMARY KEY</b>, <b>FOREIGN KEY</b> com as a&ccedil;&otilde;es referenciais "
        "<i>ON UPDATE CASCADE</i> e <i>ON DELETE RESTRICT</i>, <b>UNIQUE</b>, <b>NOT NULL</b>, "
        "<b>CHECK</b>, <b>DEFAULT</b> e <b>AUTO_INCREMENT</b>.", P))
    s.append(Paragraph(
        "No painel <i>Action Output</i>, ao p&eacute; da janela, todas as opera&ccedil;&otilde;es "
        "aparecem com marca&ccedil;&atilde;o verde: a cria&ccedil;&atilde;o do banco, das cinco "
        "tabelas, do &iacute;ndice de apoio e da vis&atilde;o do atributo derivado.", P))
    s += figura("projetofisico-schema.png",
                "Figura 2 &mdash; Execu&ccedil;&atilde;o do DDL. Cabe&ccedil;alho com a "
                "identifica&ccedil;&atilde;o do autor e log de cria&ccedil;&atilde;o sem erros.")
    agrupar_figura(s)

    # ---------------- Carga ----------------
    s.append(Paragraph("4. Projeto F&iacute;sico &mdash; carga dos dados (DML)", H))
    s.append(Paragraph(
        "O script <font face='Courier'>02-dados.sql</font> insere os dados extra&iacute;dos da "
        "s&eacute;rie da ANP. Seu cabe&ccedil;alho registra a fonte e o per&iacute;odo "
        "coberto, e o corpo do script mostra a inser&ccedil;&atilde;o dos tr&ecirc;s bairros e "
        "dos quatro tipos de combust&iacute;vel.", P))
    s.append(Paragraph(
        "O <i>Action Output</i> comprova a carga completa, informando a quantidade de "
        "registros inseridos em cada tabela: <b>3</b> em <font face='Courier'>bairro</font>, "
        "<b>4</b> em <font face='Courier'>combustivel</font>, <b>5</b> em "
        "<font face='Courier'>posto</font>, <b>7</b> em "
        "<font face='Courier'>telefone_posto</font> e <b>569</b> em "
        "<font face='Courier'>coleta</font>, todas sem duplicatas ou avisos.", P))
    s += figura("projetofisico-dados.png",
                "Figura 3 &mdash; Carga dos dados. O log confirma 569 coletas inseridas.")
    agrupar_figura(s)

    # ---------------- Tabelas povoadas ----------------
    s.append(Paragraph("5. Tabelas povoadas", H))
    s.append(Paragraph(
        "A consulta abaixo percorre as cinco tabelas do modelo e retorna, para cada uma, a "
        "quantidade de linhas armazenadas. Ela comprova em um &uacute;nico resultado que "
        "nenhuma tabela ficou vazia ap&oacute;s a carga:", P))
    s.append(Paragraph(
        "<font face='Courier'>bairro</font> com <b>3</b> registros, "
        "<font face='Courier'>posto</font> com <b>5</b>, "
        "<font face='Courier'>telefone_posto</font> com <b>7</b>, "
        "<font face='Courier'>combustivel</font> com <b>4</b> e "
        "<font face='Courier'>coleta</font> com <b>569</b>. No painel "
        "<i>Action Output</i> confirma-se o retorno de 5 linhas, e no painel "
        "<i>Navigator</i>, &agrave; esquerda, o banco "
        "<font face='Courier'>precos_combustiveis</font> aparece expandido com suas tabelas "
        "e vis&otilde;es.", P))
    s.append(Paragraph(
        "Cabe destacar a tabela <font face='Courier'>telefone_posto</font>: seus 7 registros "
        "distribu&iacute;dos entre 5 postos significam que alguns deles possuem mais de um "
        "n&uacute;mero de telefone. &Eacute; precisamente essa multiplicidade que justifica o "
        "mapeamento do atributo multivalorado em tabela pr&oacute;pria &mdash; "
        "represent&aacute;-la numa &uacute;nica coluna violaria a 1&ordf; Forma Normal.", P))
    s.append(Paragraph(
        "Os n&uacute;meros conferem com o log de inser&ccedil;&atilde;o apresentado na Figura 3 "
        "e atendem aos m&iacute;nimos do enunciado: 5 postos e 4 combust&iacute;veis (II.a) "
        "distribu&iacute;dos por 3 bairros (II.c).", P))
    s += figura("projetofisico-consulta-tabelaspovoadas.png",
                "Figura 4 &mdash; Todas as tabelas povoadas: contagem de registros de cada "
                "uma das cinco tabelas do modelo.")
    agrupar_figura(s)

    # ---------------- Consultas ----------------
    s.append(Paragraph("6. Consultas exigidas (item II.d)", H))
    s.append(Paragraph(
        "Cada consulta obrigat&oacute;ria foi mantida em arquivo pr&oacute;prio, de modo que a "
        "captura apresente simultaneamente a identifica&ccedil;&atilde;o do autor, o "
        "c&oacute;digo-fonte da consulta e o resultado obtido.", P))

    s.append(Paragraph("6.1 Consulta I &mdash; menor e maior pre&ccedil;o por combust&iacute;vel", H2))
    s.append(Paragraph(
        "Retorna o menor e o maior pre&ccedil;o de cada tipo de combust&iacute;vel, com nome do "
        "posto, endere&ccedil;o, bairro, tipo, valor e data da coleta. A fun&ccedil;&atilde;o de "
        "janela <font face='Courier'>ROW_NUMBER()</font> classifica as coletas de cada "
        "combust&iacute;vel simultaneamente por valor crescente e decrescente; a primeira "
        "posi&ccedil;&atilde;o de cada ordena&ccedil;&atilde;o corresponde, respectivamente, ao "
        "menor e ao maior pre&ccedil;o. O resultado traz <b>8 linhas</b> &mdash; o par "
        "m&iacute;nimo e m&aacute;ximo de cada um dos quatro combust&iacute;veis.", P))
    s += figura("projetofisico-consulta-maioremenorpreco.png",
                "Figura 5 &mdash; Consulta I e seu resultado (8 linhas).")
    agrupar_figura(s)

    s.append(Paragraph("6.2 Consulta II &mdash; pre&ccedil;o m&eacute;dio e quantidade de amostras", H2))
    s.append(Paragraph(
        "Retorna, para cada posto e cada tipo de combust&iacute;vel, a quantidade de amostras "
        "coletadas e o pre&ccedil;o m&eacute;dio praticado, acompanhados do nome do posto e do "
        "bairro. O agrupamento por posto e combust&iacute;vel produz <b>20 linhas</b>, uma para "
        "cada combina&ccedil;&atilde;o dos cinco postos com os quatro combust&iacute;veis. A "
        "coluna <font face='Courier'>qtd_amostras</font> revela entre 27 e 31 "
        "amostras por combina&ccedil;&atilde;o, bem acima do m&iacute;nimo de 5 exigido.", P))
    s += figura("projetofisico-consulta-mediaeamostras.png",
                "Figura 6 &mdash; Consulta II e seu resultado (20 linhas).")
    agrupar_figura(s)

    s.append(Paragraph("6.3 Consulta III &mdash; pre&ccedil;o mais recente", H2))
    s.append(Paragraph(
        "Retorna, para cada posto e cada tipo de combust&iacute;vel, apenas a "
        "cota&ccedil;&atilde;o mais recente registrada. A fun&ccedil;&atilde;o de janela "
        "particiona as coletas por posto e combust&iacute;vel, ordena da data mais nova para a "
        "mais antiga e retem somente a primeira de cada parti&ccedil;&atilde;o. S&atilde;o "
        "<b>20 linhas</b>, com datas concentradas na segunda quinzena de agosto de 2026 &mdash; "
        "as coletas mais recentes dispon&iacute;veis na s&eacute;rie.", P))
    s += figura("projetofisico-consulta-precomaisrecente.png",
                "Figura 7 &mdash; Consulta III e seu resultado (20 linhas).")
    agrupar_figura(s)

    s.append(Paragraph("6.4 Consulta IV &mdash; evolu&ccedil;&atilde;o do pre&ccedil;o no tempo", H2))
    s.append(Paragraph(
        "Mostra a evolu&ccedil;&atilde;o do pre&ccedil;o de um combust&iacute;vel espec&iacute;fico "
        "em um posto espec&iacute;fico, ordenada pelas datas de coleta. No exemplo consulta-se a "
        "Gasolina no posto <i>Auto Posto R M Ltda</i>, no bairro Praia de Itaparica, "
        "resultando em <b>31 linhas</b> entre janeiro e agosto de 2026.", P))
    s.append(Paragraph(
        "A s&eacute;rie evidencia o comportamento do pre&ccedil;o ao longo do semestre: parte de "
        "R$ 6,29 em janeiro, recua at&eacute; R$ 6,06 no in&iacute;cio de mar&ccedil;o, sobe "
        "abruptamente para R$ 6,59 em 11 de mar&ccedil;o e oscila em patamar superior nos meses "
        "seguintes. Alterando os dois valores da cl&aacute;usula "
        "<font face='Courier'>WHERE</font> obt&eacute;m-se a s&eacute;rie de qualquer outro "
        "posto e combust&iacute;vel.", P))
    s += figura("projetofisico-consulta-evolucaopreco.png",
                "Figura 8 &mdash; Consulta IV e seu resultado (31 linhas, ordenadas por data).")
    agrupar_figura(s)

    # ---------------- Integridade ----------------
    s.append(Paragraph("7. Verifica&ccedil;&atilde;o das restri&ccedil;&otilde;es de integridade", H))
    s.append(Paragraph(
        "Para demonstrar que as restri&ccedil;&otilde;es declaradas no DDL s&atilde;o "
        "efetivamente aplicadas pelo SGBD &mdash; e n&atilde;o apenas declaradas &mdash; foram "
        "submetidos tr&ecirc;s comandos de inser&ccedil;&atilde;o deliberadamente "
        "inv&aacute;lidos. Todos foram rejeitados, como mostram as linhas em vermelho no "
        "<i>Action Output</i>:", P))
    s.append(Paragraph(
        "<b>Erro 3819</b> &mdash; um valor negativo de pre&ccedil;o foi barrado pela "
        "restri&ccedil;&atilde;o <font face='Courier'>CHECK ck_coleta_valor</font>, que exige "
        "valor maior que zero.", P))
    s.append(Paragraph(
        "<b>Erro 1062</b> &mdash; a tentativa de registrar uma segunda coleta para o mesmo "
        "posto, combust&iacute;vel e data foi barrada pela chave &uacute;nica "
        "<font face='Courier'>uk_coleta_amostra</font>, que garante uma &uacute;nica "
        "cota&ccedil;&atilde;o por amostra.", P))
    s.append(Paragraph(
        "<b>Erro 1452</b> &mdash; a refer&ecirc;ncia a um posto inexistente foi barrada pela "
        "chave estrangeira <font face='Courier'>fk_coleta_posto</font>, preservando a "
        "integridade referencial entre as tabelas.", P))
    s += figura("projetofisico-integridade.png",
                "Figura 9 &mdash; Restri&ccedil;&otilde;es rejeitando dados inv&aacute;lidos: "
                "CHECK, UNIQUE e FOREIGN KEY.")
    agrupar_figura(s)

    # ---------------- Conclusao ----------------
    s.append(Paragraph("8. Conclus&atilde;o", H))
    s.append(Paragraph(
        "O projeto conceitual da AOP01 foi integralmente convertido em um modelo relacional na "
        "3&ordf; Forma Normal e implementado em MySQL 8.0.46. O banco encontra-se "
        "funcional e povoado com dados reais, e as quatro consultas exigidas pelo item II.d do "
        "enunciado foram executadas com sucesso, retornando respectivamente 8, 20, 20 e 31 "
        "linhas.", P))
    s.append(Paragraph(
        "As restri&ccedil;&otilde;es de integridade foram n&atilde;o apenas declaradas, mas "
        "verificadas em execu&ccedil;&atilde;o. Os atributos especiais do modelo conceitual "
        "receberam tratamento adequado: o multivalorado tornou-se tabela pr&oacute;pria, o "
        "composto foi decomposto em colunas simples, e o derivado permaneceu como "
        "c&aacute;lculo em uma vis&atilde;o, sem ocupar espa&ccedil;o de armazenamento.", P))
    s.append(Paragraph(
        "Os artefatos de divulga&ccedil;&atilde;o &agrave; comunidade &mdash; planilhas e "
        "gr&aacute;ficos do item II.e &mdash; ser&atilde;o objeto da AOP03.", P))

    s.append(Paragraph("Refer&ecirc;ncia dos dados", H2))
    s.append(Paragraph(
        "BRASIL. Ag&ecirc;ncia Nacional do Petr&oacute;leo, G&aacute;s Natural e "
        "Biocombust&iacute;veis. <i>S&eacute;rie Hist&oacute;rica de Pre&ccedil;os de "
        "Combust&iacute;veis</i>. Dados abertos, jan.&ndash;ago. 2026. "
        "Dispon&iacute;vel em: gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
        "serie-historica-de-precos-de-combustiveis.", P))

    doc = SimpleDocTemplate(
        str(SAIDA), pagesize=A4,
        leftMargin=MARGEM, rightMargin=MARGEM,
        topMargin=1.3 * cm, bottomMargin=1.3 * cm,
        title="AOP02 - Projeto Logico e Fisico - " + AUTOR,
        author=AUTOR, subject="Arquitetura de Dados Relacionais I - UVV")
    try:
        doc.build(s)
    except PermissionError:
        raise SystemExit(
            "nao consegui gravar " + SAIDA.name + ": o arquivo esta aberto em "
            "algum leitor de PDF. Feche-o e rode o script de novo.")
    return SAIDA


if __name__ == "__main__":
    caminho = construir()
    from pypdf import PdfReader
    paginas = PdfReader(str(caminho)).pages
    n = len(paginas)
    # A capa e uma folha so: se a ultima linha transbordar, a pagina 2 fica
    # praticamente vazia em vez de comecar a Apresentacao.
    assert len(paginas[1].extract_text().strip()) > 300,         "pagina 2 quase vazia - algum elemento da capa transbordou"
    tam = caminho.stat().st_size
    print(caminho.name + " gerado - " + str(n) + " paginas, "
          + format(tam / 1024, ".0f") + " KB")
    assert 6 <= n <= 12, "numero de paginas fora do esperado: " + str(n)
    sys.exit(0)
