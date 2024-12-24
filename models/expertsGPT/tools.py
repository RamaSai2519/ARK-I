import json
import requests
from .tools_schemas import *
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.interfaces import Output


class ExpertsTools:
    def __init__(self):
        pass

    def get_sarathi_details(self, phone_number: str) -> str:
        url = config.URL + '/actions/expert'
        params = {'phoneNumber': phone_number}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details
        expert = {
            '_id': data.get('_id'),
            'name': data.get('name', ''),
            'persona': data.get('persona', {}),
            'phoneNumber': data.get('phoneNumber'),
        }
        return json.dumps(expert)

    def get_timings(self, expert_id: str) -> str:
        url = config.URL + '/actions/timings'
        params = {'expert': expert_id}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details
        return json.dumps(data)

    def get_sarathi_schedules(self, expert_name: str) -> str:
        url = config.URL + '/actions/schedules'
        params = {'filter_field': 'expert', 'filter_value': expert_name}
        params['pending'] = 'true'
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details.get('data')
        if not data:
            return "No upcoming schedules found"
        return json.dumps(data)

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(GetSarathiDetails),
            pydantic_function_tool(GetTimings),
            pydantic_function_tool(GetSarathiSchedules)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetSarathiDetails': lambda args: self.get_sarathi_details(args.get('phoneNumber')),
            'GetTimings': lambda args: self.get_timings(args.get('expertId')),
            'GetSarathiSchedules': lambda args: self.get_sarathi_schedules(args.get('expertName'))
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return response
