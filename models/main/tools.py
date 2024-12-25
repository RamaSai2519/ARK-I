import json
import pytz
import requests
from .tools_schemas import *
from shared.models.common import Common
from datetime import datetime, timedelta
from models.controller import Controller
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.interfaces import Output
from shared.models.constants import TimeFormats


class MainTools:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber
        self.controller = Controller(self.phoneNumber)

    def get_user_details(self, arguments: dict = None) -> dict:
        url = config.URL + '/actions/user'
        params = {'phoneNumber': self.phoneNumber}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        user = output.output_details

        data = {
            '_id': user.get('_id', ''),
            'name': user.get('name', ''),
            'city': user.get('city', ''),
            'persona': user.get('customerPersona', ''),
        }
        birthDate = user.get('birthDate')
        if birthDate and isinstance(birthDate, datetime):
            data['birthDate'] = birthDate.strftime('%Y-%m-%d')
        return data

    def update_user(self, user: dict) -> dict:
        url = config.URL + '/actions/user'
        user = Common.filter_none_values(user)
        user['phoneNumber'] = self.phoneNumber
        response = requests.post(url, json=user)
        return response.json()

    def connect_now(self, arguments: dict) -> dict:
        url = config.URL + '/actions/call'
        payload = {
            'user_id': arguments.get('user_id'),
            'expert_id': arguments.get('expert_id'),
            'user_requested': True
        }
        response = requests.post(url, json=payload)
        return response.json()

    def connect_later(self, arguments: dict) -> dict:
        url = config.URL + '/actions/schedules'
        job_time = datetime.strptime(arguments.get(
            'job_time'), TimeFormats.ANTD_TIME_FORMAT)
        status = 'PENDING' if (job_time - datetime.now()
                               ).total_seconds() < 900 else 'WAPENDING'
        payload = {
            'status': status,
            'job_type': 'CALL',
            'isDeleted': False,
            'initiatedBy': 'ARK',
            'user_requested': True,
            'user_id': arguments.get('user_id'),
            'expert_id': arguments.get('expert_id'),
            'job_time': job_time.strftime(TimeFormats.AWS_TIME_FORMAT)
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_current_time(self, arguments: dict = None) -> str:
        times = {
            'TODAY_IST': datetime.now(pytz.timezone('Asia/Kolkata')),
            'TODAY_UTC': datetime.now(pytz.utc),
            'TOMORROW_IST': (datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1)),
            'TOMORROW_UTC': (datetime.now(pytz.utc) + timedelta(days=1)),
        }
        times = {key: value.strftime(TimeFormats.ANTD_TIME_FORMAT)
                 for key, value in times.items()}
        response = "Current IST Time: "
        response += times['TODAY_IST']
        response += "\nCurrent UTC Time: "
        response += times['TODAY_UTC']
        response += "\nTomorrow IST Time: "
        response += times['TOMORROW_IST']
        response += "\nTomorrow UTC Time: "
        response += times['TOMORROW_UTC']
        return response

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(ConnectNow,
                                   description=f"Make sure user_id and expert_id are valid ObjectIds only."),
            pydantic_function_tool(ConnectLater,
                                   description=f"Make sure job_time is in the format {TimeFormats.ANTD_TIME_FORMAT} and is in UTC timezone and english only."),
            pydantic_function_tool(GetUserDetails),
            pydantic_function_tool(GetCurrentTime),
            pydantic_function_tool(ExpertsAssistant),
            pydantic_function_tool(ServicesAssistant),
            pydantic_function_tool(SchedulesAssistant),
            pydantic_function_tool(
                UpdateUserDetails,
                description=f"Make sure birthDate is in the format {TimeFormats.ANTD_TIME_FORMAT} and is in english only."),
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            "GetCurrentTime": self.get_current_time,
            "GetUserDetails": self.get_user_details,
            "ConnectNow": lambda args: self.connect_now(args),
            "ConnectLater": lambda args: self.connect_later(args),
            "UpdateUserDetails": lambda args: self.update_user(args.get('user')),
            "ExpertsAssistant": lambda args: self.controller.invoke_sub_model('expert', args.get('prompt')),
            "ServicesAssistant": lambda args: self.controller.invoke_sub_model('sukoon', args.get('prompt')),
            "SchedulesAssistant": lambda args: self.controller.invoke_sub_model('schedule', args.get('prompt')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return json.dumps(response)
