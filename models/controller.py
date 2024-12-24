from chat import Chat
from shared.models.interfaces import Model
from models.expertsGPT.tools import ExpertsTools
from models.sukoonGPT.prompt import SukoonPrompt
from models.expertsGPT.prompt import ExpertsPrompt


class Prompts:
    sukoon_prompt = SukoonPrompt().get_system_message()
    experts_prompt = ExpertsPrompt().get_system_message()


class Tools:
    expert_tools = ExpertsTools().get_tools()


class Handlers:
    expert_handler = ExpertsTools().handle_function_call


class Controller:
    def __init__(self):
        self.models = {
            'expert': Model(Prompts.experts_prompt, Tools.expert_tools,
                            Handlers.expert_handler),
            'sukoon': Model(Prompts.sukoon_prompt)
        }

    def invoke_model(self, model_name: str, prompt: str) -> str:
        model = self.models.get(model_name)
        return Chat(model, prompt).get_response()
