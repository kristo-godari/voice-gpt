from gtts import gTTS
import io


class TextToSpeechConverter:

    def __init__(self, config):
        self.config = config

    def text_to_speech(self, text):
        print(f"Started tex to speech process.")
        audio_bytes = io.BytesIO()
        tts = gTTS(text, lang=self.config.get_text_to_speech_lang())
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        print(f"Finished tex to speech process.")
        return audio_bytes
