import json
import requests
from .tools_schemas import *
from shared.models.common import Common
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.helpers.experts import ExpertsHelper
from shared.models.interfaces import Output, Expert


class ExpertsTools:
    def __init__(self) -> None:
        pass

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
            pydantic_function_tool(GetTimings,
                                   description='Gets the availability timings of a sarathi in IST'),
            pydantic_function_tool(GetSarathiSchedules,
                                   description='Gets the upcoming schedules of a sarathi with UTC job_time'),
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetTimings': lambda args: self.get_timings(args.get('expertId')),
            'GetSarathiSchedules': lambda args: self.get_sarathi_schedules(args.get('expertName')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return response
