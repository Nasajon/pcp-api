INSERT INTO public.recursos
(recurso, grupoderecurso, codigo, descricao, tipo, centrodetrabalho, custohora, tenant, estabelecimento)
VALUES('c54cca2c-1468-4eb1-88a0-b16d891985bb'::uuid, NULL, '01', 'teste', 'posto_de_trabalho', NULL, 12.0, 1, '39836516-7240-4fe5-847b-d5ee0f57252d');
INSERT INTO public.recursos
(recurso, grupoderecurso, codigo, descricao, tipo, centrodetrabalho, custohora, tenant, estabelecimento)
VALUES('ed07dac5-8420-47f3-8464-3549a7c5ec88'::uuid, NULL, '02', 'teste1', 'equipamento', NULL, 10.0, 1,'39836516-7240-4fe5-847b-d5ee0f57252d');
INSERT INTO public.recursos
(recurso, grupoderecurso, codigo, descricao, tipo, centrodetrabalho, custohora, tenant, estabelecimento)
VALUES('01a1ba15-be5c-4e6e-85b2-3caa4b5de887'::uuid, NULL, '03', 'teste3', 'outros', NULL, NULL, 1,'39836516-7240-4fe5-847b-d5ee0f57252d');


--plantas
insert into plantas 
(planta, codigo, descricao, estabelecimento, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('8e94d551-af58-40f9-a660-8bea18224220', '01', 'planta 01', '39836516-7240-4fe5-847b-d5ee0f57252d', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br');
insert into plantas 
(planta, codigo, descricao, estabelecimento, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('061e5214-0091-47a5-957d-c6b4379ba98c', '02', 'planta 02', '39836516-7240-4fe5-847b-d5ee0f57252d', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br');

-- CENTRO DE TRABALHO
insert into centrosdetrabalhos 
(centrodetrabalho, codigo, descricao, planta, estabelecimento, responsavel, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('b4bd4419-fd6e-44ce-9e00-167d750ca8a1','01', 'centro de trabalho 01', '8e94d551-af58-40f9-a660-8bea18224220', '39836516-7240-4fe5-847b-d5ee0f57252d', 'Thiago Dias', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br' );

insert into centrosdetrabalhos 
(centrodetrabalho, codigo, descricao, planta, estabelecimento, responsavel, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('8119dce4-0a64-4bf4-b54f-529313a5e4ff', '02', 'centro de trabalho 02', '8e94d551-af58-40f9-a660-8bea18224220', '39836516-7240-4fe5-847b-d5ee0f57252d', 'Thiago Dias', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br' );

insert into centrosdetrabalhos 
(centrodetrabalho, codigo, descricao, planta, estabelecimento, responsavel, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('cfe427c0-6a2f-4ca3-a451-5854a1076c86','03', 'centro de trabalho 03', '061e5214-0091-47a5-957d-c6b4379ba98c', '39836516-7240-4fe5-847b-d5ee0f57252d', 'Thiago Dias', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br' );

insert into centrosdetrabalhos 
(centrodetrabalho, codigo, descricao, planta, estabelecimento, responsavel, tenant, criado_em, criado_por, atualizado_em, atualizado_por) VALUES
('c880713d-c16e-49c1-8f0c-b0649b77e772', '04', 'centro de trabalho 04', '061e5214-0091-47a5-957d-c6b4379ba98c', '39836516-7240-4fe5-847b-d5ee0f57252d', 'Thiago Dias', 1, current_timestamp, 'hugorabock@nasajon.com.br', current_timestamp, 'hugorabock@nasajon.com.br' );