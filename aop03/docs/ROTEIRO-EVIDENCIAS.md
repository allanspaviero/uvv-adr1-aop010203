# Roteiro da sessão de evidências — AOP03

**Allan Spaviero Alpoim — 202636574**
Divulgação do projeto *Preços de Combustíveis — Vila Velha/ES* por videoconferência.

Endereço do site: **https://allanspaviero.github.io/uvv-adr1-aop010203/**

---

## O que o professor exige, em uma frase

Não basta provar que o site existe. As evidências precisam mostrar **pessoas
reais usando a solução**, com o ambiente e a interação visíveis, sem identificar
ninguém. Uma apresentação em que só você fala e os outros assistem **não cumpre o
requisito** — é por isso que este roteiro tem um bloco inteiro dedicado a colocar
os participantes no comando.

Regras que valem o tempo todo: consentimento antes de qualquer captura, nada de
rostos, nada de crianças, nada de uniformes ou logotipos identificáveis.

---

## Antes da chamada

**1. Confira o site no ar.** Abra o endereço acima no celular e no computador.
Espere as tabelas aparecerem. Se surgir a mensagem de erro sobre o banco de
dados, avise antes de marcar a sessão.

**2. Convide de 3 a 5 pessoas.** Vizinhos, familiares, colegas — qualquer pessoa
que abasteça na região serve, e é justamente esse o público do projeto. Mensagem
pronta:

> Oi! Estou terminando um trabalho de extensão da faculdade: um site que mostra o
> preço da gasolina, do etanol e do diesel nos postos de Vila Velha, com dados da
> ANP. Preciso apresentar para algumas pessoas e registrar a conversa como
> evidência para a disciplina. São uns 20 minutos numa chamada. Você toparia?
> Não aparece rosto nem nome de ninguém nas imagens — eu explico tudo no começo.

**3. Peça a cada participante, ao entrar:**
- deixar a **câmera desligada**;
- trocar o **nome de exibição** para só o primeiro nome ou algo genérico
  ("Participante 1"). Isso resolve de uma vez a regra de não identificar ninguém.

**4. Deixe aberto no seu computador:** o site, esta página e a ferramenta de
captura de tela. No Windows, `Win + Shift + S` recorta e copia; `Win + Alt + R`
grava vídeo.

**5. Crie a pasta** `aop03/evidencias/` para jogar os arquivos capturados.

---

## Bloco 1 — Abertura e consentimento

**Capture o print 1 antes de começar a falar do projeto:** a tela da chamada com
todos conectados, câmeras desligadas, nomes já trocados. É o print do *ambiente*.

Fala pronta:

> Boa noite, pessoal, obrigado por virem. Antes de começar, três coisas rápidas.
>
> Primeiro: eu vou tirar algumas fotos da tela durante a conversa, porque
> preciso entregar essas imagens como evidência do trabalho para a
> universidade. Nas imagens vai aparecer a tela do site e a janela da chamada —
> não vai aparecer rosto de ninguém, e os nomes estão como vocês colocaram
> agora. As imagens vão só para a entrega da disciplina, não vão para rede
> social nenhuma.
>
> Segundo: se em algum momento vocês não quiserem aparecer em alguma captura, é
> só falar e eu não uso aquela imagem.
>
> Terceiro: quem concorda com isso pode confirmar agora, em voz alta ou no chat?

**Espere a confirmação de todos.** Se alguém não concordar, peça que saia da
chamada antes de você começar a capturar — não dá para usar a evidência sem o
consentimento de quem está nela.

> Combinado. Então vamos lá.

---

## Bloco 2 — O problema e o projeto (você compartilha a tela)

Compartilhe a tela e abra o site no topo da página.

> O que eu construí foi isso aqui. É um trabalho da disciplina de Arquitetura de
> Dados Relacionais, mas a ideia não é acadêmica: é resolver uma coisa chata do
> dia a dia. A gente nunca sabe se o posto em que está abastecendo é caro ou
> barato, porque não dá para rodar a cidade conferindo preço.
>
> Então eu montei um banco de dados com os preços de cinco postos de Vila Velha,
> em três bairros, com quinhentas e sessenta e nove coletas de preço de janeiro a
> agosto. Os dados são oficiais, da Série Histórica da ANP — eu não inventei
> nenhum número.

Aponte a barra de selos no topo (período, coletas, postos, fonte).

> E aqui em cima o site já diz de onde vem tudo: o período coberto, quantas
> coletas tem, quantos postos e a fonte.

---

## Bloco 3 — Passeio pelas consultas

Percorra as seções pelo menu do topo, nesta ordem. Não corra: pare em cada uma e
pergunte se faz sentido.

**"Mais barato"**

> Essa primeira parte é a resposta mais direta: onde cada combustível esteve mais
> barato no período, e em que posto. Olha a diferença do etanol para a gasolina.

**"Menor e maior preço"**

> Aqui a mesma coisa, mas com os dois extremos lado a lado. Repara que dá para
> ver a diferença entre o posto mais caro e o mais barato no mesmo combustível —
> isso é dinheiro que fica no bolso de quem sabe.

**"Média e amostras"**

> Essa tabela mostra quanto cada posto cobrou em média, e sobre quantas coletas
> essa média foi calculada. A coluna de amostras importa: média feita com trinta
> coletas é bem mais confiável do que média feita com duas.

**"Preço mais recente"**

> Essa é a tabela de consultar antes de abastecer: o último preço registrado em
> cada posto, para cada combustível.

**"Evolução no tempo"** — troque o posto e o combustível nos seletores, na frente
deles.

> E aqui dá para escolher um posto e um combustível e ver o preço mudando ao
> longo dos meses. Olha, se eu trocar o posto aqui... a consulta roda de novo na
> hora.

**"Gráficos"** — troque o combustível do segundo gráfico.

> Esses dois gráficos são a parte mais fácil de ler. O primeiro mostra o preço
> médio de cada combustível subindo e descendo. O segundo separa por posto, então
> dá para ver quem costuma cobrar mais caro e quem repassa as quedas primeiro.

**Abra um "Ver a consulta SQL"** — é o que liga o site ao banco de dados e vale a
pena mostrar.

> E essa parte aqui é a graça do trabalho para a disciplina: essa tabela não é um
> texto que eu digitei. O site abre o banco de dados dentro do navegador e roda
> essa consulta aqui, na hora, toda vez que vocês carregam a página.

**Capture o print 2 aqui:** a tela compartilhada mostrando uma tabela do site,
com a janela da chamada e os participantes visíveis na lateral.

---

## Bloco 4 — O bloco que vale a nota: eles usam

Este é o bloco que transforma "apresentação" em "uso pela comunidade". Não pule.

> Agora eu queria que vocês usassem, porque o site não foi feito para eu mostrar,
> foi feito para vocês consultarem. Eu vou mandar o link no chat.

Mande o link no chat da chamada. **Pare de compartilhar sua tela.**

> Abre aí no celular ou no computador de vocês. Enquanto isso eu faço umas
> perguntas, e quem achar primeiro responde.

Perguntas prontas — elas forçam a navegação real pelas quatro consultas:

1. **"Qual posto está com a gasolina mais barata no registro mais recente?"**
   *(leva à seção "Preço mais recente")*
2. **"Em qual bairro fica esse posto?"**
   *(mesma tabela, coluna do bairro)*
3. **"Qual foi o etanol mais barato do período inteiro, e quando?"**
   *(leva à seção "Menor e maior preço")*
4. **"Escolhe um posto aí na 'Evolução no tempo' e me diz se o diesel subiu ou
   caiu de janeiro para agosto."**
   *(leva à consulta com seletores — é a consulta IV do trabalho)*

Depois peça a um participante que **compartilhe a tela dele** enquanto responde:

> Você consegue compartilhar sua tela rapidinho e mostrar onde achou? Só para eu
> registrar que deu para usar sem eu explicar.

**Capture o print 3 aqui — este é o print mais importante da entrega:** a tela de
**outra pessoa** navegando no site, dentro da chamada. É a prova literal de "uso
da solução pela comunidade".

**Capture o print 4:** o chat da chamada com o link e as respostas que eles
digitaram.

---

## Bloco 5 — Encerramento

> Era isso. Se vocês quiserem usar de verdade depois, o link fica no ar — e tem
> um botão lá embaixo para baixar a planilha com todos os dados, se alguém quiser
> mexer no Excel.
>
> Obrigado pelo tempo de vocês. Confirmando de novo: eu vou usar essas imagens só
> na entrega da faculdade. Alguém quer que eu tire alguma?

**Capture o print 5:** a seção "Baixe os dados" do site, ou o momento em que
alguém baixa a planilha.

---

## Checklist dos prints

Confira antes de encerrar a chamada. Faltando um, é mais fácil repetir agora do
que remarcar.

| # | O que mostra | Requisito que cumpre |
|---|---|---|
| 1 | A chamada com todos conectados, antes de começar | o **ambiente** |
| 2 | Sua tela compartilhada com uma tabela do site | a **divulgação** |
| 3 | A tela de outro participante navegando no site | o **uso pela comunidade** |
| 4 | O chat com o link e as respostas dos participantes | a **interação** |
| 5 | A seção de planilhas, ou alguém baixando o arquivo | o **item II.e** |

Se você também gravar vídeo: suba em nuvem (Google Drive, YouTube não listado) e
guarde só o link — o relatório leva o link, não o arquivo.

---

## Depois da chamada

1. Salve os prints em `aop03/evidencias/`, nomeados na ordem:
   `01-ambiente.png`, `02-apresentacao.png`, `03-uso.png`, `04-chat.png`,
   `05-planilhas.png`.

2. **Confira cada imagem** contra as regras: nenhum rosto, nenhum nome completo,
   nenhum logo de empresa, nenhuma criança. Se escapou alguma coisa, borre a
   região:

   ```bash
   python aop03/scripts/desfocar.py aop03/evidencias/03-uso.png 120,80,300,200
   ```

   Os números são `x,y,largura,altura` em pixels, contados do canto superior
   esquerdo. O original não é alterado — sai um arquivo `-desfocada` ao lado.

3. Anote, para cada print, **data, horário e quantas pessoas participaram**. Essa
   informação vira a legenda de cada imagem no relatório.

4. Me chame de volta com os prints prontos. O relatório PDF é montado a partir
   deles, e você revisa o texto antes de virar arquivo.
