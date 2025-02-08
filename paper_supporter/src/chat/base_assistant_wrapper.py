from paper_supporter.lib.openai import EventHandler
from paper_supporter.lib.openai.base_intelligence_assistant import BaseIntelligenceAssistant


class ChatAssistant:
    def __init__(self, model: str, vector_store_id: str = None):
        self.assistant = BaseIntelligenceAssistant(model, vector_store_id)

    def add_message(self, message: str):
        self.assistant.add_message(message)

    def run(self):
        handler = EventHandler()
        return self.assistant.run(handler)

    def get_vector_store(self):
        return self.assistant.get_vector_store()