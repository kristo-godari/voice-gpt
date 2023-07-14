import whisper
from retry import retry


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config
        self.model = whisper.load_model("base")

    @retry(Exception, tries=3, delay=0)
    def speech_to_text(self):
        print(f"Started convert speech to text.")
        result = self.model.transcribe(self.config.get_record_audio_output_file(), fp16=False)
        print(f"Text result is {result['text']}.")
        return result["text"]
