-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- CONSULTA IV  (requisito II.d.IV)
-- Evolucao do preco ao longo do tempo de UM combustivel especifico em
-- UM posto especifico, ordenada pelas datas de coleta.
-- Retorna: nome do posto, bairro, tipo de combustivel, valor do
--          combustivel e data da coleta.
--
-- Troque os dois valores do WHERE para consultar outro posto ou outro
-- combustivel. Os postos vao de 1 a 5; os tipos validos sao
-- 'Gasolina', 'Gasolina Aditivada', 'Etanol' e 'Diesel'.
--
-- Resultado esperado: 31 linhas para o posto 1 com Gasolina.
-- =====================================================================

USE precos_combustiveis;

SELECT  p.nome        AS posto,
        b.nome        AS bairro,
        cb.tipo       AS combustivel,
        c.valor,
        c.data_coleta
FROM        coleta      c
INNER JOIN  posto       p  ON p.id_posto        = c.id_posto
INNER JOIN  bairro      b  ON b.id_bairro       = p.id_bairro
INNER JOIN  combustivel cb ON cb.id_combustivel = c.id_combustivel
WHERE   p.id_posto       = 1          -- posto especifico
  AND   cb.tipo          = 'Gasolina' -- combustivel especifico
ORDER BY c.data_coleta;
