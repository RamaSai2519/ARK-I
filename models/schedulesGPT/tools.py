import json
import requests
from .tools_schemas import *
from openai import pydantic_function_tool
from shared.configs import CONFIG as config


class SchedulesTools:
    def __init__(self) -> None:
        pass

    def cancel_schedule(self, _id: str) -> dict:
        url = config.URL + '/actions/schedules'
        payload = {'_id': _id, 'isDeleted': True}
        response = requests.post(url, json=payload)
        return response.json()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(CancelSchedule)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetTimings': lambda args: self.cancel_schedule(args.get('_id'))
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return response
