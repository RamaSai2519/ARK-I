from shared.db.chat import get_system_prompts_collection
from shared.models.common import Common


class SukoonPrompt:
    def __init__(self) -> None:
        self.system_prompts_collection = get_system_prompts_collection()

    def get_sukoon(self) -> str:
        system_prompt = self.system_prompts_collection.find_one(
            {'context': 'wa_webhook'})
        return system_prompt['content']

    def get_system_message(self) -> str:
        query = {'context': 'ark_sukoon'}
        doc = self.system_prompts_collection.find_one(query)
        prompt = doc.get('content')

        info = self.get_sukoon()
        prompt += info
        prompt = Common.strip_para(prompt)

        return prompt
