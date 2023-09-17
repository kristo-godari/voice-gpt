from pydub import AudioSegment
from pydub.playback import play


class AudioPlayer:
    def __init__(self, config):
        self.config = config

    def play_audio(self, audio_bytes):
        print("Started playing audio from memory")
        song = AudioSegment.from_file(audio_bytes, format="mp3")
        play(song)