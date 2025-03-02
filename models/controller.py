from chat import Chat
from shared.models.interfaces import Model
from models.userGPT.prompt import UserPrompt
from models.eventsGPT.tools import EventsTools
from models.sukoonGPT.tools import SukoonTools
from models.eventsGPT.prompt import EventsPrompt
from models.expertsGPT.tools import ExpertsTools
from models.sukoonGPT.prompt import SukoonPrompt
from models.expertsGPT.prompt import ExpertsPrompt
from models.partnersGPT.tools import PartnersTools
from models.partnersGPT.prompt import PartnersPrompt
from models.schedulesGPT.tools import SchedulesTools
from models.schedulesGPT.prompt import SchedulesPrompt


class Controller:
    def __init__(self, phoneNumber: str, history: list[dict]) -> None:
        self.history = history
        self.models = {
            'expert': Model(
                ExpertsPrompt(phoneNumber).get_system_message,
                ExpertsTools().get_tools,
                ExpertsTools().handle_function_call
            ),
            'schedule': Model(
                SchedulesPrompt(phoneNumber).get_system_message,
                SchedulesTools(phoneNumber, self).get_tools,
                SchedulesTools(phoneNumber, self).handle_function_call
            ),
            'sukoon': Model(
                SukoonPrompt(phoneNumber).get_system_message,
                SukoonTools(phoneNumber, self).get_tools,
                SukoonTools(phoneNumber, self).handle_function_call
            ),
            'event': Model(
                EventsPrompt(phoneNumber).get_system_message,
                EventsTools(phoneNumber).get_tools,
                EventsTools(phoneNumber).handle_function_call
            ),
            'partner': Model(
                PartnersPrompt(phoneNumber).get_system_message,
                PartnersTools(phoneNumber).get_tools,
                PartnersTools(phoneNumber).handle_function_call
            ),
            'user': Model(
                UserPrompt(phoneNumber, history).get_system_message
            )
        }

    def invoke_sub_model(self, model_name: str, prompt: str) -> str:
        model = self.models.get(model_name)
        chat_obj = Chat(model, prompt, self)
        response = chat_obj.compute()
        return response
