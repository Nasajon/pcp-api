from abc import abstractmethod
from typing import Any, Dict, List, Set
from nsj_rest_lib.service.service_base import ServiceBase

from nsj_rest_lib.entity.filter import Filter, FilterOperator
from nsj_rest_lib.dto.dto_base import DTOFieldFilter
import uuid

class BasicService(ServiceBase):

    def list(self,
        after: uuid.UUID,
        limit: int,
        fields: Dict[str, Set[str]],
        order_fields: List[str],
        filters: Dict[str, Any], 
        for_search : bool = False, 
        offset: int = None
        ):

        if not for_search:
            return super().list(after, limit, fields, order_fields, filters, offset)
            
        return self.list_search(after, limit, fields, order_fields, filters, offset)


    def list_search(self,
        after: uuid.UUID,
        limit: int,
        fields: Dict[str, Set[str]],
        order_fields: List[str],
        filters: Dict[str, Any],
        offset: int = None
        ):

        fields = self._resolving_fields(fields)

        # Handling the fields to retrieve
        entity_fields = self._convert_to_entity_fields(fields['root'])

        # Handling order fields
        order_fields = self._convert_to_entity_fields(order_fields)

        # Handling filters
        all_filters = {}
        if filters is not None:
            all_filters.update(filters)
        if self._dto_class.fixed_filters is not None:
            all_filters.update(self._dto_class.fixed_filters)

        entity_filters = self._create_entity_filters_for_search(all_filters)

        entity_list = self._dao.list_search(after, limit, entity_fields, order_fields, entity_filters, offset)    

        # Convertendo para uma lista de DTOs
        # dto_list = [self._dto_class().convert_from_entity(entity)
        #             for entity in entity_list]
        dto_list = [self._dto_class(entity) for entity in entity_list]

        # Retrieving related lists
        if len(self._dto_class.list_fields_map) > 0:
            self._retrieve_related_lists(dto_list, fields)

        # Returning
        return dto_list

    def _create_entity_filters_for_search(self, filters: Dict[str, Any]) -> Dict[str, List[Filter]]:
        """
        Converting DTO filters to Entity filters.

        Returns a Dict (indexed by entity field name) of List of Filter.
        """

        if filters is None:
            return None

        entity_filters = {}
        for filter in filters:

            is_entity_filter = False
            if filter in self._dto_class.field_filters_map:
                # Retrieving filter config
                field_filter = self._dto_class.field_filters_map[filter]
            elif filter in self._dto_class.fields_map:
                # Creating filter config to a DTOField (equals operator)
                field_filter = DTOFieldFilter(filter, FilterOperator.ILIKE)
                field_filter.set_field_name(filter)
            # TODO Refatorar para usar um mapa de fields do entity
            elif filter in self._entity_class().__dict__:
                is_entity_filter = True
            else:
                # Ignoring not declared filters (or filter for not existent DTOField)
                continue

            # Resolving entity field name (to filter)
            if not is_entity_filter:
                entity_field_name = self._convert_to_entity_field(
                    field_filter.field_name)
            else:
                entity_field_name = filter

            # Creating entity filters (one for each value - separated by comma)
            if isinstance(filters[filter], str):
                values = filters[filter].split(',')
            else:
                values = [filters[filter]]

            for value in values:
                if isinstance(value, str):
                    value = f'%{value.strip()}%'

                if not is_entity_filter:
                    entity_filter = Filter(
                        field_filter.operator,
                        value
                    )
                else:
                    entity_filter = Filter(
                        FilterOperator.ILIKE,
                        value
                    )

                # Storing filter in dict
                filter_list = entity_filters.setdefault(entity_field_name, [])
                filter_list.append(entity_filter)

        return entity_filters
