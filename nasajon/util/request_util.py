from __future__ import nested_scopes
from typing import Any, Dict, List, Set
import re
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.exception import  MissingParameterException
from nasajon.settings import DEFAULT_PAGE_SIZE

class RequestParserNsjApiUtil:

    @staticmethod
    def str_args_to_nsj_api_fields(fields, dto: DTOBase) -> dict[str, str]:
        if fields is None:
            fields_map = {}
            fields_map.setdefault('root', dto.resume_fields)
            return fields_map

        fields = fields.split(',')

        matcher_dot = re.compile('(.+)\.(.+)')
        matcher_par = re.compile('(.+)\((.+)\)')

        # Construindo o mapa de retorno
        fields_map = {}

        # Iterando cada field recebido
        for field in fields:
            field = field.strip()

            match_dot = matcher_dot.match(field)
            match_par = matcher_par.match(field)

            if match_dot is not None:
                # Tratando fields=entidade_aninhada.propriedade
                key = match_dot.group(1)
                value = match_dot.group(2)

                # Adicionando a propriedade do objeto interno as campos root
                root_field_list = fields_map.setdefault('root', set())
                if not key in root_field_list:
                    root_field_list.add(key)

                field_list = fields_map.setdefault(key, set())
                field_list.add(value)
            elif match_par is not None:
                # Tratando fields=entidade_aninhada(propriedade1, propriedade2)
                key = match_dot.group(1)
                value = match_dot.group(2)

                field_list = fields_map.setdefault(key, set())

                # Adicionando a propriedade do objeto interno as campos root
                root_field_list = fields_map.setdefault('root', set())
                if not key in root_field_list:
                    root_field_list.add(key)

                # Tratando cada campo dentro do parêntese
                for val in value.split(','):
                    val = val.strip()

                    field_list.add(val)
            else:
                # Tratando propriedade simples (sem entidade aninhada)
                root_field_list = fields_map.setdefault('root', set())
                root_field_list.add(field)

        return fields_map

    @staticmethod
    def args_to_filters(args: Dict[str, str]):
        filters = {}
        for arg in args:
            if arg in ['limit', 'after', 'offset', 'fields', 'tenant', 'grupo_empresarial', 'estabelecimento']:
                continue

            filters[arg] = args.get(arg)
        return filters

    def args_to_limit(args: Dict[str, str]):
        return int(args.get('limit', DEFAULT_PAGE_SIZE))

    @staticmethod
    def args_to_search(search_text : str, args: Dict[str, str], dto : DTOBase):
        result = {}
        for field in dto.resume_fields:
            if dto.__annotations__[field] == str:
                result[field] = search_text
        return result
    



class RequestValidator:
    @staticmethod
    def validate_tenant_args(args : Dict[str, str]):
        if args is None or 'tenant' not in args or args.get('tenant').strip() == '':
            raise MissingParameterException('tenant')


    @staticmethod
    def validate_grupo_empresarial_args(args : Dict[str, str]):
        if args is None or 'grupo_empresarial' not in args or args.get('grupo_empresarial').strip() == '':
            raise MissingParameterException('grupo_empresarial')
        


    @staticmethod
    def validate_tenant_json(json : Any):
        if json is None or 'tenant' not in json or json['tenant'].strip() == '':
            raise MissingParameterException('tenant')

    @staticmethod
    def validate_grupo_empresarial_json(json : Any):
        if json is None or 'grupo_empresarial' not in json or json['grupo_empresarial'].strip() == '':
            raise MissingParameterException('grupo_empresarial')

class RequestFieldsDictParser:

    @staticmethod
    def dict_object_single_fields_to_str(args: Dict[str, str]):
        result = []
        for key in args:
            if args[key] == {} or type(args[key]) != dict:
                result.append(key)

        return ",".join(result)
            

    @staticmethod
    def dict_args_to_dict_fields(args: Dict[str, str]) -> Dict[str, str]:
        result ={}
        if 'fields' in args:
            fields = args.get('fields')
            fields = fields.split(',')
        for field in fields:
            if '.' in field:
                fields_nested = field.strip().split('.')
                nested_dict = result
                for nested_field in fields_nested:
                    nested_dict = RequestFieldsDictParser._extract_nested_dict(nested_field.strip(), nested_dict)
                continue
            result[field] = {}
        return result
    
    @staticmethod
    def dict_object_nesteds_to_str( entity: str, object_dict):
        if entity in object_dict:
            keys = RequestFieldsDictParser._extract_nested_fields_recursive(object_dict[entity])
        return ",".join(keys)
    
    @staticmethod
    def _extract_nested_dict(field: str, dict_result = {}):
        if field not in dict_result:
            dict_result[field] = {}
        return dict_result[field]
    @staticmethod
    def _extract_nested_fields_recursive( nested_dict: Dict[str, str]):
        result = []
        for key in nested_dict.keys():
            inner_keys = RequestFieldsDictParser._extract_nested_fields_recursive(nested_dict[key])
            
            if len(inner_keys) <= 0:
                result.append(key)
                continue

            for inner_key in inner_keys:
                result.append(f'{key}.{inner_key}')
            
        return result