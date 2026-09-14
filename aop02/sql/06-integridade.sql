-- deve ser recusado pelo CHECK
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (1, 1, '2026-09-01', -1);

-- deve ser recusado pela UNIQUE
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (1, 1, '2026-01-07', 6.19);

-- deve ser recusado pela FOREIGN KEY
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (999, 1, '2026-09-01', 6.19);