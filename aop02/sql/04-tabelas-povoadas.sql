-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- Rode uma consulta de cada vez com Ctrl+Enter (cursor dentro dela),
-- para que o Result Grid mostre um resultado por print.
-- =====================================================================

USE precos_combustiveis;
SELECT 'bairro'         AS tabela, COUNT(*) AS qtd_linhas FROM bairro
UNION ALL
SELECT 'posto',          COUNT(*) FROM posto
UNION ALL
SELECT 'telefone_posto', COUNT(*) FROM telefone_posto
UNION ALL
SELECT 'combustivel',    COUNT(*) FROM combustivel
UNION ALL
SELECT 'coleta',         COUNT(*) FROM coleta;

-- ---------------------------------------------------------------------
-- B. CONTEUDO DE CADA TABELA, uma a uma.
-- ---------------------------------------------------------------------

-- B.1 - BAIRRO (3 linhas) - II.c: os postos cobrem mais de um bairro
SELECT * FROM bairro ORDER BY id_bairro;

-- B.2 - COMBUSTIVEL (4 linhas) - II.a: os 4 tipos exigidos
SELECT * FROM combustivel ORDER BY id_combustivel;

-- B.3 - POSTO (5 linhas) - II.a: os 5 postos coletados
SELECT * FROM posto ORDER BY id_posto;

-- B.4 - TELEFONE_POSTO (7 linhas) - atributo multivalorado do MER
SELECT * FROM telefone_posto ORDER BY id_posto, telefone;

-- B.5 - COLETA (569 linhas) - II.b: as coletas de preco
SELECT * FROM coleta ORDER BY id_coleta;


-- ---------------------------------------------------------------------
-- C. VISAO LEGIVEL DA TABELA COLETA
-- A tabela coleta guarda apenas os IDs das chaves estrangeiras. Esta
-- consulta mostra o mesmo conteudo com os nomes resolvidos, que e o
-- que o leitor do PDF entende. Bom print para acompanhar o B.5.
-- ---------------------------------------------------------------------
SELECT  c.id_coleta,
        p.nome        AS posto,
        b.nome        AS bairro,
        cb.tipo       AS combustivel,
        c.data_coleta,
        c.valor
FROM        coleta      c
INNER JOIN  posto       p  ON p.id_posto        = c.id_posto
INNER JOIN  bairro      b  ON b.id_bairro       = p.id_bairro
INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
ORDER BY c.id_coleta;


-- ---------------------------------------------------------------------
-- D. ATRIBUTO DERIVADO Qtd_Amostras
-- O atributo derivado do projeto conceitual nao e uma coluna
-- armazenada: e calculado por esta view a partir das coletas.
-- ---------------------------------------------------------------------
SELECT * FROM vw_posto_amostras ORDER BY posto;


-- ---------------------------------------------------------------------
-- E. CONFERENCIA DOS MINIMOS DO ENUNCIADO
-- Mostra em uma unica tabela que cada exigencia numerica foi cumprida.
-- ---------------------------------------------------------------------
SELECT 'II.a - postos coletados'        AS requisito,
       '5'                              AS exigido,
       CAST(COUNT(*) AS CHAR)           AS obtido FROM posto
UNION ALL
SELECT 'II.a - tipos de combustivel', '4', CAST(COUNT(*) AS CHAR) FROM combustivel
UNION ALL
SELECT 'II.c - bairros distintos', '>= 2', CAST(COUNT(DISTINCT id_bairro) AS CHAR) FROM posto
UNION ALL
SELECT 'II.b - menor nro de datas por posto', '>= 5',
       CAST(MIN(d.datas) AS CHAR)
FROM  (SELECT id_posto, COUNT(DISTINCT data_coleta) AS datas
       FROM coleta GROUP BY id_posto) d;
