from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from paper_supporter.lib.openai.base_assistant import BaseAssistant


def main():
    """
    Main function to interact with the BaseAssistant using a streaming interface.
    It sends a message to the assistant and processes the streamed response.

    The function performs the following steps:
    1. Initializes an empty list to store the response.
    2. Creates an instance of BaseAssistant with the model 'gpt-4o-mini'.
    3. Adds a message to the assistant.
    4. Opens a streaming session with the assistant.
    5. Iterates over the events in the stream.
    6. If the event is of type ThreadMessageDelta, extracts the text content and appends it to the response list.
    7. Prints the concatenated response.

    The `delta` variable represents the text change (delta) received from the assistant during the streaming session.
    Specifically, it is a part of the text extracted from the `ThreadMessageDelta` event data.
    This delta is used to build the final response by appending each piece of text received in real-time.

    Returns:
        None
    """
    response = []
    assistant = BaseAssistant("gpt-4o-mini")
    assistant.add_message("Hello, how are you?")
    with assistant.stream() as stream:
        for event in stream:
            # print(f"[DEBUG] {event}\n")
            if isinstance(event, ThreadMessageDelta):
                delta = event.data.delta.content[0].text.value
                print(delta, end="")
                response.append(delta)
    print()

    print("".join(response))


if __name__ == '__main__':
    main()
