import json
import requests
from .tools_schemas import *
from datetime import datetime
from models.common import CommonTools
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.constants import TimeFormats


class SchedulesTools:
    def __init__(self, phoneNumber: str, controller) -> None:
        self.controller = controller
        self.phone_number = phoneNumber
        self.user = CommonTools.get_user_details(phoneNumber)

    def cancel_schedule(self, _id: str) -> dict:
        url = config.URL + '/actions/schedules'
        payload = {'_id': _id, 'isDeleted': True}
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
            'user_id': self.user.get('_id'),
            'expert_id': arguments.get('expert_id'),
            'job_time': job_time.strftime(TimeFormats.AWS_TIME_FORMAT)
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_current_time(self, arguments: dict = None) -> str:
        return CommonTools.get_current_time()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(
                CreateSchedule,
                description=f"Make sure job_time is in the format {TimeFormats.ANTD_TIME_FORMAT} and is in UTC timezone and english only. If an invalid ID error is returned then ask the 'ExpertsAssistant' for the correct `_id` by providing the expert name."),
            pydantic_function_tool(
                CancelSchedule, description='Pass the _id of the schedule to cancel it'),
            pydantic_function_tool(GetCurrentTime),
            pydantic_function_tool(ExpertsAssistant)
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Model: Schedules, Function name: {
                function_name}, Arguments: {arguments}'
        )
        function_map = {
            'GetCurrentTime': self.get_current_time,
            'CreateSchedule': lambda args: self.connect_later(args),
            'CancelSchedule': lambda args: self.cancel_schedule(args.get('schedule_id')),
            'ExpertsAssistant': lambda args: self.controller.invoke_sub_model('expert', args.get('prompt')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}\n')
        return json.dumps(response)
