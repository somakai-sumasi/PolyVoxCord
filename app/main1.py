from voice_model.voicevox import Voicevox

list = Voicevox.voice_list()
text = ""
for key, val in list.items():
    text += f"`{key}`   {val}\n"

print(text)
