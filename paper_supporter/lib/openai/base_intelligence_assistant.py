from openai.types.beta import FileSearchToolParam, assistant_update_params
from openai.types.beta.assistant_create_params import ToolResourcesFileSearch
from openai.types.beta.file_search_tool_param import FileSearch
from openai.types.beta.vector_stores import VectorStoreFile

from .base_assistant import BaseAssistant, CLIENT


class BaseIntelligenceAssistant(BaseAssistant):
    """
    BaseIntelligenceAssistant class to interact with the OpenAI assistant with additional file search capabilities.
    """

    def __init__(self, model: str, storage_id: str = None):
        """
        Initialize the BaseIntelligenceAssistant with a specific model and optional storage ID.

        :param model: The model to use for the assistant.
        :param storage_id: The storage ID for the vector store. If None, a new vector store is created.
        """

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
        """
        Get the storage ID of the vector store.

        :return: The storage ID.
        """

        return self.storage.id

    def add_file(self, file_object):
        """
        Add a file to the vector store.

        :param file_object: The file object to add.
        """

        file = CLIENT.files.create(
            file=file_object,
            purpose="assistants"
        )
        CLIENT.beta.vector_stores.files.create(
            vector_store_id=self.storage.id,
            file_id=file.id
        )

    def get_files(self) -> list[VectorStoreFile]:
        """
        Get the list of files in the vector store.

        :return: A list of VectorStoreFile objects.
        """

        return CLIENT.beta.vector_stores.files.list(
            vector_store_id=self.storage.id
        )

    def remove_file_from_vector_store(self, id_):
        """
        Remove a file from the vector store by its ID.

        :param id_: The ID of the file to remove.
        """

        CLIENT.beta.vector_stores.files.delete(
            vector_store_id=self.storage.id,
            file_id=id_
        )

    @staticmethod
    def remove_file_from_storage(id_):
        """
        Remove a file from the storage by its ID.

        :param id_: The ID of the file to remove.
        """

        CLIENT.files.delete(id_)

    def remove_file(self, file: VectorStoreFile, remove_file_on_storage=True):
        """
        Remove a file from the vector store and optionally from the storage.

        :param file: The VectorStoreFile object to remove.
        :param remove_file_on_storage: Whether to remove the file from the storage as well.
        """

        self.remove_file_from_vector_store(file.id)
        if remove_file_on_storage:
            BaseIntelligenceAssistant.remove_file_from_storage(file.id)
