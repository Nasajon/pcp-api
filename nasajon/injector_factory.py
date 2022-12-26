from typing import Type
from sqlalchemy.engine.base import Connection
from nasajon.dao.planta_dao import PlantaDao
from nasajon.dao.centro_de_trabalho_dao import CentroDeTrabalhoDao

from nsj_rest_lib.service.service_base import ServiceBase
from nsj_rest_lib.dao.dao_base import DAOBase
from nasajon.services.centro_de_trabalho_service import CentroDeTrabalhoService
from nasajon.services.planta_service import PlantaService
class InjectorFactory:
    _db_connection: Connection

    
    def __init__(self) -> None:
        self.services = {
            PlantaService.__name__ : self.planta_service,
            CentroDeTrabalhoService.__name__: self.centro_de_trabalho_service
        }
    def __enter__(self):
        from nasajon.db_pool_config import db_pool
        self._db_connection = db_pool.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()

    def db_adapter(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2
        return DBAdapter2(self._db_connection)
    
    def planta_dao(self):
        return PlantaDao(self.db_adapter())
    
    def centro_de_trabalho_dao(self):
        return CentroDeTrabalhoDao(self.db_adapter())

    def planta_service(self):
        return PlantaService(self, self.planta_dao())
    
    # def cache_service(self):
    #     from nasajon.service.cache_service import CacheService
    #     return CacheService()
    # DAOs
    def centro_de_trabalho_service(self):
        return CentroDeTrabalhoService(self, self.centro_de_trabalho_dao())


    def get_service_by_name(self, clazz: Type):
        if not clazz.__name__ in self.services:
            raise Exception(f'Service not found: {clazz.__name__}')

        service_method = self.services[clazz.__name__]

        return service_method()

    def get_service_by_class_ns_api(self, dto_class : Type, entity_class : Type, dto_response_class: Type = None) -> ServiceBase:
            return ServiceBase(
                        self,
                        DAOBase(self.db_adapter(), entity_class),
                        dto_class,
                        entity_class,
                        dto_response_class)   