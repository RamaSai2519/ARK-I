import json
from .tools_schemas import *
from models.common import CommonTools
from openai import pydantic_function_tool


class PartnersTools:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber

    def get_current_time(self, arguments: dict = None) -> str:
        return CommonTools.get_current_time()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(GetCurrentTime)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Model: Events, Function name: {
                function_name}, Arguments: {arguments}'
        )
        function_map = {
            "GetCurrentTime": self.get_current_time
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}\n')
        return json.dumps(response)
