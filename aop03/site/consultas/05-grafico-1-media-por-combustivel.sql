-- =====================================================================
-- AOP03 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- GRAFICO I  (requisito II.e.I)
-- Evolucao do preco medio de CADA combustivel ao longo do tempo.
-- Retorna uma linha por mes e por combustivel, com a media das coletas
-- daquele mes - e a serie que alimenta o grafico de linhas do site.
--
-- SUBSTR(CAST(data AS CHAR), 1, 7) extrai o 'AAAA-MM' da data. E a forma
-- portavel de agrupar por mes: funciona tanto no MySQL do projeto fisico
-- quanto no SQLite que o site executa no navegador.
--
-- Resultado esperado: 32 linhas (8 meses x 4 combustiveis).
-- =====================================================================

USE precos_combustiveis;

SELECT  SUBSTR(CAST(c.data_coleta AS CHAR), 1, 7) AS mes,
        cb.tipo                                   AS combustivel,
        ROUND(AVG(c.valor), 3)                    AS preco_medio,
        COUNT(*)                                  AS qtd_amostras
FROM        coleta      c
INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
GROUP BY mes, cb.id_combustivel, cb.tipo
ORDER BY combustivel, mes;
