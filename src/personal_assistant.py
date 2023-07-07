import wx

import assistant_ui
from src.assistant_config import AssistantConfig
from src.audio_player import AudioPlayer
from src.audio_recorder import AudioRecorder
from src.speach_to_text import SpeechToTextConverter
from src.text_to_speach import TextToSpeechConverter
from src.conversation_engine import ConversationEngine


class EventHandler:
    RECORDING_STARTED = "RECORDING_STARTED"
    RECORDING_STOPPED = "RECORDING_STOPPED"
    PROMPT = ""

    def __init__(self, audio_player, audio_recorder, text_to_speech_converter, speech_to_text_converter, conversation_engine, frame):
        self.audio_player = audio_player
        self.audio_recorder = audio_recorder
        self.text_to_speech_converter = text_to_speech_converter
        self.speech_to_text_converter = speech_to_text_converter
        self.conversation_engine = conversation_engine
        self.frame = frame

    def handle_event(self, event):
        if event == self.RECORDING_STARTED:
            print("RECORDING_STARTED")
            self.audio_recorder.startRecording()

        elif event == self.RECORDING_STOPPED:
            print("RECORDING_STOPPED")
            self.audio_recorder.stopRecording()

            text = self.speech_to_text_converter.speech_to_text()
            frame.appendMessage(text, "Human")
            self.PROMPT = self.PROMPT + text + "\n AI: "

            response = self.conversation_engine.chat(self.PROMPT)
            self.PROMPT = self.PROMPT + response + "\n Human: "

            frame.appendMessage(response, "AI")

            text_to_speech_converter.text_to_speech(response)
            audio_player.play_audio()

        else:
            print("OTHER")
        pass


if __name__ == "__main__":

    # configure objects
    app = wx.App()
    config = AssistantConfig()
    audio_player = AudioPlayer(config)
    audio_recorder = AudioRecorder(config)
    text_to_speech_converter = TextToSpeechConverter(config)
    speech_to_text_converter = SpeechToTextConverter(config)
    conversation_engine = ConversationEngine(config)
    frame = assistant_ui.ChatRecorderFrame(None)
    event_handler = EventHandler(audio_player, audio_recorder, text_to_speech_converter, speech_to_text_converter, conversation_engine, frame)

    # create frame
    frame.event_handler = event_handler
    frame.Show()

    # get initial response
    initial_response = conversation_engine.chat(config.get_initial_prompt())
    # update prompt, conversation engine needs the whole context every time
    event_handler.PROMPT = config.get_initial_prompt() + initial_response + "\n Human: "
    # show it in ui
    frame.appendMessage(initial_response, "AI")
    # convert it to audio and store it locally
    text_to_speech_converter.text_to_speech(initial_response)
    # play the audio
    audio_player.play_audio()

    # start app
    app.MainLoop()
