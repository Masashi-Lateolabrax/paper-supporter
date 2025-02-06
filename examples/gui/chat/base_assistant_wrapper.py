from paper_supporter.lib.openai import BaseFileAssistant, EventHandler


class ChatAssistant:
    def __init__(self, model: str):
        self.assistant = BaseFileAssistant(model)

    def add_message(self, message: str):
        self.assistant.add_message(message)

    def run(self):
        handler = EventHandler()
        return self.assistant.run(handler)
