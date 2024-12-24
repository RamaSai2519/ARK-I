from shared.helpers.openai import GPT_Client
from shared.models.interfaces import Model
from shared.models.common import Common
from openai import RateLimitError
from pprint import pprint
import time


class Chat:
    def __init__(self, model: Model, prompt: str) -> None:
        self.model = model
        self.prompt = prompt
        self.message_history = self.get_message_history()

    def update_history(self, role: str, content: str) -> None:
        self.message_history.append(
            {"role": role, "content": content, "timestamp": Common.get_current_utc_time().strftime('%Y-%m-%d %H:%M:%S')})
        return self.message_history

    def get_message_history(self) -> list[dict]:
        return [{"role": "system", "content": self.model.prompt()}]

    def get_response(self) -> str:
        client_obj = GPT_Client()
        client = client_obj.get_gpt_client()
        tools = self.model.tools() if self.model.tools else None
        errors = 0

        while True:
            try:
                if tools:
                    response = client.chat.completions.create(
                        model='gpt-4-turbo', messages=self.message_history, tools=tools)
                else:
                    response = client.chat.completions.create(
                        model='gpt-4-turbo', messages=self.message_history)
                tool_calls = response.choices[0].message.tool_calls
                if tool_calls:
                    self.message_history.append({
                        'role': 'assistant',
                        'tool_calls': [
                            {**t.__dict__, 'function': t.function.__dict__}
                            for t in tool_calls
                        ],
                    })
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments = tool_call.function.arguments
                        tool_response = self.model.handler(
                            function_name, arguments)
                        self.message_history.append(
                            {'role': 'tool', 'content': tool_response, 'tool_call_id': tool_call.id, 'timestamp': Common.get_current_utc_time().strftime('%Y-%m-%d %H:%M:%S')})
                    continue
                break
            except RateLimitError:
                print('Rate limit error. Waiting for 5 seconds.')
                errors += 1
                if errors > 3:
                    return "Rate limit error. Please try again later."
                time.sleep(5)
        assistant_response = response.choices[0].message.content
        return assistant_response

    def compute(self) -> str:
        self.update_history('user', self.prompt)

        return self.get_response()
