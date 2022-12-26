from typing import  Set
from nsj_rest_lib.controller.route_base import RouteBase
from http.client import responses

from nsj_gcf_utils.json_util import json_dumps, json_loads
from nsj_gcf_utils.rest_error_util import format_json_error
from nasajon.settings import CONTENT_TYPE_JSON_HEADER


class BulkRoute(RouteBase):

    

    def _fill_response_error(self, error, status, response_item):
        response_item['status'] = status

        if 'body' not in response_item:
            response_item['body'] = {}

        if error is not None:
            response_item['body']= json_loads(format_json_error(error))
        return response_item

    def _add_response_list(self, response, response_item, status,  error = None, request_item = None, status_codes: Set = None):

         response_item = self._fill_response_error(error, status, response_item)
         if request_item is not None:
            request_item['request'] = request_item

         if status_codes is not None:
            status_codes.add(status)

         if 'response' not in response:
            response['response'] = []   
         response['response'].append(response_item)
         return response