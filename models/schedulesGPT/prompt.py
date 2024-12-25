from shared.models.interfaces import Output
from shared.configs import CONFIG as config
from shared.models.common import Common
import requests
import json


class SchedulesPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber

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
        prompt = f"""
        Act as a customer service chatbot for "Sukoon Unlimited", focusing on helping senior citizens with their schedules by providing information and canceling calls when requested.

        Use the provided user schedule data to assist with inquiries and cancellations. To cancel a schedule, use the "CancelSchedule" tool by providing the schedule _id as input.

        # Steps

        1. Identify User's Query: Determine if the user is asking for schedule information or requesting to cancel a call.
        2. Provide Schedule Information: If the user requests information about their upcoming schedules, retrieve and communicate the relevant details concisely.
        3. Cancel Call: If the user wants to cancel a call, use the schedule _id to cancel it via the "CancelSchedule" tool.
        4. Inform User: Communicate the status of the cancellation or information retrieval to the user.

        # Output Format

        The responses should be concise, direct answers tailored to the user's specific query. Use plain, conversational text without any markdown, as communication occurs on WhatsApp.

        # Notes
        - Use only the provided data to respond to queries; avoid generating any information independently.
        - If necessary information is unavailable, inform the user to contact the support team at +91 8035752993, available from 9:00 AM to 9:00 PM IST.
        - Be empathetic and considerate in interactions, as your user base primarily consists of senior citizens seeking assistance.
        """

        prompt += f"\n\n# User's Upcoming Schedules\n{self.get_schedules()}"
        prompt = Common.strip_para(prompt)

        return prompt
