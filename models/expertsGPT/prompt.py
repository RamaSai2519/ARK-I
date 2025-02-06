from shared.db.chat import get_system_prompts_collection
from shared.db.experts import get_experts_collections
from shared.helpers.experts import ExpertsHelper
from shared.helpers.users import UsersHelper
from shared.models.interfaces import Expert
from shared.models.common import Common
import json


class ExpertsPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.common = Common()
        self.phoneNumber = phoneNumber
        self.collection = get_system_prompts_collection()
        self.experts_collections = get_experts_collections()

    def get_all_experts(self) -> str:
        experts_helper = ExpertsHelper()
        query = {'type': 'saarthi', 'active': True, 'isDeleted': False}
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
                'description': expert.description
            }
            experts.append(expert_dict)
        experts = json.dumps(experts)
        return experts

    def get_system_message(self) -> str:
        context = self.common.get_beta_context(self.phoneNumber, 'ark_expert')
        query = {'context': context}
        doc = self.collection.find_one(query)
        prompt = doc.get('content')

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
