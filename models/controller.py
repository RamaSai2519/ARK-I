from chat import Chat
from shared.models.interfaces import Model
from models.eventsGPT.tools import EventsTools
from models.sukoonGPT.tools import SukoonTools
from models.eventsGPT.prompt import EventsPrompt
from models.expertsGPT.tools import ExpertsTools
from models.sukoonGPT.prompt import SukoonPrompt
from models.expertsGPT.prompt import ExpertsPrompt
from models.schedulesGPT.tools import SchedulesTools
from models.schedulesGPT.prompt import SchedulesPrompt


class Controller:
    def __init__(self, phoneNumber: str) -> None:
        self.models = {
            'expert': Model(
                ExpertsPrompt(phoneNumber).get_system_message,
                ExpertsTools().get_tools,
                ExpertsTools().handle_function_call
            ),
            'schedule': Model(
                SchedulesPrompt(phoneNumber).get_system_message,
                SchedulesTools().get_tools,
                SchedulesTools().handle_function_call
            ),
            'sukoon': Model(
                SukoonPrompt().get_system_message,
                SukoonTools(phoneNumber, self).get_tools,
                SukoonTools(phoneNumber, self).handle_function_call
            ),
            'event': Model(
                EventsPrompt(phoneNumber).get_system_message,
                EventsTools(phoneNumber).get_tools,
                EventsTools(phoneNumber).handle_function_call
            )
        }

    def invoke_sub_model(self, model_name: str, prompt: str) -> str:
        model = self.models.get(model_name)
        chat_obj = Chat(model=model, prompt=prompt)
        response = chat_obj.compute()
        return response
