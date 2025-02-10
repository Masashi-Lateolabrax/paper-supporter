import enum
from PySide6.QtCore import Signal, Slot, QMutex, QThread, QMutexLocker
from base_assistant_wrapper import ChatAssistant


class AssistantWorkerState(enum.Enum):
    Idle = enum.auto()
    Processing = enum.auto()
    NeedExecution = enum.auto()


class AssistantWorker(QThread):
    assistant_reply = Signal(str)

    def __init__(self, model: str, parent=None):
        super().__init__(parent)
        self.assistant = ChatAssistant(model)
        self.mutex = QMutex()
        self.message = ""
        self.state = AssistantWorkerState.Idle

    def __del__(self):
        self.requestInterruption()
        self.wait()

    @Slot(str)
    def exec(self, message: str):
        with QMutexLocker(self.mutex):
            if self.state == AssistantWorkerState.Idle:
                self.state = AssistantWorkerState.NeedExecution
                self.message = message

    def _process_messages(self, message: str):
        self.assistant.add_message(message)
        response = self.assistant.run()
        self.assistant_reply.emit(response)

    def run(self):
        while not self.isInterruptionRequested():
            with QMutexLocker(self.mutex):
                match self.state:
                    case AssistantWorkerState.Idle:
                        continue
                    case AssistantWorkerState.NeedExecution:
                        self.state = AssistantWorkerState.Processing
                        msg = self.message
                        self.message = ""
                    case _:
                        print("Invalid state")
                        continue

            self._process_messages(msg)

            with QMutexLocker(self.mutex):
                self.state = AssistantWorkerState.Idle
