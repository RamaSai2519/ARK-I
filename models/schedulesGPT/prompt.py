from shared.db.chat import get_system_prompts_collection
from shared.models.constants import TimeFormats
from shared.models.interfaces import Output
from shared.configs import CONFIG as config
from shared.models.common import Common
import requests
import json


class SchedulesPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.common = Common()
        self.phoneNumber = phoneNumber
        self.collection = get_system_prompts_collection()

    def get_user_name(self) -> str:
        url = config.URL + '/actions/user'
        params = {'phoneNumber': self.phoneNumber}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        user = output.output_details
        return user.get('name')

    def get_schedules(self) -> str:
        url = config.URL + '/actions/schedules'
        user_name = self.get_user_name()
        params = {'filter_field': 'user', 'filter_value': user_name}
        params['pending'] = 'true'
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details.get('data')
        if not data:
            return "No upcoming schedules found"
        return json.dumps(data)

    def get_system_message(self) -> str:
        context = self.common.get_beta_context(
            self.phoneNumber, 'ark_schedule')
        query = {'context': context}
        doc = self.collection.find_one(query)
        prompt = doc.get('content')
        prompt += f'While dealing with date strings when you want to call functions, always use this format: {
            TimeFormats.ANTD_TIME_FORMAT}.'
        prompt += f"\n\n# User's Upcoming Schedules\n{self.get_schedules()}"
        prompt = Common.strip_para(prompt)

        return prompt
