from shared.models.interfaces import ChatInput as Input, Output
from shared.db.chat import get_histories_collection
from shared.helpers.openai import GPT_Client
from models.main.prompt import MainPrompt
from shared.models.common import Common
from models.main.tools import MainTools
from openai import RateLimitError
from datetime import datetime
import time


class ARK:
    def __init__(self, input: Input) -> None:
        self.input = input
        self.common = Common()
        self.tooler = MainTools(self.input.phoneNumber)
        self.histories_collection = get_histories_collection()

        self.now_date = self.get_now_date()
        self.query = self.prep_query()
        self.message_history, self.history_id, self.system_message = self.determine_history()

    def get_now_date(self) -> datetime:
        now_date = Common.get_current_utc_time()
        now_date = now_date.strftime('%Y-%m-%d %H')
        return now_date

    def prep_query(self) -> dict:
        query = {'phoneNumber': self.input.phoneNumber,
                 'createdAt': self.now_date, 'context': self.input.context}
        return query

    def determine_history(self) -> tuple[list[dict], str]:
        history = self.histories_collection.find_one(self.query)
        if history:
            return history['history'], history['_id'], history['history'][-1]['content']

        system_message = MainPrompt().get_system_message()
        default_history = [{"role": "system", "content": system_message}]

        insertion = self.histories_collection.insert_one(
            {**self.query, 'history': default_history, 'status': 'started'})
        return default_history, insertion.inserted_id, system_message

    def update_history(self, role: str, content: str) -> None:
        self.message_history.append(
            {"role": role, "content": content, "timestamp": Common.get_current_utc_time().strftime('%Y-%m-%d %H:%M:%S')})
        return self.message_history

    def save_history(self) -> None:
        update = {'$set': {'history': self.message_history, 'status': 'done'}}
        self.histories_collection.update_one({'_id': self.history_id}, update)

    def truncate_history(self):
        system_message = self.message_history[0]
        truncated_history = [system_message]
        self.message_history = truncated_history
        self.update_history('user', self.input.prompt)

    def get_gpt_response(self) -> str:
        client_obj = GPT_Client()
        client = client_obj.get_gpt_client()
        tools = self.tooler.get_tools()
        errors = 0
        while True:
            try:
                response = client.chat.completions.create(
                    model='gpt-4-turbo', messages=self.message_history, tools=tools)
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
                        tool_response = self.tooler.handle_function_call(
                            function_name, arguments)
                        self.message_history.append(
                            {'role': 'tool', 'content': tool_response, 'tool_call_id': tool_call.id, 'timestamp': Common.get_current_utc_time().strftime('%Y-%m-%d %H:%M:%S')})
                    continue
                break
            except RateLimitError:
                print('Rate limit error. Waiting for 5 seconds.')
                errors += 1
                if errors > 3:
                    print('Truncating message history.')
                    self.truncate_history()
                    continue
                time.sleep(5)
        assistant_response = response.choices[0].message.content
        return assistant_response

    def check_to_serve(self) -> bool:
        return True
        doc = self.histories_collection.find_one(self.query)
        if doc['status'] == 'inprogress':
            return False
        update = {'$set': {'status': 'inprogress'}}
        self.histories_collection.update_one({'_id': self.history_id}, update)
        return True

    def compute(self) -> Output:
        if self.check_to_serve() == False:
            return Output(output_message='Please wait for the assistant to respond.')
        self.update_history('user', self.input.prompt)
        response = self.get_gpt_response()

        self.update_history('assistant', response)
        self.save_history()

        return Output(
            output_details={
                'response': Common.jsonify(response),
                'history': Common.jsonify(self.message_history)
            }
        )
