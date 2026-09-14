-- =====================================================================
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
-- Projeto de Extensao: Precos de Combustiveis - Vila Velha/ES
--
-- 01-schema.sql : PROJETO FISICO - definicao do banco (DDL)
-- SGBD: MySQL 8.0 / InnoDB
--
-- Conversao do projeto conceitual (AOP01, modelo ER) para o modelo
-- relacional em 3a Forma Normal:
--
--   Telefone (multivalorado)  -> tabela propria telefone_posto        (1FN)
--   Endereco (composto)       -> colunas rua, numero, cep em posto
--   Bairro   (do composto)    -> tabela propria bairro + FK em posto  (3FN)
--   Qtd_Amostras (derivado)   -> NAO e coluna: view vw_posto_amostras
--   Registra        1:N       -> FK coleta.id_posto       NOT NULL
--   Referente_Cbstvl 1:N      -> FK coleta.id_combustivel NOT NULL
--
-- Restricoes utilizadas: PRIMARY KEY, FOREIGN KEY (com ON UPDATE CASCADE
-- e ON DELETE RESTRICT), UNIQUE, NOT NULL, CHECK, DEFAULT, AUTO_INCREMENT.
--
-- #####################################################################
-- #  ATENCAO: este script comeca com DROP DATABASE. Ele apaga e recria
-- #  o banco VAZIO. Depois de rodar este arquivo, rode SEMPRE o
-- #  02-dados.sql em seguida, senao todas as consultas voltarao vazias.
-- #####################################################################
-- =====================================================================

DROP DATABASE IF EXISTS precos_combustiveis;
CREATE DATABASE precos_combustiveis
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE precos_combustiveis;


-- ---------------------------------------------------------------------
-- BAIRRO
-- Extraida do atributo composto Endereco do MER. Isola a localidade do
-- posto: sem ela, cidade e uf ficariam dependentes de forma transitiva
-- do posto atraves do bairro, violando a 3FN.
-- ---------------------------------------------------------------------
CREATE TABLE bairro (
    id_bairro   INT          NOT NULL AUTO_INCREMENT,
    nome        VARCHAR(60)  NOT NULL,
    cidade      VARCHAR(60)  NOT NULL DEFAULT 'Vila Velha',
    uf          CHAR(2)      NOT NULL DEFAULT 'ES',
    CONSTRAINT pk_bairro        PRIMARY KEY (id_bairro),
    CONSTRAINT uk_bairro_local  UNIQUE (nome, cidade, uf),
    CONSTRAINT ck_bairro_uf     CHECK (uf REGEXP '^[A-Z]{2}$')
) ENGINE = InnoDB;


-- ---------------------------------------------------------------------
-- POSTO
-- Entidade Posto do MER. Bandeira e o unico atributo OPCIONAL (NULL),
-- exatamente como marcado no projeto conceitual: posto de bandeira
-- BRANCA nao possui bandeira.
-- ---------------------------------------------------------------------
CREATE TABLE posto (
    id_posto    INT          NOT NULL AUTO_INCREMENT,
    cnpj        CHAR(14)     NOT NULL,
    nome        VARCHAR(120) NOT NULL,
    bandeira    VARCHAR(60)      NULL,
    rua         VARCHAR(120) NOT NULL,
    numero      VARCHAR(15)      NULL,
    cep         CHAR(8)          NULL,
    id_bairro   INT          NOT NULL,
    CONSTRAINT pk_posto       PRIMARY KEY (id_posto),
    CONSTRAINT uk_posto_cnpj  UNIQUE (cnpj),
    CONSTRAINT ck_posto_cnpj  CHECK (cnpj REGEXP '^[0-9]{14}$'),
    CONSTRAINT ck_posto_cep   CHECK (cep IS NULL OR cep REGEXP '^[0-9]{8}$'),
    CONSTRAINT fk_posto_bairro FOREIGN KEY (id_bairro)
        REFERENCES bairro (id_bairro)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- ---------------------------------------------------------------------
-- TELEFONE_POSTO
-- Mapeamento do atributo MULTIVALORADO Telefone. A 1FN proibe guardar
-- varios telefones em uma unica coluna, entao ele vira tabela propria
-- com chave primaria composta (id_posto, telefone).
-- ---------------------------------------------------------------------
CREATE TABLE telefone_posto (
    id_posto    INT         NOT NULL,
    telefone    VARCHAR(20) NOT NULL,
    CONSTRAINT pk_telefone_posto PRIMARY KEY (id_posto, telefone),
    CONSTRAINT fk_telefone_posto FOREIGN KEY (id_posto)
        REFERENCES posto (id_posto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;


-- ---------------------------------------------------------------------
-- COMBUSTIVEL
-- Entidade Combustivel do MER. Os 4 tipos do requisito II.a.
-- ---------------------------------------------------------------------
CREATE TABLE combustivel (
    id_combustivel INT         NOT NULL AUTO_INCREMENT,
    tipo           VARCHAR(30) NOT NULL,
    CONSTRAINT pk_combustivel      PRIMARY KEY (id_combustivel),
    CONSTRAINT uk_combustivel_tipo UNIQUE (tipo)
) ENGINE = InnoDB;


-- ---------------------------------------------------------------------
-- COLETA
-- Entidade Coleta do MER. Concentra os dois relacionamentos 1:N:
-- o lado (1,1) de Registra e de Referente_Cbstvl vira FK obrigatoria.
-- A UNIQUE garante uma unica cotacao por posto/combustivel/data.
-- ---------------------------------------------------------------------
CREATE TABLE coleta (
    id_coleta      INT           NOT NULL AUTO_INCREMENT,
    id_posto       INT           NOT NULL,
    id_combustivel INT           NOT NULL,
    data_coleta    DATE          NOT NULL,
    valor          DECIMAL(6,3)  NOT NULL,
    CONSTRAINT pk_coleta        PRIMARY KEY (id_coleta),
    CONSTRAINT uk_coleta_amostra UNIQUE (id_posto, id_combustivel, data_coleta),
    CONSTRAINT ck_coleta_valor   CHECK (valor > 0),
    CONSTRAINT fk_coleta_posto FOREIGN KEY (id_posto)
        REFERENCES posto (id_posto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_coleta_combustivel FOREIGN KEY (id_combustivel)
        REFERENCES combustivel (id_combustivel)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;

-- Indice de apoio as consultas por combustivel e por data (itens II.d.I e II.d.IV).
CREATE INDEX ix_coleta_combustivel_data ON coleta (id_combustivel, data_coleta);


-- ---------------------------------------------------------------------
-- VW_POSTO_AMOSTRAS
-- Atributo DERIVADO Qtd_Amostras do MER. Atributo derivado nao se
-- armazena em 3FN: ele e calculado a partir das coletas do posto.
-- ---------------------------------------------------------------------
CREATE VIEW vw_posto_amostras AS
SELECT  p.id_posto,
        p.nome              AS posto,
        b.nome              AS bairro,
        COUNT(c.id_coleta)  AS qtd_amostras
FROM        posto  p
INNER JOIN  bairro b ON b.id_bairro = p.id_bairro
LEFT JOIN   coleta c ON c.id_posto  = p.id_posto
GROUP BY p.id_posto, p.nome, b.nome;
