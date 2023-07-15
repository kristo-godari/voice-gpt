import wx


class FlowOrchestrator:
    RECORDING_STARTED = "RECORDING_STARTED"
    RECORDING_STOPPED = "RECORDING_STOPPED"
    PROMPT = ""

    def __init__(self, audio_player, text_to_speech_converter, speech_to_text_converter, conversation_engine, ui,
                 config):
        self.audio_player = audio_player
        self.text_to_speech_converter = text_to_speech_converter
        self.speech_to_text_converter = speech_to_text_converter
        self.conversation_engine = conversation_engine
        self.ui = ui
        self.config = config

    def initialize(self):
        # Get initial response
        initial_response = self.conversation_engine.chat(self.config.get_initial_prompt())

        # Update prompt, conversation engine needs the whole context every time
        self.PROMPT = self.config.get_initial_prompt() + initial_response + "\n Human: "

        # Show it in UI
        wx.CallAfter(self.ui.appendMessage, initial_response, "AI")

        # Convert it to audio and store it locally
        audio_bytes = self.text_to_speech_converter.text_to_speech(initial_response)

        # Play the audio
        self.audio_player.play_audio(audio_bytes)

    def continue_conversation(self, recording_bytes):
        # convert speech to text
        text = self.speech_to_text_converter.speech_to_text(recording_bytes)

        wx.CallAfter(self.ui.appendMessage, text, "Human")

        # update prompt with new text
        self.PROMPT = self.PROMPT + text + "\n AI: "

        # send prompt to conversation engine
        response = self.conversation_engine.chat(self.PROMPT)
        self.PROMPT = self.PROMPT + response + "\n Human: "

        # update UI with response
        wx.CallAfter(self.ui.appendMessage, response, "AI")

        # convert response to audio
        audio_bytes = self.text_to_speech_converter.text_to_speech(response)

        # play audio
        self.audio_player.play_audio(audio_bytes)