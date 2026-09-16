-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- CONSULTA I  (requisito II.d.I)
-- Menor e maior preco de CADA tipo de combustivel.
-- Retorna: nome do posto, endereco, bairro, tipo de combustivel,
--          valor do combustivel e data da coleta.
--
-- ROW_NUMBER() numera as coletas de cada combustivel por valor crescente
-- e decrescente ao mesmo tempo; a linha de posicao 1 em cada ordenacao e,
-- respectivamente, o menor e o maior preco daquele combustivel.
--
-- Resultado esperado: 8 linhas (o par minimo/maximo dos 4 combustiveis).
-- =====================================================================

USE precos_combustiveis;

WITH ranqueado AS (
    SELECT  cb.tipo                                  AS combustivel,
            p.nome                                   AS posto,
            CONCAT(p.rua, ', ', COALESCE(p.numero, 's/n')) AS endereco,
            b.nome                                   AS bairro,
            c.valor,
            c.data_coleta,
            ROW_NUMBER() OVER (PARTITION BY cb.id_combustivel
                               ORDER BY c.valor ASC,  c.data_coleta DESC) AS pos_menor,
            ROW_NUMBER() OVER (PARTITION BY cb.id_combustivel
                               ORDER BY c.valor DESC, c.data_coleta DESC) AS pos_maior
    FROM        coleta      c
    INNER JOIN  posto       p  ON p.id_posto       = c.id_posto
    INNER JOIN  bairro      b  ON b.id_bairro      = p.id_bairro
    INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
)
SELECT  combustivel,
        CASE WHEN pos_menor = 1 THEN 'MENOR PRECO' ELSE 'MAIOR PRECO' END AS extremo,
        posto,
        endereco,
        bairro,
        valor,
        data_coleta
FROM   ranqueado
WHERE  pos_menor = 1 OR pos_maior = 1
ORDER BY combustivel, extremo DESC;
