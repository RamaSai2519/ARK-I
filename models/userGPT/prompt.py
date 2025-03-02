from shared.db.chat import get_system_prompts_collection
from shared.models.common import Common


class UserPrompt:
    def __init__(self, phoneNumber: str, history: list[dict]) -> None:
        self.common = Common()
        self.history = history
        self.phoneNumber = phoneNumber
        self.system_prompts_collection = get_system_prompts_collection()

    def get_system_message(self) -> str:
        context = self.common.get_beta_context(self.phoneNumber, 'ark_user')
        query = {'context': context}
        doc = self.system_prompts_collection.find_one(query)
        prompt = str(doc.get('content'))
        prompt = prompt.format(main_history=self.history)
        prompt = Common.strip_para(prompt)

        return prompt
