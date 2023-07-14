import configparser


class AssistantConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config/role-play-conversation.properties")
        self.get_text_to_speech_output_file_name = "tmp-output/text-to-speech-output.wav"
        self.get_record_audio_file_name = "tmp-output/recording-output.wav"

    def get_initial_prompt(self):
        return self.config.get("text", "initial-prompt")

    def get_text_to_speech_lang(self):
        return self.config.get("text", "text-to-speach-language")

    def get_openai_api_key(self):
        return self.config.get("text", "openai-api-key")

    def get_text_to_speech_output_file(self):
        return self.get_text_to_speech_output_file_name

    def get_record_audio_output_file(self):
        return self.get_record_audio_file_name
