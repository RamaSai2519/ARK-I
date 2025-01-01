from shared.db.chat import get_system_prompts_collection
from shared.configs import CONFIG as config
from shared.models.interfaces import Output
from shared.models.common import Common
import requests
import json


class EventsPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber
        self.collection = get_system_prompts_collection()

    def get_all_events(self) -> str:
        url = config.URL + "/actions/list_events"
        params = {'fromToday': 'true'}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        data = output.output_details.get('data', [])
        if data == []:
            return "No upcoming events found. Please contact support for more information."
        return json.dumps(data)

    def get_system_message(self) -> str:
        query = {'context': 'ark_event'}
        doc = self.collection.find_one(query)
        prompt = doc.get('content')

        prompt += "\nHere are the upcoming events, all the timimgs of events below are in UTC, mention the timezone clearly in all your responses:\n"
        prompt += self.get_all_events()
        prompt = Common.strip_para(prompt)

        return prompt
