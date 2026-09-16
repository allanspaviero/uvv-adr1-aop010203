-- =====================================================================
-- AOP03 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- GRAFICO II  (requisito II.e.II)
-- Evolucao do preco medio de cada combustivel EM CADA POSTO ao longo do
-- tempo. Acrescenta o posto ao agrupamento do grafico anterior, para que
-- o site possa desenhar uma linha por posto dentro de cada combustivel.
--
-- Resultado esperado: 160 linhas (8 meses x 4 combustiveis x 5 postos).
-- =====================================================================

USE precos_combustiveis;

SELECT  SUBSTR(CAST(c.data_coleta AS CHAR), 1, 7) AS mes,
        cb.tipo                                   AS combustivel,
        p.nome                                    AS posto,
        b.nome                                    AS bairro,
        ROUND(AVG(c.valor), 3)                    AS preco_medio,
        COUNT(*)                                  AS qtd_amostras
FROM        coleta      c
INNER JOIN  posto       p  ON p.id_posto        = c.id_posto
INNER JOIN  bairro      b  ON b.id_bairro       = p.id_bairro
INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
GROUP BY mes, cb.id_combustivel, cb.tipo, p.id_posto, p.nome, b.nome
ORDER BY combustivel, posto, mes;
