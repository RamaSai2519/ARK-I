import json
import requests
from .tools_schemas import *
from models.common import CommonTools
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.interfaces import Output
from shared.models.constants import TimeFormats


class ExpertsTools:
    def __init__(self) -> None:
        pass

    def get_timings(self, expert_id: str, date: str) -> str:
        url = config.URL + '/actions/slots'
        payload = {
            'datetime': date,
            'duration': 30,
            'expert': expert_id
        }
        response = requests.post(url, json=payload)
        output = Output(**response.json())
        data = output.output_details
        if not data:
            return "No slots available, try another date"
        return data

    def get_sarathi_schedules(self, expert_name: str) -> str:
        url = config.URL + '/actions/schedules'
        params = {'filter_field': 'expert', 'filter_value': expert_name}
        params['pending'] = 'true'
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details.get('data')
        if not data:
            return "No upcoming schedules found"
        return data

    def get_current_time(self, arguments: dict = None) -> str:
        return CommonTools.get_current_time()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(GetSlots,
                                   description=f'Gets the slots of an expert, the `date` should be in {TimeFormats.ANTD_TIME_FORMAT} format only'),
            pydantic_function_tool(GetSarathiSchedules,
                                   description='Gets the upcoming schedules of a sarathi with UTC job_time'),
            pydantic_function_tool(GetCurrentTime)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Model: Experts, Function name: {
                function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetCurrentTime': self.get_current_time,
            'GetTimings': lambda args: self.get_timings(args.get('expertId'), args.get('date')),
            'GetSarathiSchedules': lambda args: self.get_sarathi_schedules(args.get('expertName')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}\n')
        return json.dumps(response)
