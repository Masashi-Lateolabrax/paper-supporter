from openai.types.beta import FileSearchToolParam, assistant_update_params
from openai.types.beta.assistant_create_params import ToolResourcesFileSearch
from openai.types.beta.file_search_tool_param import FileSearch

from .base_assistant import BaseAssistant, CLIENT


class BaseIntelligenceAssistant(BaseAssistant):
    def __init__(self, model: str, storage_id: str = None):
        super().__init__(model)

        if storage_id is None:
            self.storage = CLIENT.beta.vector_stores.create()
        else:
            self.storage = CLIENT.beta.vector_stores.retrieve(
                vector_store_id=storage_id
            )

        super()._modify(
            tools=[
                FileSearchToolParam(
                    type="file_search",
                    file_search=FileSearch()
                )
            ],
            tool_resources=assistant_update_params.ToolResources(
                file_search=ToolResourcesFileSearch(
                    vector_store_ids=[self.storage.id]
                )
            )
        )

    def get_storage_id(self):
        return self.storage.id

    def add_file(self, file_object):
        file = CLIENT.files.create(
            file=file_object,
            purpose="assistants"
        )
        CLIENT.beta.vector_stores.files.create(
            vector_store_id=self.storage.id,
            file_id=file.id
        )
