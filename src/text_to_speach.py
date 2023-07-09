from TTS.api import TTS


class TextToSpeechConverter:

    def __init__(self, config):
        self.config = config
        self.model_name = "tts_models/multilingual/multi-dataset/your_tts" if self.config.get_text_to_speech_lang() == "en" else "tts_models/de/thorsten/tacotron2-DDC"
        self.tts = TTS(self.model_name)

    def text_to_speech(self, text):
        self.tts.tts_to_file(text=text, speaker=self.tts.speakers[0], language=self.tts.languages[0], file_path=self.config.get_text_to_speech_output_file())