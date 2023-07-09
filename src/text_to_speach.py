from TTS.api import TTS


class TextToSpeechConverter:

    def __init__(self, config):
        self.config = config
        self.model_name = TTS.list_models()[0]
        self.tts = TTS(self.model_name)

    def text_to_speech(self, text):
        self.tts.tts_to_file(text=text, speaker=self.tts.speakers[1], language=self.tts.languages[0], file_path=self.config.get_text_to_speech_output_file())