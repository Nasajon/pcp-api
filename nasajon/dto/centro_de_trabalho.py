from datetime import datetime
from uuid import UUID, uuid4
from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.dto.dto_base import DTOBase

@DTO()
class CentroDeTrabalhoGetDTO(DTOBase):
    centrodetrabalho : UUID = DTOField(pk=True, resume=True)
    codigo : str =  DTOField(max=30, not_null=True, resume=True)
    descricao : str =  DTOField(max=60, not_null=True, resume=True)
    responsavel : str = DTOField(max=60, not_null=True, resume=True)
    estabelecimento : UUID = DTOField()
    planta : UUID = DTOField()
    tenant : int = DTOField()


@DTO()
class CentroDeTrabalhoPostDTO(DTOBase):
    centrodetrabalho : UUID = DTOField(pk=True, default_value=uuid4)
    codigo : str = DTOField(max=30, not_null=True, resume=True)
    descricao : str = DTOField(max=60, not_null=True, resume=True)
    responsavel : str = DTOField(max=30, not_null=True, resume=True)
    planta : UUID = DTOField(not_null=True)
    tenant : int = DTOField(not_null=True)
    estabelecimento : UUID = DTOField(not_null=True)
    criado_em : datetime = DTOField(default_value=datetime.now)
    atualizado_em : datetime = DTOField(default_value=datetime.now)
    
    
    
@DTO()
class CentroDeTrabalhoPutDTO(DTOBase):
    centrodetrabalho : UUID = DTOField(pk=True)
    codigo : str = DTOField(max=30, not_null=True, resume=True)
    descricao : str = DTOField(max=60, not_null=True, resume=True)
    responsavel : str = DTOField(max=30, not_null=True, resume=True)
    planta : UUID = DTOField(not_null=True)
    estabelecimento : UUID = DTOField(not_null=True)
    tenant : int = DTOField(not_null=True)
    atualizado_em : datetime = DTOField(default_value=datetime.now)