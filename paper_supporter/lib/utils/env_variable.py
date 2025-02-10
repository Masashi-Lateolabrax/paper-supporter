import dataclasses
import os
from dotenv import load_dotenv, set_key
from openai import OpenAI


@dataclasses.dataclass
class EnvVariable:
    ORGANIZATION = None
    PROJECT = None
    OPENAI_API_KEY = None
    CLIENT = None

    def __init__(self, env_file_path):
        # Check if env_file_path is absolute path. If not, make it absolute path.

        if not os.path.exists(env_file_path):
            print("paper-supporterフォルダの直下に.envファイルを作成してください.")
            print(".envファイルに「ORGANIZATION」「PROJECT」「OPENAI_API_KEY」を記述してください.")

        self.env_file_path = env_file_path

        load_dotenv(self.env_file_path)

        EnvVariable.ORGANIZATION = os.getenv("ORGANIZATION")
        EnvVariable.PROJECT = os.getenv("PROJECT")
        EnvVariable.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        EnvVariable.CLIENT = OpenAI(
            organization=EnvVariable.ORGANIZATION,
            project=EnvVariable.PROJECT,
            api_key=EnvVariable.OPENAI_API_KEY
        )

        self._id = os.getenv("ASSISTANT_VECTOR_STORE_ID")
        if not self._id or self._id.strip() == "":
            self._id = self._create_vector_store()

    def _create_vector_store(self):
        vector_store = EnvVariable.CLIENT.beta.vector_stores.create()
        set_key(self.env_file_path, "ASSISTANT_VECTOR_STORE_ID", vector_store.id)
        return vector_store.id

    def get_vector_store_id(self):
        return self._id

    def set_vector_store_id(self, value):
        self._id = value
        set_key(self.env_file_path, "ASSISTANT_VECTOR_STORE_ID", value)
