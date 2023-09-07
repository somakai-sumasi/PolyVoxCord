import subprocess
import os
import subprocess
from dotenv import load_dotenv


os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()
SOF_TALK = os.getenv("WAV_FILE")
WAV_FILE = os.getenv("SOF_TALK")

_start = "start " + SOF_TALK
_speed = "/S:120"
_pitch = "/O:100"
_model = "/T:7/U:1"
_word = "/W:おはようございます"
_save = "/R:"+WAV_FILE+"test.wav"

_command = [_start, _speed, _pitch, _model, _save, _word]

subprocess.run(" ".join(_command), shell=True)
