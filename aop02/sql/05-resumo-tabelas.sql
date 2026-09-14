-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
--
-- 05-resumo-tabelas.sql
-- Resumo das 5 tabelas do banco com a quantidade de linhas de cada uma.
-- Comprova numa unica consulta que nenhuma tabela do modelo ficou vazia
-- (exigencia do item III.d: "todas as tabelas povoadas").
--
-- Execute o arquivo inteiro com Ctrl+Shift+Enter: como ha apenas uma
-- consulta, o Result Grid mostra um unico resultado, pronto para o print.
--
-- Resultado esperado: 5 linhas
--   bairro 3 | posto 5 | telefone_posto 7 | combustivel 4 | coleta 569
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
