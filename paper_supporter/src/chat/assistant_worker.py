import enum
from PySide6.QtCore import Signal, Slot, QMutex, QThread, QMutexLocker
from openai.types.beta.assistant_stream_event import ThreadMessageDelta

from paper_supporter.lib.openai import BaseIntelligenceAssistant


class AssistantWorkerState(enum.Enum):
    Idle = enum.auto()
    Processing = enum.auto()
    NeedExecution = enum.auto()


class AssistantWorker(QThread):
    assistant_text_delta = Signal(str)

    def __init__(self, model: str, vector_store_id: str = None, parent=None):
        super().__init__(parent)
        self.assistant = BaseIntelligenceAssistant(model, vector_store_id)
        self.mutex = QMutex()
        self.message = ""
        self.state = AssistantWorkerState.Idle

    def __del__(self):
        self._cleanup()

    def _cleanup(self):
        try:
            self.requestInterruption()
            self.wait()
        except Exception as e:
            print(f"Exception in _cleanup: {e}")

    @Slot(str)
    def receive_message(self, message: str):
        with QMutexLocker(self.mutex):
            if self.state == AssistantWorkerState.Idle:
                self.state = AssistantWorkerState.NeedExecution
                self.message = message

    def _process_messages(self, message: str):
        self.assistant.add_message(message)
        debug = []
        with self.assistant.stream() as stream:
            for event in stream:
                if isinstance(event, ThreadMessageDelta):
                    delta = event.data.delta.content[0].text.value
                    self.assistant_text_delta.emit(delta)
                    debug.append(delta)
        print(f"DEBUG: assistant> {debug}")

    def run(self):
        while not self.isInterruptionRequested():
            with QMutexLocker(self.mutex):
                if self.state == AssistantWorkerState.NeedExecution:
                    self.state = AssistantWorkerState.Processing
                    msg = self.message
                    self.message = ""
                else:
                    continue

            if msg:
                self._process_messages(msg)

            with QMutexLocker(self.mutex):
                self.state = AssistantWorkerState.Idle
