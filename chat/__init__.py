from shared.helpers.openai import GPT_Client, GPT2_Client
from models.userGPT.prompt import UserPrompt
from shared.models.interfaces import Model
from shared.models.common import Common
from openai import RateLimitError
import json


class Chat:
    def __init__(self, model: Model, prompt: str, controller) -> None:
        self.model = model
        self.prompt = prompt
        self.controller = controller
        self.client_obj = GPT_Client()
        self.client = self.client_obj.get_gpt_client()
        self.message_history = self.get_message_history()

    def update_history(self, role: str, content: str) -> None:
        self.message_history.append(
            {"role": role, "content": content, "timestamp": Common.get_current_utc_time().strftime('%Y-%m-%d %H:%M:%S')})
        return self.message_history

    def get_message_history(self) -> list[dict]:
        return [{"role": "system", "content": self.model.prompt()}]

    def check_for_failed_tool(self) -> bool:
        for msg in reversed(self.message_history):
            if msg['role'] == 'assistant' and 'tool_calls' in msg:
                for call in msg['tool_calls']:
                    if call['function']['name'] == 'CreateSchedule':
                        tool_call_id = call['id']
                        for history_msg in self.message_history:
                            if history_msg.get('tool_call_id') == tool_call_id and 'FAILURE' in history_msg['content']:
                                prompt = 'Here is the history between main model(user) and sub-model(tool(SchedulesAssistant))'
                                history = self.message_history[1:]
                                prompt += f'\n{json.dumps(history)}'
                                user_prompt = self.controller.invoke_sub_model(
                                    'user', prompt)
                                self.update_history('user', user_prompt)
                                return True
        return False

    def get_response(self) -> str:
        tools = self.model.tools() if self.model.tools else None
        errors = 0

        while True:
            try:
                if tools:
                    response = self.client.chat.completions.create(
                        model='gpt-4o-2024-11-20', messages=self.message_history, tools=tools)
                else:
                    response = self.client.chat.completions.create(
                        model='gpt-4o-2024-11-20', messages=self.message_history)
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
                        if function_name == 'CreateSchedule' and 'FAILURE' in tool_response:
                            self.update_history(
                                'assistant', 'There was an error creating the schedule. See the history for more information.')
                    if self.message_history[-1]['role'] == 'tool':
                        continue
                if self.check_for_failed_tool():
                    continue
                break
            except RateLimitError:
                print('Rate limit error. Waiting for 5 seconds.')
                errors += 1
                if errors > 3:
                    return "Rate limit error. Please try again later."
                self.client_obj = GPT2_Client()
                self.client = self.client_obj.get_gpt_client()
        assistant_response = response.choices[0].message.content
        return assistant_response

    def compute(self) -> str:
        self.update_history('user', self.prompt)

        return self.get_response()
