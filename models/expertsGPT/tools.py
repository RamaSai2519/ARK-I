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

    def format_experts(self, data: list[dict]) -> str:
        experts = []
        for expert in data:
            expert = Common.clean_dict(expert, Expert)
            expert = Expert(**expert)
            expert_dict = {
                '_id': expert._id,
                'name': expert.name,
                'status': expert.status,
                'active': expert.active,
                'description': expert.description,
                'persona': expert.persona
            }
            if expert.persona:
                expert_dict['persona'] = expert.persona
            experts.append(expert_dict)
        return experts

    def get_available_experts_for_recommendation(self) -> str:
        experts_helper = ExpertsHelper()
        query = {'status': 'online'}
        data = experts_helper.get_experts(query=query, persona=True)
        experts = self.format_experts(data)
        return json.dumps(experts)

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
            pydantic_function_tool(GetTimings),
            pydantic_function_tool(GetSarathiSchedules),
            pydantic_function_tool(GetAvailableExpertsForRecommendation)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetTimings': lambda args: self.get_timings(args.get('expertId')),
            'GetSarathiSchedules': lambda args: self.get_sarathi_schedules(args.get('expertName')),
            'GetAvailableExpertsForRecommendation': lambda args: self.get_available_experts_for_recommendation()
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return response
