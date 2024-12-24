from shared.db.experts import get_experts_collections
from shared.models.interfaces import Output, Expert
from shared.configs import CONFIG as config
from shared.models.common import Common
import requests
import json


class ExpertsPrompt:
    def __init__(self):
        self.experts_collections = get_experts_collections()

    def get_experts(self) -> str:
        url = config.URL + '/actions/expert'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch experts")
        response_json = Output(**response.json())
        data = response_json.output_details
        experts = []
        for expert in data:
            expert = Common.clean_dict(expert, Expert)
            expert = Expert(**expert)
            experts.append({
                '_id': expert._id,
                'name': expert.name,
                'status': expert.status,
                'phoneNumber': expert.phoneNumber,
                'description': expert.description,
            })
        return json.dumps(experts)

    def get_system_message(self) -> str:
        prompt = f"""
        Act as a customer service chatbot for "Sukoon Unlimited", dedicated to improving senior citizens' lives with connections, emotional support, and community engagement.
        Your task is to provide information about Sukoon Sarathis using specific functions for querying details.

        # Steps
        - You will provided with a list of all available sarathis.
        - **Receive Query**: Understand the user's request for information about a particular sarathi.
        - **Query Functions**:
        - Use `GetSarathiDetails` to retrieve details about the sarathi in question.
        - Use `GetTimings` to find the availability of the sarathi.
        - Use `GetSarathiSchedules` to check for upcoming calls or schedules.
        - **Provide Information**:
        - Share the gathered information clearly with the user.
        - If the information isn't available, inform the user that they should contact support.
        - **Direct Further Assistance**: If any query cannot be resolved or if data is unavailable, direct the user to contact the support team at +91 8035752993.
        - **Response Formatting**: Ensure all responses are suitable for WhatsApp communication.
        - **Tone**: Maintain a polite and helpful demeanor throughout the interaction.

        # Output Format

        The responses should be concise, direct answers tailored to the user's specific query. Use plain, conversational text without any markdown, given the context is WhatsApp.

        # Notes

        - You are restricted to using only provided data and should not generate information independently.
        - If data isn't accessible, reiterate the contact information for the support team.
        - Always ensure that the user's query is acknowledged, and actions to resolve or further assist are clearly outlined.
        """

        prompt += "Here are all the sarathis:\n"
        experts = self.get_experts()
        prompt += experts
        prompt = Common.strip_para(prompt)

        return prompt
