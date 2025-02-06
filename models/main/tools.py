import json
import requests
from .tools_schemas import *
from .slack import SlackManager
from models.common import CommonTools
from shared.models.common import Common
from models.controller import Controller
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.constants import TimeFormats


class MainTools:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber
        self.controller = Controller(self.phoneNumber)

    def get_user_details(self, arguments: dict = None) -> dict:
        return CommonTools.get_user_details(self.phoneNumber)

    def update_user(self, user: dict) -> dict:
        url = config.URL + '/actions/user'
        user = Common.filter_falsy_values(user)
        user['phoneNumber'] = self.phoneNumber
        response = requests.post(url, json=user)
        return response.json()

    def get_previous_calls(self, count: int) -> dict:
        url = config.URL + '/actions/call'
        params = {
            'size': count,
            'dest': 'list',
            'filter_field': 'user',
            'filter_value': self.phoneNumber
        }
        response = requests.get(url, params=params)
        output = response.json()
        return output.get('output_details', {}).get('data', 'No calls done yet')

    def get_current_time(self, arguments: dict = None) -> str:
        return CommonTools.get_current_time()

    def notify_support(self, details: str) -> str:
        slack = SlackManager()
        return slack.send_message(self.phoneNumber, details)

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(GetUserDetails),
            pydantic_function_tool(GetCurrentTime),
            pydantic_function_tool(ExpertsAssistant),
            pydantic_function_tool(GetPreviousCalls),
            pydantic_function_tool(NotifySupportTeam),
            pydantic_function_tool(ServicesAssistant),
            pydantic_function_tool(PartnersAssistant),
            pydantic_function_tool(SchedulesAssistant),
            pydantic_function_tool(
                UpdateUserDetails,
                description=f"Make sure birthDate is in the format {TimeFormats.ANTD_TIME_FORMAT} and is in english only."),
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Model: Main, Function name: {
                function_name}, Arguments: {arguments}'
        )
        function_map = {
            "GetCurrentTime": self.get_current_time,
            "GetUserDetails": self.get_user_details,
            "UpdateUserDetails": lambda args: self.update_user(args.get('user')),
            "NotifySupportTeam": lambda args: self.notify_support(args.get('details')),
            "GetPreviousCalls": lambda args: self.get_previous_calls(int(args.get('count'))),
            "ExpertsAssistant": lambda args: self.controller.invoke_sub_model('expert', args.get('prompt')),
            "ServicesAssistant": lambda args: self.controller.invoke_sub_model('sukoon', args.get('prompt')),
            "PartnersAssistant": lambda args: self.controller.invoke_sub_model('partner', args.get('prompt')),
            "SchedulesAssistant": lambda args: self.controller.invoke_sub_model('schedule', args.get('prompt')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}\n')
        return json.dumps(response)
