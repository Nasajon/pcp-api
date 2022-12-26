from nsj_rest_lib.dao.dao_base import DAOBase
from nasajon.services.basic_service import BasicService
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nasajon.entity.planta_entity import PlantaEntity
from nasajon.dto.planta import PlantaGetDTO

class PlantaService(BasicService):
    
    def __init__(self, injector_factory: NsjInjectorFactoryBase, dao: DAOBase):
        super().__init__(injector_factory, dao, PlantaGetDTO, PlantaEntity, PlantaGetDTO)
        