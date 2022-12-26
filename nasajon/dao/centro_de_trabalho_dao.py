from nasajon.dao.basic_dao import BasicDao
from nasajon.entity.centro_de_trabalho_entity import CentroDeTrabalhoEntity
from nsj_gcf_utils.db_adapter2 import DBAdapter2

class CentroDeTrabalhoDao(BasicDao):
    def __init__(self, db: DBAdapter2):
        super().__init__(db, CentroDeTrabalhoEntity)