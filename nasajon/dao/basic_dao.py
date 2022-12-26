import uuid
from nsj_rest_lib.entity.entity_base import EntityBase
from typing import Any, Dict, List, Tuple
from nsj_rest_lib.entity.filter import FilterOperator, Filter
import enum
from nsj_rest_lib.dao.dao_base import DAOBase

class BasicDao(DAOBase):
    def list_search(self, after: uuid.UUID,
        limit: int,
        fields: List[str],
        order_fields: List[str],
        filters: Dict[str, List[Filter]],
        offset: int = None
    ) -> List[EntityBase]:
        """
        Returns a paginated entity list.
        """

        # Creating a entity instance
        entity = self._entity_class()

        # Cheking should use default entity order
        if order_fields is None:
            order_fields = entity.get_default_order_fields()

        # Making order fields with alias list
        order_fields_alias = [f"t0.{i}" for i in order_fields]

        # Resolving data to pagination
        order_map = {field: None for field in order_fields}

        if after is not None:
            after_obj = self.get(after)
            if len(after_obj) > 0:
                for field in order_fields:
                    order_map[field] = getattr(after_obj[0], field, None)

        # Making default order by clause
        order_by = f"""
            {', '.join(order_fields_alias)}
        """

        # Organizando o where da paginação
        pagination_where = ''
        if after is not None:

            # Making a list of pagination condictions
            list_page_where = []
            old_fields = []
            for field in order_fields:
                # Making equals condictions
                buffer_old_fields = 'true'
                for of in old_fields:
                    buffer_old_fields += f" and t0.{of} = :{of}"

                # Making current more than condiction
                list_page_where.append(
                    f"({buffer_old_fields} and t0.{field} > :{field})")

                # Storing current field as old
                old_fields.append(field)

            # Making SQL page condiction
            pagination_where = f"""
                and (
                    false
                    or {' or '.join(list_page_where)}
                )
            """

        # Organizando o where dos filtros
        filters_where, filter_values_map = self._make_filters_sql_search(filters)

        # Montando a query em si
        sql = f"""
        select

            {self._sql_fields(fields)}

        from
            {entity.get_table_name()} as t0
        where
            true
            {pagination_where}
            {filters_where}
        order by
            {order_by}
        """

        # Adding limit if received
        if limit is not None:
            sql += f"        limit {limit}"

        if offset is not None:
            sql += f"        offset {offset}"
        # Making the values dict
        kwargs = {
            **order_map,
            **filter_values_map
        }

        # Running the SQL query
        resp = self._db.execute_query_to_model(
            sql,
            self._entity_class,
            **kwargs
        )

        return resp

    def _make_filters_sql_search(self, filters: Dict[str, List[Filter]], with_and: bool = True, use_table_alias: bool = True) -> Tuple[str, Dict[str, Any]]:
        """
        Interpreta os filtros, retornando uma tupla com formato (filters_where, filter_values_map), onde
        filters_where: Parte do SQL, a ser adicionada na cláusula where, para realização dos filtros
        filter_values_map: Dicionário com os valores dos filtros, a serem enviados na excução da query

        Se receber o parâmetro filters nulo ou vazio, retorna ('', {}).
        """

        filters_where = ''
        filter_values_map = {}
        if filters is not None:
            filters_where = []

            # Iterating fields with filters
            for filter_field in filters:
                field_filter_where = []

                # Iterating condictions
                idx = -1
                for condiction in filters[filter_field]:
                    idx += 1

                    # Resolving condiction
                    operator = '='
                    if condiction.operator == FilterOperator.DIFFERENT:
                        operator = '<>'
                    elif condiction.operator == FilterOperator.GREATER_THAN:
                        operator = '>'
                    elif condiction.operator == FilterOperator.LESS_THAN:
                        operator = '<'
                    elif condiction.operator == FilterOperator.LIKE:
                        operator =  'like'
                    elif condiction.operator == FilterOperator.ILIKE:
                        operator =  'ilike'

                    # Making condiction alias
                    condiction_alias = f"ft_{condiction.operator.value}_{filter_field}_{idx}"

                    # Making condiction buffer
                    if use_table_alias:
                        condiction_buffer = f"t0.{filter_field} {operator} :{condiction_alias}"
                    else:
                        condiction_buffer = f"{filter_field} {operator} :{condiction_alias}"

                    # Storing field filter where
                    field_filter_where.append(condiction_buffer)

                    # Storing condiction value
                    if condiction.value is not None and isinstance(condiction.value.__class__, enum.EnumMeta):
                        filter_values_map[condiction_alias] = condiction.value.value
                    else:
                        filter_values_map[condiction_alias] = condiction.value

                # Formating condictions (with OR)
                field_filter_where = ' or '.join(field_filter_where)
                if field_filter_where.strip() != '':
                    field_filter_where = f"({field_filter_where})"

                # Storing all condictions to a field
                filters_where.append(field_filter_where)

            # Formating all filters (with AND)
            filters_where = '\n or '.join(filters_where)
            if filters_where.strip() != '' and with_and:
                filters_where = f"and {filters_where}"

        return (filters_where, filter_values_map)
    