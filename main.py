import os

from paper_supporter import main

env_file_path = "./.env"

if __name__ == '__main__':
    if not os.path.isabs(env_file_path):
        env_file_path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            env_file_path
        )
    main(env_file_path)
