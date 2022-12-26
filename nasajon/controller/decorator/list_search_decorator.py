from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.controller.route_base import RouteBase
from nasajon.util.request_util import RequestValidator, RequestParserNsjApiUtil
from nasajon.injector_factory import InjectorFactory
from nsj_gcf_utils.json_util import json_dumps, json_loads
from nsj_gcf_utils.rest_error_util import format_json_error
from nasajon.settings import CONTENT_TYPE_JSON_HEADER, DEFAULT_PAGE_SIZE
from nsj_gcf_utils.pagination_util import page_body
from flask import g, request
from nsj_rest_lib.exception import DTOConfigException, MissingParameterException
from nsj_rest_lib.service.service_base import ServiceBase
import logging

from typing import Any, Dict, Type



class ListSearchRoute(RouteBase):

    def __init__(self, url, method, dto_class: DTOBase, entity_class: EntityBase, factory: Type[InjectorFactory], service_name = None, 
                 require_estabelecimento: bool = True) -> None:
        super().__init__(
            url=url,
            http_method=method,
            dto_class=dto_class,
            entity_class=entity_class,
            dto_response_class=None,
            injector_factory=factory,
            service_name=service_name,
            handle_exception=None,
            require_tenant=True,
            require_grupo_emprearial=False,
        )
        self._require_estabelecimento=require_estabelecimento
    def handle_request(self) -> Any:
        try:
            
            RequestValidator.validate_tenant_args(request.args)
            args = request.args
            fields = RequestParserNsjApiUtil.str_args_to_nsj_api_fields(args.get('fields'), self._dto_class)
            current_after = args.get('after')
            offset = int(args.get('offset', 0))
            limit = RequestParserNsjApiUtil.args_to_limit(args)
            tenant = args.get('tenant')
            grupo_empresarial = args.get('grupo_empresarial')
            estabelecimento = args.get('estabelecimento')
            scope = ''
            
            for_search = False
          
            
            if 'search' in request.args:
                filters = RequestParserNsjApiUtil.args_to_search(args.get('search'), args, self._dto_class)
                for_search = True
            else:
                filters = RequestParserNsjApiUtil.args_to_filters(args)
         
            # if (filters == {} and 'search' not in args ):
                # use_cache = True
                
            if self._require_tenant:
                if tenant is None:
                    raise MissingParameterException('tenant')

                if not ('tenant' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'tenant' field declaration on DTOClass: {self._dto_class}")

                filters['tenant'] = tenant
                scope = tenant

            if self._require_grupo_emprearial:
                if grupo_empresarial is None:
                    raise MissingParameterException('grupo_empresarial')

                if not ('grupo_empresarial' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'grupo_empresarial' field declaration on DTOClass: {self._dto_class}")
                scope = grupo_empresarial
                filters['grupo_empresarial'] = grupo_empresarial
                
                
                             
            if self._require_estabelecimento:
                if estabelecimento is None:
                    raise MissingParameterException('estabelecimento')
                
                if not ('estabelecimento' in self._dto_class.fields_map):
                    raise DTOConfigException(
                        f"Missing 'estabelecimento' field declaration on DTOClass: {self._dto_class}")
                filters['estabelecimento'] = estabelecimento
                scope = estabelecimento
                
                
            with self._injector_factory() as injector:
               
                
                if self._service_name is not None:
                    service = injector.get_service_by_name(self._service_name)
                else:
                    service = self._get_service(injector)
                    
                dict_data = service.list(None, limit, fields, None, filters, for_search, offset)
                    
                data = [dto.convert_to_dict(fields) for dto in dict_data]

                page = page_body(
                        base_url=request.base_url,
                        limit=limit,
                        current_after=current_after,
                        current_before=None,
                        result=data,
                        id_field= self._dto_class.pk_field
                    )


            response =  (json_dumps(page), 200 , CONTENT_TYPE_JSON_HEADER) 
        except MissingParameterException as e:
            response =  (format_json_error(e), 400, CONTENT_TYPE_JSON_HEADER)
        except Exception as e:
            response =  (format_json_error(e), 500, CONTENT_TYPE_JSON_HEADER)
        return response
    
    
    def get_history_from_cache(self, tenant, scope, service : ServiceBase, filters: Dict[str, Any], injector):
        if not hasattr(injector, 'get_cache'):
            return 
        cache = injector.get_cache()
        email = g.profile['email']
        
        key = f'{email}-{tenant}-{scope}-{self._entity_class.__name__}'
        
        list_txt = cache.get_list(key)
        list = []
        
        if list_txt is not None or list_txt != '':
            list_keys = json_loads(list_txt)
            
        fields_map = {}
        fields_map.setdefault('root', self._dto_class.resume_fields)
        list_keys.reverse()
        result = []
        for key in list_keys:
            filters_temp = filters.copy()
            filters_temp[self._dto_class.pk_field] = key
            obj_list = service.list(None, 1, fields_map, None, filters_temp)
            result.append(obj_list[0])
        
        return result
                
            
            
            