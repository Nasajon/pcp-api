from datetime import datetime
from typing import List
from uuid import UUID
from nsj_rest_lib.entity.entity_base import EntityBase


class CentroDeTrabalhoEntity(EntityBase):
    centrodetrabalho : UUID
    codigo : str 
    descricao : str 
    responsavel : str
    planta : UUID
    atualizado_por : str
    criado_por : str
    atualizado_em : datetime
    criado_em : datetime
    tenant : int
    estabelecimento: UUID
    
    def __init__(self) -> None:
        super().__init__()
        self.centrodetrabalho = None
        self.codigo = None
        self.descricao = None
        self.responsavel = None
        self.planta = None
        self.atualizado_por = None
        self.criado_por = None
        self.atualizado_em = None
        self.criado_em = None
        self.tenant = None
        self.estabelecimento = None
        
    def get_table_name(self) -> str:
        return 'centrosdetrabalhos'

    def get_pk_field(self) -> str:
        return 'centrodetrabalho'

    
    def get_pk_column_name(self) -> str:
        return 'centrodetrabalho'

    def get_default_order_fields(self) -> List[str]:
        return ['codigo', 'tenant']
