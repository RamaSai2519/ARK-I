import json
import requests
from .tools_schemas import *
from models.common import CommonTools
from shared.models.common import Common
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.db.users import get_user_collection
from shared.db.events import get_events_collection


class SukoonTools:
    def __init__(self, phoneNumber: str, controller) -> None:
        self.controller = controller
        self.phone_number = phoneNumber
        self.users_collection = get_user_collection()
        self.events_collection = get_events_collection()
        self.user = CommonTools.get_user_details(phoneNumber)

    def get_user(self) -> dict:
        query = {'phoneNumber': self.phone_number}
        return self.users_collection.find_one(query)

    def register_user_for_event(self, slug: str) -> dict:
        query = {'slug': slug}
        event = self.events_collection.find_one(query)
        if not event:
            return {'error': 'Invalid event slug, ask the "EventsandMeetupsAssistant" tool for valid event slug.'}
        url = config.URL + '/actions/upsert_event_user'
        token = Common.get_token(self.user.get('_id'), 'free_events')
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'phoneNumber': self.phone_number,
                   'source': slug, 'initFrom': 'ARK'}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(EventsandMeetupsAssistant),
            pydantic_function_tool(
                RegisterUserForEvent, description="Register a user for an event by sending the two or three letter slug of the event.")
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Model: Sukoon, Function name: {
                function_name}, Arguments: {arguments}'
        )
        function_map = {
            'RegisterUserForEvent': lambda args: self.register_user_for_event(args.get('event_slug')),
            'EventsandMeetupsAssistant': lambda args: self.controller.invoke_sub_model('event', args.get('prompt'))
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'{function_name} Response: {response}\n')
        return json.dumps(response)
