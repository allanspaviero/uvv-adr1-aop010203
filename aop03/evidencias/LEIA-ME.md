# Evidências da divulgação

Os prints da videoconferência vão aqui, nomeados na ordem em que entram no
relatório:

```
01-ambiente.png     a chamada com todos conectados, antes de começar
02-apresentacao.png sua tela compartilhada com uma consulta do site
03-uso.png          a tela de outro participante navegando sozinho
04-chat.png         o chat com o link e as respostas
05-planilhas.png    a aba de planilhas, ou alguém baixando o arquivo
```

As imagens **não são versionadas**: o `.gitignore` do projeto bloqueia `.png` e
`.jpg`. É de propósito. São registros de pessoas que consentiram com o uso na
entrega da faculdade, não com a publicação num repositório aberto. Elas ficam no
seu computador e entram apenas no PDF.

O passo a passo da sessão está em [`../docs/ROTEIRO-EVIDENCIAS.md`](../docs/ROTEIRO-EVIDENCIAS.md).

Se algum enquadramento sair com rosto, logotipo ou nome completo visível:

```bash
python aop03/scripts/desfocar.py aop03/evidencias/03-uso.png 120,80,300,200
```
