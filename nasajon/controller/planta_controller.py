from nasajon.settings import MOPE_CODE, CONTENT_TYPE_JSON_HEADER
from nasajon.dto.planta import PlantaPostDTO, PlantaGetDTO, PlantaPutDTO
from nasajon.entity.planta_entity import PlantaEntity
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nasajon.controller.decorator.delete_route import DeleteRoute
from nasajon.controller.decorator.save_cache import SaveCache, CacheScope
from nasajon.injector_factory import InjectorFactory
from nasajon.services.planta_service import PlantaService
from nasajon.controller.decorator.list_search_decorator import ListSearchRoute
from nsj_gcf_utils.json_util import json_dumps, json_loads
from nasajon.wsgi import application

RESOURCE_ROUTE = f'/{MOPE_CODE}/plantas'
RECENTS_ROUTE = f'/{MOPE_CODE}/plantas/recents'
RESOURCE_ID_ROUTE = f'/{MOPE_CODE}/plantas/<id>'

@application.route(RESOURCE_ROUTE, methods=['GET'])
@ListSearchRoute(
    url=RESOURCE_ROUTE,
    method='GET',
    dto_class=PlantaGetDTO,
    entity_class=PlantaEntity,
    factory=InjectorFactory, 
    service_name=PlantaService
)
def get_list(request, response):
    data = json_loads(response[0])
    if 'result' in data:
        return (json_dumps(data['result']),response[1],response[2])
    return response

@application.route(RESOURCE_ID_ROUTE, methods=['GET'])
@GetRoute(
    url=RESOURCE_ID_ROUTE,
    http_method='GET',
    dto_class=PlantaGetDTO,
    entity_class=PlantaEntity,
    require_grupo_emprearial=False
)
@SaveCache(PlantaGetDTO, PlantaEntity,  InjectorFactory, CacheScope.ESTABELECIMENTO)
def get(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 


@application.route(RESOURCE_ROUTE, methods=['POST'])
@PostRoute(
    url=RESOURCE_ROUTE,
    http_method='POST',
    dto_class=PlantaPostDTO,
    entity_class=PlantaEntity,
    require_grupo_emprearial=False,
    dto_response_class=PlantaGetDTO
)
def post(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 

@application.route(RESOURCE_ID_ROUTE, methods=['PUT'])
@PutRoute(
    url=RESOURCE_ID_ROUTE,
    http_method='PUT',
    dto_class=PlantaPutDTO,
    entity_class=PlantaEntity,
    require_grupo_emprearial=False,
    dto_response_class=PlantaGetDTO
)
def put(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 


@application.route(RESOURCE_ID_ROUTE, methods=['DELETE'])
@DeleteRoute(
    url=RESOURCE_ID_ROUTE,
    http_method='PUT',
    dto_class=PlantaPutDTO,
    entity_class=PlantaEntity,
    require_grupo_emprearial=False,
    dto_response_class=PlantaGetDTO,
    injector_factory=InjectorFactory
)
def delete(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 