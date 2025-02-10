import os

from paper_supporter.lib.openai import BaseFileAssistant, EventHandler


def main():
    assistant = BaseFileAssistant("gpt-4o-mini")

    while True:
        print("Please target file path")
        file_path = input("File Path> ")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                assistant.add_file(f)
            break

    while True:
        msg = input("user message> ").strip()
        if msg == "" or msg == "q" or msg == "exit":
            break
        assistant.add_message(msg)
        assistant.run(EventHandler())
        print()


if __name__ == '__main__':
    main()
