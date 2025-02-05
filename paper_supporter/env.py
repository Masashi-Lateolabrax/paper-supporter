import os
from dotenv import load_dotenv

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
