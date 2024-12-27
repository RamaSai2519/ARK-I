from shared.models.common import Common
from shared.models.constants import TimeFormats
from shared.db.chat import get_system_prompts_collection


class MainPrompt:
    def __init__(self) -> None:
        self.collection = get_system_prompts_collection()

    def get_system_message(self) -> str:
        query = {'context': 'ark_main'}
        doc = self.collection.find_one(query)
        prompt = doc.get('content')
        prompt += f'While dealing with date strings when you want to call functions, always use this format: {
            TimeFormats.ANTD_TIME_FORMAT}.'
        prompt = Common.strip_para(prompt)

        return prompt
