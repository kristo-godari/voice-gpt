import whisper


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config
        self.model = whisper.load_model("base")

    def speech_to_text(self):
        result = self.model.transcribe(self.config.get_record_audio_output_file(), fp16=False)
        return result["text"]
