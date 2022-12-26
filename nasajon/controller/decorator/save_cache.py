from enum import Enum, IntEnum
from tkinter import E
from typing import Any, Type
from flask import g, request

import redis
from nasajon.injector_factory import InjectorFactory
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_gcf_utils.json_util import json_loads, json_dumps

class CacheScope(IntEnum):
    TENANT = 0
    GRUPO_EMPRESARIAL = 1
    EMPRESA = 2
    ESTABELECIMENTO = 3


class SaveCache:

    def __init__(self, dto_class : Type[DTOBase], entity_class: Type[EntityBase], injector : Type[InjectorFactory], scope : CacheScope = CacheScope.TENANT) -> None:
        self._dto_class = dto_class
        self._entity_class = entity_class
        self._injector = injector
        self._scope = scope
    
    def __call__(self, func) -> Any:
        def wrapper(*args, **kwds):
            data = {}
            
            if request.method in ["GET", "DELETE"]:
                data = request.args
            elif request.method in ["POST", "PUT", "PATCH"]:
                data = request.get_json()
            else:
                data = request.args
            
            if 'tenant' not in data:
                raise Exception('Tenant não informado na requisição para cache')
            tenant = data.get("tenant")
            
            if self._scope == CacheScope.GRUPO_EMPRESARIAL:
                if 'grupo_empresarial' not in data:
                    raise Exception('Grupo empresarial não informado na requisição para cache')
                scope = data.get("grupo_empresarial")
            elif self._scope == CacheScope.EMPRESA:
                if 'empresa' not in data:
                    raise Exception('Empresa não informada na requisição para cache')
                scope = data.get("empresa")
            elif self._scope == CacheScope.ESTABELECIMENTO:
                if 'estabelecimento' not in data:
                    raise Exception('Estabelecimento não informado na requisição para cache')
                scope = data.get("estabelecimento")
                
            # email = g.profile['email']
            
            self._dto_class.resume_fields
            response =  func(*args, **kwds)
            # with self._injector() as i:
                # cache = i.cache_service()
                # cache.save_cache(email=email, scope=scope, tenant=tenant, data=response[0], dto_class=self._dto_class)
            return response
        return wrapper