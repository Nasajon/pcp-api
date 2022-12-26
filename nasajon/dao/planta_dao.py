from nasajon.dao.basic_dao import BasicDao
from nasajon.entity.planta_entity import PlantaEntity
from nsj_gcf_utils.db_adapter2 import DBAdapter2

class PlantaDao(BasicDao):
    def __init__(self, db: DBAdapter2):
        super().__init__(db, PlantaEntity)