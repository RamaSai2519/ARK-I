from shared.db.experts import get_experts_collections
from shared.helpers.experts import ExpertsHelper
from shared.helpers.users import UsersHelper
from shared.models.interfaces import Expert
from shared.models.common import Common
import json


class ExpertsPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.phoneNumber = phoneNumber
        self.experts_collections = get_experts_collections()

    def get_all_experts(self) -> str:
        experts_helper = ExpertsHelper()
        query = {'type': 'saarthi', 'active': True}
        data = experts_helper.get_experts(persona=True, query=query)
        experts = []
        for expert in data:
            expert = Common.clean_dict(expert, Expert)
            expert = Expert(**expert)
            expert_dict = {
                '_id': expert._id,
                'name': expert.name,
                'status': expert.status,
                'persona': expert.persona,
                'phoneNumber': expert.phoneNumber,
                'description': expert.description
            }
            experts.append(expert_dict)
        experts = json.dumps(experts)
        return experts

    def get_system_message(self) -> str:
        prompt = f"""
        Act as a customer service chatbot for "Sukoon Unlimited", dedicated to improving senior citizens' lives with connections, emotional support, and community engagement.
        Your task is to provide information about Sukoon Sarathis using specific functions for querying details.

        # Steps
        - You will be provided with a list of all available sarathis.
        - Receive Query: Understand the user's request for information about a particular sarathi.
        - Query Functions:
        - Use `GetTimings` to find the availability of the sarathi.
        - Use `GetSarathiSchedules` to check for upcoming calls or schedules of the sarathi.
        - Determine the availabilty based on the timings and schedules.
        - Provide Information:
        - Share the gathered information clearly with the user. Be sure to provide the _id(s) of the sarathi(s) clearly.
        - When asked for a recommendation, compare the user's persona with the sarathis' personas and recommend the most suitable sarathis with a detailed explanation. Always Provide a couple of options.
        - If the information isn't available, inform the user that they should contact support.
        - Make sure to mention if the sarathi is online or offline right now. If offline, provide the timings when they will be available.
        - Direct Further Assistance: If any query cannot be resolved or if data is unavailable, direct the user to contact the support team at +91 8035752993.
        - Response Formatting: Ensure all responses are suitable for WhatsApp communication.
        - Tone: Maintain a polite and helpful demeanor throughout the interaction.

        # Output Format

        The responses should be concise, direct answers tailored to the user's specific query. Use plain, conversational text without any markdown, given the context is WhatsApp.

        # Notes

        - You are restricted to using only provided data and should not generate information independently.
        - If data isn't accessible, reiterate the contact information for the support team.
        - If the user requests a recommendation, recommend a sarathi by comparing all available sarathis' personas with the user's persona. Make sure to provide a detailed explanation for the recommendation.
        """

        prompt += "Here are all the sarathis:\n"
        experts = self.get_all_experts()
        prompt += experts
        prompt += "Here are the user details:\n"
        user = UsersHelper().get_user(self.phoneNumber)
        user = {
            'name': user.get('name', ''),
            'persona': user.get('customerPersona', '')
        }
        prompt += json.dumps(user)
        prompt = Common.strip_para(prompt)

        return prompt
