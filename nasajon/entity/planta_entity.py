from datetime import datetime
from typing import List
from uuid import UUID
from nsj_rest_lib.entity.entity_base import EntityBase


class PlantaEntity(EntityBase):
    planta : UUID
    codigo : str 
    descricao : str
    estabelecimento : UUID 
    tenant : int 
    atualizado_por : str
    criado_por : str
    atualizado_em : datetime
    criado_em : datetime
    
    def __init__(self) -> None:
        super().__init__()
        self.planta = None
        self.codigo = None
        self.descricao = None
        self.estabelecimento = None
        self.tenant = None
        self.atualizado_por = None
        self.criado_por = None
        self.atualizado_em = None
        self.criado_em = None
        
        
    def get_table_name(self) -> str:
        return 'plantas'

    def get_pk_field(self) -> str:
        return 'planta'

    
    def get_pk_column_name(self) -> str:
        return 'planta'

    def get_default_order_fields(self) -> List[str]:
        return ['codigo', 'tenant']