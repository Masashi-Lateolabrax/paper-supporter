import time

from openai import OpenAI
from openai.types import FileObject
from openai.types.beta import VectorStore
from openai.types.beta.vector_stores import VectorStoreFile


class FileManager:
    """
    OpenAIのサーバーで管理されているファイルを操作するためのクラス
    """

    def __init__(self, client: OpenAI, vector_store_id=None):
        self.client = client

        if vector_store_id is None:
            self.vector_store: VectorStore = self.client.beta.vector_stores.create()
        else:
            existing_vector_store = next(
                (x for x in self.client.beta.vector_stores.list() if x.id == vector_store_id),
                None
            )
            if existing_vector_store:
                self.vector_store: VectorStore = existing_vector_store
            else:
                print(f"Vector store with ID {vector_store_id} not found. Creating a new vector store.")
                self.vector_store: VectorStore = self.client.beta.vector_stores.create()

    def upload_file(self, file_object) -> FileObject:
        """
        ファイルをアップロードする
        """
        return self.client.files.create(
            file=file_object,
            purpose="assistants",
        )

    def get_files(self) -> list[FileObject]:
        """
        アップロードされているファイルの一覧を取得する
        """
        return [x for x in self.client.files.list()]

    def remove_file(self, file: FileObject) -> bool:
        """
        アップロードされているファイルを消去する
        """
        return self.client.files.delete(file.id).deleted

    def attach_file(self, file: FileObject) -> VectorStoreFile | None:
        """
        アップロードされているファイルをVector Storeにアタッチする
        """
        attached_file = self.client.beta.vector_stores.files.create(
            vector_store_id=self.vector_store.id,
            file_id=file.id
        )
        while attached_file.status == "in_progress":
            print(attached_file.status)
            time.sleep(1)
            attached_file: VectorStoreFile = self.client.beta.vector_stores.files.retrieve(
                vector_store_id=self.vector_store.id,
                file_id=file.id
            )

        match attached_file.status:
            case "failed":
                print("Failed to attach file.")
                return None
            case "cancelled":
                print("Cancelled to attach file.")
                return None
            case "completed":
                print("Attached file.")

        return attached_file

    def detach_file(self, file: FileObject) -> VectorStoreFile | None:
        """
        アップロードされているファイルをVector Storeからデタッチする
        """
        attached_file_list = self.get_attached_files()
        vector_store_file = next((x for x in attached_file_list if x.id == file.id), None)
        if vector_store_file is None:
            print("File is not attached to the vector store.")
            return None

        res = self.client.beta.vector_stores.files.delete(
            vector_store_id=self.vector_store.id,
            file_id=vector_store_file.id
        )
        if not res.deleted:
            print("Failed to detach file.")
            return None

        vector_store_file = self.client.beta.vector_stores.files.retrieve(
            vector_store_id=self.vector_store.id,
            file_id=vector_store_file.id
        )
        while vector_store_file.status == "in_progress":
            print(vector_store_file.status)
            time.sleep(1)
            vector_store_file = self.client.beta.vector_stores.files.retrieve(
                vector_store_id=self.vector_store.id,
                file_id=vector_store_file.id
            )

        match vector_store_file.status:
            case "failed":
                print("Failed to detach file.")
                return None
            case "cancelled":
                print("Cancelled to detach file.")
                return None
            case "completed":
                print("Detached file.")

        return vector_store_file

    def get_attached_files(self) -> list[VectorStoreFile]:
        """
        Vector Storeにアタッチされているファイルの一覧を取得する
        """
        return [x for x in self.client.beta.vector_stores.files.list(self.vector_store.id)]
