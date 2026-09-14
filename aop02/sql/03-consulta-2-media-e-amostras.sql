-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- CONSULTA II  (requisito II.d.II)
-- Para cada posto e cada tipo de combustivel: a quantidade de amostras
-- daquele posto e o preco medio de cada combustivel.
-- Retorna: nome do posto, bairro, tipo de combustivel, preco medio
--          e quantidade de amostras.
--
-- Resultado esperado: 20 linhas (5 postos x 4 combustiveis).
-- =====================================================================

USE precos_combustiveis;

SELECT  p.nome                    AS posto,
        b.nome                    AS bairro,
        cb.tipo                   AS combustivel,
        ROUND(AVG(c.valor), 3)    AS preco_medio,
        COUNT(*)                  AS qtd_amostras
FROM        coleta      c
INNER JOIN  posto       p  ON p.id_posto        = c.id_posto
INNER JOIN  bairro      b  ON b.id_bairro       = p.id_bairro
INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
GROUP BY p.id_posto, p.nome, b.nome, cb.id_combustivel, cb.tipo
ORDER BY posto, combustivel;
