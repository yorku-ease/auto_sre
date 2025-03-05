import ollama

class Model:
    def generate(self, prompt: str) -> str:
        pass

def _get_local_model_names():
    local_models = ollama.list()['models']
    return [m.model for m in local_models]

# TODO: Add support for ollama running outside ollama through client object which accepts URL
class OllamaModel:
    def __init__(self, model: str, system_prompt: str = None):
        if model not in _get_local_model_names():
            print(f"{model} not downloaded, downloading")
            ollama.pull(model)
        
        self.model = model
        self.prompts = []
        if system_prompt is not None:
            self.prompts.append(
                self._make_message(system_prompt, "system")
            )
    
    def set_system_prompt(self, system_prompt: str):
        if self.prompts and self.prompts[0]["role"] == "system":
            self.prompts = self.prompts[1:]
        self.prompts = [self._make_message(system_prompt, role = "system")] + self.prompts 

    def _make_message(self, prompt: str, role: str = "user") -> dict[str, str]:
        return {
            "role": role,
            "content": prompt
        }

    def generate(self, prompt: str):
        messages = self.prompts + [self._make_message(prompt)]
        return ollama.chat(
            self.model,
            messages=messages
        ).message.content

