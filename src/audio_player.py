import os


class AudioPlayer:
    def __init__(self, config):
        self.config = config

    def play_audio(self):
        if os.name == 'nt':  # Windows
            os.startfile(self.config.get_text_to_speech_output_file())
        elif os.name == 'posix':  # Linux/Mac
            os.system('afplay "{}"'.format(self.config.get_text_to_speech_output_file()))
