from shared.db.chat import get_system_prompts_collection
from shared.models.common import Common


class PartnersPrompt:
    def __init__(self, phoneNumber: str) -> None:
        self.common = Common()
        self.phoneNumber = phoneNumber
        self.collection = get_system_prompts_collection()

    def get_system_message(self) -> str:
        context = self.common.get_beta_context(
            self.phoneNumber, 'ark_partners')
        query = {'context': context}
        doc = self.collection.find_one(query)
        prompt = doc.get('content')

        prompt = Common.strip_para(prompt)
        return prompt
