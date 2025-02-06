from typing_extensions import override
from typing import Optional, Iterable

from openai import OpenAI, NotGiven, NOT_GIVEN, AssistantEventHandler
from openai.types import Metadata
from openai.types.beta import AssistantResponseFormatOptionParam, assistant_update_params
from openai.types.beta.assistant_tool_param import AssistantToolParam

from paper_supporter.env import ORGANIZATION, PROJECT, OPENAI_API_KEY

CLIENT = OpenAI(
    organization=ORGANIZATION,
    project=PROJECT,
    api_key=OPENAI_API_KEY
)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


class BaseAssistant:
    def __init__(self, model: str):
        self.assistant = CLIENT.beta.assistants.create(
            model=model,
        )
        self.thread = CLIENT.beta.threads.create()

    def __del__(self):
        CLIENT.beta.assistants.delete(
            assistant_id=self.assistant.id
        )
        CLIENT.beta.threads.delete(
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
        CLIENT.beta.assistants.update(
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
        CLIENT.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

    def run(self, event_handler: EventHandler | None = None):
        with CLIENT.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=event_handler,
        ) as stream:
            stream.until_done()
        return stream.current_message_snapshot.content[0].text.value

    def clear_messages(self):
        thread_messages = CLIENT.beta.threads.messages.list(self.thread.id)
        for msg in thread_messages:
            CLIENT.beta.threads.messages.delete(
                message_id=msg.id,
                thread_id=self.thread.id,
            )

    def set_instructions(self, instructions: str):
        CLIENT.beta.assistants.update(
            assistant_id=self.assistant.id,
            instructions=instructions,
        )
