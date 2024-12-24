import json
import requests
from .tools_schemas import *
from datetime import datetime
from models.controller import Controller
from openai import pydantic_function_tool
from shared.configs import CONFIG as config
from shared.models.interfaces import Output


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
        birthDate = user.get('birthDate')

        data = {
            'name': user.get('name', ''),
            'city': user.get('city', ''),
            'persona': user.get('customerPersona', ''),
        }
        if birthDate and isinstance(birthDate, datetime):
            data['birthDate'] = birthDate.strftime('%Y-%m-%d')
        return data

    def register_user(self, name: str = None, city: str = None, birthDate: str = None) -> dict:
        url = config.URL + '/actions/user'
        payload = {'phoneNumber': self.phoneNumber, 'name': name}
        if birthDate:
            payload['birthDate'] = birthDate
        if city:
            payload['city'] = city
        response = requests.post(url, json=payload)
        return response.json()

    def get_tools(self) -> list:
        return [
            pydantic_function_tool(SaveUserCity),
            pydantic_function_tool(SaveUserName),
            pydantic_function_tool(GetUserDetails),
            pydantic_function_tool(ExpertsAssistant),
            pydantic_function_tool(ServicesAssistant),
            pydantic_function_tool(SaveUserBirthDate),
        ]

    def handle_function_call(self, function_name: str, arguments: str) -> str:
        print(
            f'Function name: {function_name}, Arguments: {arguments}'
        )
        function_map = {
            "GetUserDetails": self.get_user_details,
            "SaveUserCity": lambda args: self.register_user(city=args.get('city')),
            "SaveUserName": lambda args: self.register_user(name=args.get('name')),
            "SaveUserBirthDate": lambda args: self.register_user(birthDate=args.get('birthDate')),
            "ExpertsAssistant": lambda args: self.controller.invoke_sub_model('expert', args.get('prompt')),
            "ServicesAssistant": lambda args: self.controller.invoke_sub_model('sukoon', args.get('prompt')),
        }

        arguments = json.loads(arguments) if arguments else {}
        response = function_map[function_name](
            arguments) if function_name in function_map else {}
        print(f'Response: {response}')
        return json.dumps(response)
