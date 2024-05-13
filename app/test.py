from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid

from voice_model.voicevox import Voicevox


voice_list = Voiceroid.voice_list()
voice_list = Voicevox.voice_list()
voice_list = Softalk.voice_list()

print(voice_list)
