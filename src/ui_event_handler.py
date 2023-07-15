import threading


class UiEventHandler:
    RECORDING_STARTED = "RECORDING_STARTED"
    RECORDING_STOPPED = "RECORDING_STOPPED"
    PROMPT = ""

    def __init__(self, audio_recorder, flow_orchestrator):
        self.audio_recorder = audio_recorder
        self.flow_orchestrator = flow_orchestrator

    def handle_event(self, event):
        if event == self.RECORDING_STARTED:
            threading.Thread(target=self.audio_recorder.startRecording).start()

        elif event == self.RECORDING_STOPPED:
            recording_bytes = self.audio_recorder.stopRecording()
            threading.Thread(target=self.flow_orchestrator.continue_conversation,  args=(recording_bytes,)).start()
        else:
            print("OTHER")
        pass
