from datetime import datetime
from uuid import UUID, uuid4
from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.dto.dto_base import DTOBase

@DTO()
class PlantaGetDTO(DTOBase):
    planta : UUID = DTOField(pk=True,resume=True)
    codigo : str = DTOField(not_null=True, resume=True)
    descricao : str = DTOField(not_null=True, resume=True)
    tenant : int = DTOField()
    estabelecimento : UUID = DTOField()
    
    
@DTO()
class PlantaPostDTO(DTOBase):
    planta : UUID = DTOField(pk=True, default_value=uuid4)
    codigo : str = DTOField(not_null=True, resume=True)
    descricao : str = DTOField(not_null=True, resume=True)
    estabelecimento : UUID = DTOField(not_null=True)
    tenant : int = DTOField(not_null=True)
    criado_em : datetime = DTOField(default_value=datetime.now)
    atualizado_em : datetime = DTOField(default_value=datetime.now)
    
@DTO()
class PlantaPutDTO(DTOBase):
    planta : UUID = DTOField(pk=True, not_null=True, default_value=uuid4)
    codigo : str = DTOField(not_null=True, resume=True)
    descricao : str = DTOField(not_null=True, resume=True)
    estabelecimento : UUID = DTOField(not_null=True)
    tenant : int = DTOField(not_null=True)
    atualizado_em : datetime = DTOField(default_value=datetime.now)