from typing import Any, Callable, Set
from flask import request
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nasajon.util.request_util import RequestValidator
from http.client import responses

from nasajon.controller.decorator.bulk_route import BulkRoute
from nsj_rest_lib.exception import DTOConfigException, MissingParameterException, NotFoundException
from nsj_gcf_utils.json_util import JsonLoadException, json_dumps, json_loads
from nsj_gcf_utils.rest_error_util import format_json_error
from nasajon.settings import CONTENT_TYPE_JSON_HEADER


class BulkDeleteRoute(BulkRoute):
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
        require_grupo_emprearial=True
    ):
        super().__init__(
            url=url,
            http_method=http_method,
            dto_class=dto_class,
            entity_class=entity_class,
            dto_response_class=dto_response_class,
            injector_factory=injector_factory,
            service_name=service_name,
            handle_exception=handle_exception,
            require_tenant=require_tenant,
            require_grupo_emprearial=require_grupo_emprearial
        )

    def handle_request(self) -> Any:
        try:
            
            response_result = {
            'global_status': "MULTI-STATUS",
            "response": []
            }

            status_codes = set()

            data = request.get_data(as_text=True)
            data = json_loads(data)

            for dto_item in data:
                try:
                    response_item = {
                        "status" : 204, 
                        self._dto_class.pk_field: dto_item.get(self._dto_class.pk_field),
                        "body": {}
                    }

                    tenant = dto_item.get('tenant')
                    grupo_empresarial = dto_item.get('grupo_empresarial')


                    filters = {}
                    if self._require_tenant:
                        RequestValidator.validate_tenant_args(request.args)
                        if tenant is None:
                            raise MissingParameterException('tenant')

                        if not ('tenant' in self._dto_class.fields_map):
                            raise DTOConfigException(
                                f"Missing 'tenant' field declaration on DTOClass: {self._dto_class}")
                        filters.update({'tenant' : tenant})

                    if self._require_grupo_emprearial:
                        RequestValidator.validate_grupo_empresarial_args(request.args)

                        if not ('grupo_empresarial' in self._dto_class.fields_map):
                            raise DTOConfigException(
                                f"Missing 'grupo_empresarial' field declaration on DTOClass: {self._dto_class}")

                        filters.update({'grupoempresarial' : grupo_empresarial})
                    
                    with self._injector_factory() as injector:

                        if self._service_name is not None:
                            service = injector.get_service_by_name(self._service_name)
                        else:
                            service = self._get_service(injector)

                        service.delete(dto_item.get(self._dto_class.pk_field), filters)

                    response_item['body'] = {}
                    response_result = self._add_response_list(response_result, response_item, 204, status_codes=status_codes)

                except JsonLoadException as e:
                        response_result = self._add_response_list(response_result, response_item, 400, e, status_codes=status_codes)
                except MissingParameterException as e:
                        response_result = self._add_response_list(response_result, response_item, 400, e, status_codes=status_codes)
                except ValueError as e:
                        response_result = self._add_response_list(response_result, response_item,400,  e, status_codes=status_codes)
                except NotFoundException as e:
                        response_result = self._add_response_list(response_result, response_item,404,  e, status_codes=status_codes)
                except Exception as e:
                        response_result = self._add_response_list(response_result, response_item,500, e, status_codes=status_codes)
        except Exception as e:
            return (format_json_error(e), 500, CONTENT_TYPE_JSON_HEADER)
        
        if len(status_codes) == 0:
            status_code = 400
        elif len(status_codes) > 1:
            status_code = 207
        else:
            status_code = status_codes.pop()
        
        
        response_result['global_status'] = responses[status_code]
        return (json_dumps(response_result), status_code, CONTENT_TYPE_JSON_HEADER)
