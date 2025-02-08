import os
from dotenv import load_dotenv, set_key
from openai import OpenAI

env_file_path = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    ".env"
)
if not os.path.exists(env_file_path):
    print("paper_supporterフォルダの直下に.envファイルを作成してください.")
    print(".envファイルに「ORGANIZATION」「PROJECT」「OPENAI_API_KEY」を記述してください.")

load_dotenv()

ORGANIZATION = os.getenv("ORGANIZATION")
PROJECT = os.getenv("PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CLIENT = OpenAI(
    organization=ORGANIZATION,
    project=PROJECT,
    api_key=OPENAI_API_KEY
)


class _ASSISTANT_VECTOR_STORE_ID:
    def __init__(self):
        self._id = os.getenv("ASSISTANT_VECTOR_STORE_ID")
        if not self._id or self._id.strip() == "":
            self._id = self._create_vector_store()

    def get(self):
        return self._id

    def set(self, value):
        self._id = value
        set_key(env_file_path, "ASSISTANT_VECTOR_STORE_ID", value)

    @staticmethod
    def _create_vector_store():
        vector_store = CLIENT.beta.vector_stores.create()
        set_key(env_file_path, "ASSISTANT_VECTOR_STORE_ID", vector_store.id)
        return vector_store.id


ASSISTANT_VECTOR_STORE_ID = _ASSISTANT_VECTOR_STORE_ID()
