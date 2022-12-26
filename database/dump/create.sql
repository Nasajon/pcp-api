
drop table if exists gruposderecursos;

CREATE TABLE gruposderecursos (
	grupoderecurso uuid NOT NULL,
	codigo varchar(30) NULL,
	descricao varchar(60) NULL,
	tipo varchar(30) NULL,
	tenant int4 NULL,
    estabelecimento uuid, 
    criado_em timestamp,
    criado_por varchar(150) ,
    atualizado_em timestamp,
    atualizado_por varchar(150),
	CONSTRAINT gruposderecursos_pkey PRIMARY KEY (grupoderecurso, tenant)
);


drop table if exists plantas;
create table plantas (
    planta uuid,
    codigo varchar(30), 
    descricao varchar(60),
    estabelecimento uuid, 
    tenant int, 
    criado_em timestamp,
    criado_por varchar(150) ,
    atualizado_em timestamp,
    atualizado_por varchar(150),
    CONSTRAINT plantas_pkey PRIMARY KEY (planta, tenant)
);


drop table if exists centrosdetrabalhos;

create table centrosdetrabalhos (
    centrodetrabalho uuid , 
    codigo varchar(30), 
    descricao varchar(60), 
    planta uuid, 
    estabelecimento uuid,
    responsavel varchar(60),
    criado_em timestamp,
    criado_por varchar(150) ,
    atualizado_em timestamp,
    tenant int4,
    atualizado_por varchar(150),
    CONSTRAINT centrodetrabalho_pkey PRIMARY KEY (centrodetrabalho, tenant),
    foreign key (planta, tenant) references plantas(planta, tenant)
);


drop table if exists recursos;

CREATE TABLE recursos (
    recurso uuid,  
	grupoderecurso uuid,
	codigo varchar(30) ,
	descricao varchar(60) ,
	tipo varchar(30) ,
    centrodetrabalho uuid, 
    custohora float, 
	tenant int4,
    estabelecimento uuid, 
    criado_em timestamp,
    criado_por varchar(150) ,
    atualizado_em timestamp,
    atualizado_por varchar(150),
    CONSTRAINT recurso_pkey PRIMARY KEY (recurso, tenant),
    foreign key (grupoderecurso, tenant) references gruposderecursos(grupoderecurso, tenant)
);