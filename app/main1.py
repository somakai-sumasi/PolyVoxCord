import pyvcroid2
import threading
import time
import winsound

def display_phonetic_label(tts_events):
    start = time.perf_counter()
    now = start
    for item in tts_events:
        tick = item[0] * 0.001
        type = item[1]
        if type != pyvcroid2.TtsEventType.PHONETIC:
            continue
        while (now - start) < tick:
            time.sleep(tick - (now - start))
            now = time.perf_counter()
        value = item[2]
        print(value, end="", flush=True)
    print("")

with pyvcroid2.VcRoid2() as vc:

    vc.loadLanguage("standard_kansai")
    vc.loadVoice('zunko_44')

    # Set parameters
    vc.param.volume = 1
    vc.param.speed = 1
    vc.param.pitch = 1
    vc.param.emphasis = 1
    vc.param.pauseMiddle = 150
    vc.param.pauseLong = 370
    vc.param.pauseSentence = 800
    vc.param.masterVolume = 1

    # Text to speech
    speech, tts_events = vc.textToSpeech("こんにちは。明日の天気は晴れの予報です")


    winsound.PlaySound(speech, winsound.SND_MEMORY)

