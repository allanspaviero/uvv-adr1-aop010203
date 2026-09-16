# AOP03 — Divulgação para a comunidade

**Arquitetura de Dados Relacionais I — UVV**
Allan Spaviero Alpoim — matrícula 202636574
Projeto de Extensão: *Preços de Combustíveis* — Vila Velha/ES

Divulgação dos resultados do projeto à comunidade pela **criação de um website**
(opção *a* do enunciado), que permite ao usuário efetuar todas as consultas do
item II.d e traz as planilhas e os gráficos do item II.e.

**No ar em:** <https://allanspaviero.github.io/uvv-adr1-aop010203/>

---

## A ideia central

O site **não reimplementa nenhuma consulta**. Ele abre o banco de dados dentro do
navegador — SQLite compilado para WebAssembly — e executa os mesmos arquivos
`.sql` entregues no projeto físico da AOP02, sem alterar uma linha. É por isso
que cada painel consegue mostrar, atrás de um "ver a consulta SQL", exatamente o
comando que produziu a tabela logo acima.

```
build (Python, uma vez)            navegador (estático, sem servidor)
─────────────────────────          ──────────────────────────────────
aop02/sql/01-schema.sql  ─┐
aop02/sql/02-dados.sql   ─┼─► banco.db ───────────► sql.js ──► tabelas
                          │                           ▲
aop02/sql/03-consulta-*  ─┼─► (copiados verbatim) ────┘
aop03/sql/05-grafico-*   ─┤                           └──► Chart.js ──► gráficos
                          └─► .xlsx + .csv ────────────────► download
```

A tradução do DDL do MySQL para o SQLite não foi reescrita aqui: reaproveita
`para_sqlite()` de [`aop02/scripts/validar.py`](../aop02/scripts/validar.py), que
já estava testado. O `REGEXP` das restrições `CHECK` não existe no SQLite, mas
isso só importa na carga, feita em Python no build — o navegador recebe um banco
pronto e executa apenas `SELECT`.

## O que tem aqui

```
site/index.html      um painel por consulta, trocados pelas abas do topo
site/style.css       paleta tirada do selo da UVV; só tema claro
site/app.js          abre o banco, executa os .sql e desenha tabelas e gráficos
site/consultas/      os .sql do projeto, copiados no build (não editar aqui)
site/dados/          banco.db, a planilha e os CSVs (gerados)
site/vendor/         sql.js, Chart.js e as fontes, versionados para o site
                     não depender de CDN nenhum na hora de ser apresentado

scripts/gerar_banco.py       monta o banco.db e copia as consultas
scripts/gerar_planilhas.py   gera a planilha do item II.e e os CSVs
scripts/verificar.py         auto-verificação da entrega inteira
scripts/desfocar.py          borra regiões de uma foto antes do relatório

sql/05-grafico-1-media-por-combustivel.sql           requisito II.e.I
sql/05-grafico-2-media-por-combustivel-e-posto.sql   requisito II.e.II

docs/ROTEIRO-EVIDENCIAS.md   passo a passo da sessão de divulgação
```

## Navegação

O menu do topo não rola a página: cada item troca o painel visível, e só um fica
na tela por vez. O endereço acompanha a troca, então `#consulta-2` abre direto na
consulta II e os botões de voltar e avançar do navegador funcionam.

Um detalhe que exigiu cuidado: o Chart.js mede o canvas no momento de desenhar, e
canvas dentro de painel escondido mede zero. Por isso a troca de aba chama
`resize()` nos gráficos que acabaram de aparecer.

## Como rodar

**Reconstruir os dados do site** (já vêm prontos no repositório):

```bash
python aop03/scripts/gerar_banco.py
python aop03/scripts/gerar_planilhas.py
```

**Conferir que a entrega atende ao enunciado:**

```bash
python aop03/scripts/verificar.py
```

**Ver o site localmente.** Ele precisa ser servido por HTTP: abrir o
`index.html` com dois cliques não funciona, porque o navegador bloqueia a leitura
do banco de dados a partir do disco.

```bash
python -m http.server 8765 --directory aop03/site
```

Depois abra <http://localhost:8765>.

## Requisitos do enunciado e onde estão atendidos

| Requisito | Onde |
|---|---|
| Opção *a* — website que permite efetuar as consultas | o site inteiro, publicado no GitHub Pages |
| II.d.I — menor e maior preço de cada combustível | aba *Menor e maior preço* |
| II.d.II — preço médio e quantidade de amostras | aba *Média e amostras* |
| II.d.III — preço mais recente por posto e combustível | aba *Preço mais recente* |
| II.d.IV — evolução no tempo, posto e combustível específicos | aba *Evolução no tempo*, com seletores |
| II.e — planilhas com os dados das consultas | aba *Planilhas* — `.xlsx` com uma aba por consulta, mais os CSVs |
| II.e.I — gráfico da evolução do preço médio de cada combustível | primeiro gráfico do site e aba *Gráfico I* da planilha |
| II.e.II — o mesmo, por posto | segundo gráfico do site e aba *Gráfico II* da planilha |

A planilha traz os gráficos como objetos nativos do Excel, não como imagem
colada: abrem interativos e acompanham os dados da própria aba.

## Publicação

O site é publicado por GitHub Actions a cada push em `main` que toque em
`aop03/site/` — veja [`pages.yml`](../.github/workflows/pages.yml). O modo
"deploy from a branch" do Pages só aceita a raiz ou `/docs`, e o site mora em
subpasta, daí o workflow.

## A entrega da AOP03

A entrega no AVA é um **relatório em PDF com as evidências da divulgação**. Pelas
orientações do professor, evidência não é print de site no ar: são fotos ou
vídeos de **pessoas reais usando a solução**, com ambiente e interação visíveis,
sem identificar ninguém. O roteiro dessa sessão está em
[`docs/ROTEIRO-EVIDENCIAS.md`](docs/ROTEIRO-EVIDENCIAS.md).
