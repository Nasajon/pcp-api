from http.client import responses
from flask import request
from typing import Callable
from nasajon.controller.decorator.bulk_route import BulkRoute

from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.exception import DTOConfigException, MissingParameterException, NotFoundException
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nasajon.settings import CONTENT_TYPE_JSON_HEADER
from nsj_gcf_utils.json_util import json_dumps, json_loads, JsonLoadException
from nsj_gcf_utils.rest_error_util import format_json_error


class BulkPutRoute(BulkRoute):
    def __init__(
        self,
        url: str,
        http_method: str,
        dto_class: DTOBase,
        entity_class: EntityBase,
        dto_response_class: DTOBase = None,
        injector_factory: NsjInjectorFactoryBase = NsjInjectorFactoryBase,
        service_name: str = None,
        handle_exception: Callable = None,
        require_tenant: bool = True,
        require_grupo_emprearial: bool = True
    ):
        super().__init__(
            url=url,
            http_method=http_method,
            dto_class=dto_class,
            entity_class=entity_class,
            injector_factory=injector_factory,
            dto_response_class=dto_response_class,
            service_name=service_name,
            handle_exception=handle_exception,
            require_tenant=require_tenant,
            require_grupo_emprearial=require_grupo_emprearial,
        )

    def handle_request(self):
        response_result = {
            'global_status': "MULTI-STATUS",
            "response": []
        }


        with self._injector_factory() as factory:
            try:
               
                # Recuperando os dados do corpo da rquisição
                data = request.get_data(as_text=True)
                data = json_loads(data)
                status_codes = set()

                for request_item in data:
                    obj = request_item
                    try:    
                        pk_value = request_item[self._dto_class.pk_field]

                        response_item = {
                        "status" : 200, 
                        self._dto_class.pk_field: pk_value,
                        "body": {}
                        }

                        # Tratando do tenant e do grupo_empresarial
                        tenant = obj.get('tenant')
                        grupo_empresarial = obj.get('grupo_empresarial')

                        if self._require_tenant:
                            if tenant is None:
                                raise MissingParameterException('tenant')

                            if not ('tenant' in self._dto_class.fields_map):
                                raise DTOConfigException(
                                    f"Missing 'tenant' field declaration on DTOClass: {self._dto_class}")

                        if self._require_grupo_emprearial:
                            if grupo_empresarial is None:
                                raise MissingParameterException('grupo_empresarial')

                            if not ('grupo_empresarial' in self._dto_class.fields_map):
                                raise DTOConfigException(
                                    f"Missing 'grupo_empresarial' field declaration on DTOClass: {self._dto_class}")

                        # Convertendo os dados para o DTO
                        obj = self._dto_class(**obj)

                        partition_filters = {}

                        if tenant is not None:
                            partition_filters['tenant'] = tenant

                        if grupo_empresarial is not None:
                            partition_filters['grupo_empresarial'] = grupo_empresarial
                        
                        
                        # Construindo os objetos
                        service = self._get_service(factory)

                        # Chamando o service (método insert)
                        obj = service.update(obj, pk_value, partition_filters)

                        if obj is not None:
                            # Convertendo para o formato de dicionário (permitindo omitir campos do DTO)
                            dict_obj = obj.convert_to_dict()
                            response_item['body'] = dict_obj
                            # Retornando a resposta da requuisição
                            response_result = self._add_response_list(response_result, response_item, 200, status_codes=status_codes)
                        else:
                            # Retornando a resposta da requuisição
                            response_item['body'] = {}
                            response_result = self._add_response_list(response_result, response_item, 204, status_codes=status_codes)
                        
                    except JsonLoadException as e:
                            response_result = self._add_response_list(response_result, response_item, 400, e, request_item, status_codes=status_codes)
                    except MissingParameterException as e:
                            response_result = self._add_response_list(response_result, response_item, 400, e, request_item, status_codes=status_codes)
                    except ValueError as e:
                            response_result = self._add_response_list(response_result, response_item, 400, e, request_item, status_codes=status_codes)
                    except NotFoundException as e:
                            response_result = self._add_response_list(response_result, response_item, 404, e, request_item, status_codes=status_codes)
                    except Exception as e:
                            response_result = self._add_response_list(response_result, response_item, 500, e, request_item, status_codes=status_codes)
                            
            except Exception as e :
                return (format_json_error(e), 500, CONTENT_TYPE_JSON_HEADER)       


            if len(status_codes) == 0:
                status_code = 400
            elif len(status_codes) > 1:
                status_code = 207
            else:
                status_code = status_codes.pop()
            
            
            response_result['global_status'] = responses[status_code]
            return (json_dumps(response_result), status_code, CONTENT_TYPE_JSON_HEADER)


