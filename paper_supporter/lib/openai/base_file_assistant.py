from openai import NOT_GIVEN
from openai.types.beta import vector_store_create_params

from .base_intelligence_assistant import BaseIntelligenceAssistant

from paper_supporter.prerude import CLIENT


class BaseFileAssistant(BaseIntelligenceAssistant):
    def __init__(self, model: str, instruction: str = NOT_GIVEN):
        self.vector_store = CLIENT.beta.vector_stores.create(
            expires_after=vector_store_create_params.ExpiresAfter(
                anchor="last_active_at",
                days=1
            ),
        )

        super().__init__(model, vector_store_id=self.vector_store.id)
        self.set_instructions(instruction)

    def __del__(self):
        for f in self.get_files():
            self.remove_file_from_storage(f.id)
        CLIENT.beta.vector_stores.delete(
            vector_store_id=self.vector_store.id
        )
        super().__del__()
