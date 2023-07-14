import os
from retry import retry


class AudioPlayer:
    def __init__(self, config):
        self.config = config

    @retry(Exception, tries=3, delay=0)
    def play_audio(self):
        print(f"Started playing audio from file: \n {self.config.get_text_to_speech_output_file()} \n")
        if os.name == 'nt':  # Windows
            os.startfile(self.config.get_text_to_speech_output_file())
        elif os.name == 'posix':  # Linux/Mac
            os.system('afplay "{}"'.format(self.config.get_text_to_speech_output_file()))
