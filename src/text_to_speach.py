from gtts import gTTS


class TextToSpeechConverter:

    def __init__(self, config):
        self.config = config

    def text_to_speech(self, text):
        tts = gTTS(text, lang=self.config.get_text_to_speech_lang())
        tts.save(self.config.get_text_to_speech_output_file())
