from typing_extensions import override
from typing import Optional, Iterable

from openai import NotGiven, NOT_GIVEN, AssistantEventHandler, OpenAI
from openai.types import Metadata
from openai.types.beta import AssistantResponseFormatOptionParam, assistant_update_params
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai.lib.streaming import AssistantStreamManager


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        """
        Handles the event when a new text is created by the assistant.
        Prints the text to the console.
        """
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """
        Handles the event when there is a delta (change) in the text.
        Prints the delta value to the console.
        """
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        """
        Handles the event when a tool call is created by the assistant.
        Prints the type of the tool call to the console.
        """
        print(f"\nassistant > {tool_call.type}\n", flush=True)


class BaseAssistant:
    """
    BaseAssistant class to interact with the OpenAI assistant.
    """

    def __init__(self, client: OpenAI, model: str):
        """
        Initialize the BaseAssistant with a specific model.

        :param model: The model to use for the assistant.
        """
        self.client = client
        self.assistant = client.beta.assistants.create(
            model=model,
        )
        self.thread = client.beta.threads.create()

    def __del__(self):
        """
        Clean up the assistant and the conversation data when the object is deleted.
        """
        self.client.beta.assistants.delete(
            assistant_id=self.assistant.id
        )
        self.client.beta.threads.delete(
            thread_id=self.thread.id
        )

    def _modify(
            self,
            *,
            description: Optional[str] | NotGiven = NOT_GIVEN,
            instructions: Optional[str] | NotGiven = NOT_GIVEN,
            metadata: Optional[Metadata] | NotGiven = NOT_GIVEN,
            model: str | NotGiven = NOT_GIVEN,
            name: Optional[str] | NotGiven = NOT_GIVEN,
            response_format: Optional[AssistantResponseFormatOptionParam] | NotGiven = NOT_GIVEN,
            temperature: Optional[float] | NotGiven = NOT_GIVEN,
            tool_resources: Optional[assistant_update_params.ToolResources] | NotGiven = NOT_GIVEN,
            tools: Iterable[AssistantToolParam] | NotGiven = NOT_GIVEN,
            top_p: Optional[float] | NotGiven = NOT_GIVEN,
    ):
        """
        Modify the assistant's settings.

        :param description: The description of the assistant.
        :param instructions: The instructions for the assistant.
        :param metadata: Metadata for the assistant.
        :param model: The model to use for the assistant.
        :param name: The name of the assistant.
        :param response_format: The response format option.
        :param temperature: The temperature setting for the assistant.
        :param tool_resources: The tool resources for the assistant.
        :param tools: The tools to use with the assistant.
        :param top_p: The top_p setting for the assistant.
        """

        self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            description=description,
            instructions=instructions,
            metadata=metadata,
            model=model,
            name=name,
            response_format=response_format,
            temperature=temperature,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
        )

    def add_message(self, message: str):
        """
        Add a message to the conversation with the assistant.

        :param message: The message to add.
        """

        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

    def run(self, event_handler: EventHandler | None = None):
        """
        Start the assistant and generate responses based on the conversation.

        :param event_handler: The event handler to use for handling events.
        :return: The final response text from the assistant.
        """
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=event_handler,
        ) as stream:
            stream.until_done()
        return stream.current_message_snapshot.content[0].text.value

    def stream(self) -> AssistantStreamManager:
        """
        Start the assistant and generate responses based on the conversation.
        """
        return self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

    def clear_messages(self):
        """
        Clear the conversation with the assistant.
        """
        thread_messages = self.client.beta.threads.messages.list(self.thread.id)
        for msg in thread_messages:
            self.client.beta.threads.messages.delete(
                message_id=msg.id,
                thread_id=self.thread.id,
            )

    def set_instructions(self, instructions: str):
        """
        Set the instructions for the assistant.

        :param instructions: The instructions to set.
        """
        self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            instructions=instructions,
        )
