from openai.types.beta import vector_store_create_params, assistant_update_params
from openai.types.beta.assistant_update_params import ToolResourcesFileSearch
from openai.types.beta.file_search_tool_param import FileSearchToolParam, FileSearch
from openai.types.file_object import FileObject

from .base_assistant import CLIENT, BaseAssistant


class BaseFileAssistant(BaseAssistant):
    def __init__(self, model: str):
        super().__init__(model)
        self.files: list[FileObject] = []

        self.vector_store = CLIENT.beta.vector_stores.create(
            expires_after=vector_store_create_params.ExpiresAfter(
                anchor="last_active_at",
                days=1
            ),
        )

        super().modify(
            tools=[
                FileSearchToolParam(
                    type="file_search",
                    file_search=FileSearch()
                )
            ],
            tool_resources=assistant_update_params.ToolResources(
                file_search=ToolResourcesFileSearch(
                    vector_store_ids=[self.vector_store.id]
                )
            )
        )

    def __del__(self):
        CLIENT.beta.vector_stores.delete(
            vector_store_id=self.vector_store.id
        )
        for f in self.files:
            CLIENT.files.delete(f.id)
        super().__del__()

    def add_file(self, file_object):
        self.files.append(
            CLIENT.files.create(
                file=file_object,
                purpose="assistants"
            )
        )
        CLIENT.beta.vector_stores.files.create(
            vector_store_id=self.vector_store.id,
            file_id=self.files[-1].id
        )

    def modify(self, *args, **kwargs):
        raise NotImplemented
