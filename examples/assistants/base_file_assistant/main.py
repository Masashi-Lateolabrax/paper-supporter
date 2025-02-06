from paper_supporter.lib.openai import BaseFileAssistant, EventHandler


def main():
    assistant = BaseFileAssistant("gpt-4o-mini")
    with open("./sample_file.md", "rb") as f:
        assistant.add_file(f)

    assistant.add_message("あなたが管理している「sample_file.md」というファイルに指示されている数字を答えなさい.")
    assistant.run(EventHandler())

    # 期待する出力は「55626054」


if __name__ == '__main__':
    main()
