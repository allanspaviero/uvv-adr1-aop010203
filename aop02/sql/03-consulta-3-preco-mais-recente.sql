-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- CONSULTA III  (requisito II.d.III)
-- Para cada posto e cada tipo de combustivel, APENAS o preco mais
-- recente registrado.
-- Retorna: nome do posto, bairro, tipo de combustivel, valor do
--          combustivel e data da coleta.
--
-- ROW_NUMBER() particiona as coletas por posto e combustivel e ordena
-- da data mais nova para a mais antiga; a posicao 1 e a cotacao atual.
--
-- Resultado esperado: 20 linhas (5 postos x 4 combustiveis).
-- =====================================================================

USE precos_combustiveis;

WITH mais_recente AS (
    SELECT  p.nome        AS posto,
            b.nome        AS bairro,
            cb.tipo       AS combustivel,
            c.valor,
            c.data_coleta,
            ROW_NUMBER() OVER (PARTITION BY c.id_posto, c.id_combustivel
                               ORDER BY c.data_coleta DESC) AS pos
    FROM        coleta      c
    INNER JOIN  posto       p  ON p.id_posto        = c.id_posto
    INNER JOIN  bairro      b  ON b.id_bairro       = p.id_bairro
    INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
)
SELECT  posto, bairro, combustivel, valor, data_coleta
FROM    mais_recente
WHERE   pos = 1
ORDER BY posto, combustivel;
