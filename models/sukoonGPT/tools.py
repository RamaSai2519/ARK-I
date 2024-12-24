import json
from .tools_schemas import *


class SukoonTools:
    def __init__(self) -> None:
        pass

    def get_tools(self) -> list:
        return []

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {}

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return response
