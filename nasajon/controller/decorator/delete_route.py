from typing import Any, Callable, Type
from flask import request
from nsj_rest_lib.controller.route_base import RouteBase
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nasajon.util.request_util import RequestValidator

from nsj_rest_lib.exception import DTOConfigException, MissingParameterException, NotFoundException
from nasajon.settings import CONTENT_TYPE_JSON_HEADER
from nsj_gcf_utils.rest_error_util import format_json_error

class DeleteRoute(RouteBase):
    def __init__(
        self,
        url: str,
        http_method: str,
        dto_class: DTOBase,
        entity_class: EntityBase,
        dto_response_class: DTOBase = None,
        injector_factory: Type[NsjInjectorFactoryBase] = NsjInjectorFactoryBase,
        service_name: str = None,
        handle_exception: Callable = None,
        require_tenant: bool = True,
        require_grupo_emprearial=True, 
        require_estabelecimento=True
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
        self.require_estabelecimento = require_estabelecimento
    
    def handle_request(self, id) -> Any:
        try:
            RequestValidator.validate_tenant_args(request.args)
            args = request.args
            tenant = args.get('tenant')
            grupo_empresarial = args.get('grupo_empresarial')
            estabelecimento =   args.get('estabelecimento')

            filters = {}
            if self._require_tenant:
                if tenant is None:
                    raise MissingParameterException('tenant')

                if not ('tenant' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'tenant' field declaration on DTOClass: {self._dto_class}")
                filters = {'tenant' : tenant}

            if self._require_grupo_emprearial:
                if grupo_empresarial is None:
                    raise MissingParameterException('grupo_empresarial')

                if not ('grupo_empresarial' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'grupo_empresarial' field declaration on DTOClass: {self._dto_class}")

                filters = {'grupoempresarial' : grupo_empresarial}
                
            if self.require_estabelecimento:
                if estabelecimento is None:
                    raise MissingParameterException('estabelecimento')

                if not ('estabelecimento' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'estabelecimento' field declaration on DTOClass: {self._dto_class}")

                filters = {'estabelecimento' : estabelecimento}

            with self._injector_factory() as injector:

                if self._service_name is not None:
                    service = injector.get_service_by_name(self._service_name)
                else:
                    service = self._get_service(injector)

                service.delete(id, filters)

            response =  ({}, 204 , CONTENT_TYPE_JSON_HEADER) 
        except MissingParameterException as e:
            response =  (format_json_error(e), 400, CONTENT_TYPE_JSON_HEADER)
        except NotFoundException as e:
            response =  (format_json_error(e), 404, CONTENT_TYPE_JSON_HEADER)
        except Exception as e:
            response =  (format_json_error(e), 500, CONTENT_TYPE_JSON_HEADER)
        return response