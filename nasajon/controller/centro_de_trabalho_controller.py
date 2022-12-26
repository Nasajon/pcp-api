from nasajon.settings import MOPE_CODE, CONTENT_TYPE_JSON_HEADER
from nasajon.dto.centro_de_trabalho import CentroDeTrabalhoGetDTO, CentroDeTrabalhoPostDTO, CentroDeTrabalhoPutDTO
from nasajon.entity.centro_de_trabalho_entity import CentroDeTrabalhoEntity
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nasajon.controller.decorator.delete_route import DeleteRoute
from nasajon.controller.decorator.save_cache import SaveCache, CacheScope
from nasajon.injector_factory import InjectorFactory
from nasajon.services.centro_de_trabalho_service import CentroDeTrabalhoService
from nasajon.controller.decorator.list_search_decorator import ListSearchRoute
from nsj_gcf_utils.json_util import json_dumps, json_loads
from nasajon.wsgi import application

RESOURCE_ROUTE = f'/{MOPE_CODE}/centrosdetrabalhos'
RECENTS_ROUTE = f'/{MOPE_CODE}/centrosdetrabalhos/recents'
RESOURCE_ID_ROUTE = f'/{MOPE_CODE}/centrosdetrabalhos/<id>'

@application.route(RESOURCE_ROUTE, methods=['GET'])
@ListSearchRoute(
    url=RESOURCE_ROUTE,
    method='GET',
    dto_class=CentroDeTrabalhoGetDTO,
    entity_class=CentroDeTrabalhoEntity,
    factory=InjectorFactory, 
    service_name=CentroDeTrabalhoService
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
    dto_class=CentroDeTrabalhoGetDTO,
    entity_class=CentroDeTrabalhoEntity,
    require_grupo_emprearial=False
)
@SaveCache(CentroDeTrabalhoGetDTO, CentroDeTrabalhoEntity,  InjectorFactory, CacheScope.ESTABELECIMENTO)
def get(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 


@application.route(RESOURCE_ROUTE, methods=['POST'])
@PostRoute(
    url=RESOURCE_ROUTE,
    http_method='POST',
    dto_class=CentroDeTrabalhoPostDTO,
    entity_class=CentroDeTrabalhoEntity,
    require_grupo_emprearial=False,
    dto_response_class=CentroDeTrabalhoGetDTO
)
def post(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 

@application.route(RESOURCE_ID_ROUTE, methods=['PUT'])
@PutRoute(
    url=RESOURCE_ID_ROUTE,
    http_method='PUT',
    dto_class=CentroDeTrabalhoPutDTO,
    entity_class=CentroDeTrabalhoEntity,
    require_grupo_emprearial=False,
    dto_response_class=CentroDeTrabalhoGetDTO
)
def put(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 


@application.route(RESOURCE_ID_ROUTE, methods=['DELETE'])
@DeleteRoute(
    url=RESOURCE_ID_ROUTE,
    http_method='PUT',
    dto_class=CentroDeTrabalhoPutDTO,
    entity_class=CentroDeTrabalhoEntity,
    require_grupo_emprearial=False,
    dto_response_class=CentroDeTrabalhoGetDTO,
    injector_factory=InjectorFactory
)
def delete(request, response):
    return (response[0], response[1] , CONTENT_TYPE_JSON_HEADER) 