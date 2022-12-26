from nasajon.dto.centro_de_trabalho import CentroDeTrabalhoGetDTO
from nasajon.entity.centro_de_trabalho_entity import CentroDeTrabalhoEntity
from nsj_rest_lib.dao.dao_base import DAOBase
from nasajon.services.basic_service import BasicService
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nasajon.services.basic_service import BasicService

class CentroDeTrabalhoService(BasicService):
    def __init__(self, injector_factory: NsjInjectorFactoryBase, dao: DAOBase):
        super().__init__(injector_factory, dao, CentroDeTrabalhoGetDTO, CentroDeTrabalhoEntity, CentroDeTrabalhoGetDTO)
        