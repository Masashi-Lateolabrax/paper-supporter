from paper_supporter.lib.openai import BaseAssistant, EventHandler


def main():
    assistant = BaseAssistant("gpt-4o-mini")
    for _ in range(5):
        assistant.add_message(
            input("> ")
        )
        assistant.run(EventHandler())
        print()


if __name__ == '__main__':
    main()
