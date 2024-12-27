import json
import requests
from .tools_schemas import *
from models.common import CommonTools
from openai import pydantic_function_tool
from shared.configs import CONFIG as config


class EventsTools:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber

    def get_current_time(self, arguments: dict = None) -> str:
        return CommonTools.get_current_time()

    def get_users_events(self, arguments: dict = None) -> str:
        url = config.URL + "/actions/list_event_users"
        params = {
            'filter_field': 'phoneNumber',
            'filter_value': self.phoneNumber
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(GetCurrentTime),
            pydantic_function_tool(GetUserRegisteredEvents)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            "GetCurrentTime": self.get_current_time,
            "GetUserRegisteredEvents": self.get_users_events
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}')
        return json.dumps(response)
