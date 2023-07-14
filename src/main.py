import wx
import threading
import assistant_ui

from src.assistant_config import AssistantConfig
from src.audio_player import AudioPlayer
from src.audio_recorder import AudioRecorder
from src.flow_orchestrator import FlowOrchestrator
from src.speach_to_text import SpeechToTextConverter
from src.text_to_speach import TextToSpeechConverter
from src.conversation_engine import ConversationEngine
from src.ui_event_handler import UiEventHandler


if __name__ == "__main__":

    # configure objects
    app = wx.App()
    config = AssistantConfig()
    audio_player = AudioPlayer(config)
    audio_recorder = AudioRecorder(config)
    text_to_speech_converter = TextToSpeechConverter(config)
    speech_to_text_converter = SpeechToTextConverter(config)
    conversation_engine = ConversationEngine(config)
    ui = assistant_ui.ChatUi(None)
    flow_orchestrator = FlowOrchestrator(audio_player, text_to_speech_converter, speech_to_text_converter, conversation_engine, ui, config)
    ui_event_handler = UiEventHandler(audio_recorder, flow_orchestrator)

    # set ui event handler
    ui.event_handler = ui_event_handler

    # initialize conversation in a separate thread
    initialization_thread = threading.Thread(target=flow_orchestrator.initialize)
    initialization_thread.start()

    # show the frame
    ui.Show()

    # start app
    app.MainLoop()
