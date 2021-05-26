from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

import os
import wave
import json

def speech_to_text(wav_file_name, to_file=False):
    """Transcribes an .wav file to text and returns text as a string.
    :param wav_file_name: .wav file in current directory
    :returns: transcribed text as a string
    """
    SetLogLevel(0)
    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)
    wf = wave.open(wav_file_name, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    res = json.loads(rec.FinalResult())
    final_text = res['text']
    if to_file:
        with open(str(wav_file_name[0:-4]) + "_asr_output.txt", "w") as text_file:
            text_file.write(final_text)
    return final_text


def mp3_to_wav(mp3_file_name):
    """Converts an .mp3 file like 'audio.mp3' to a wav file like 'audio.wav' and
    places the new file into the current directory.
    :param mp3_file_name: .mp3 file in current directory
    :returns: new file name ending with .wav instead of .mp3
    """
    if mp3_file_name[-4:len(mp3_file_name)] != ".mp3":
        raise Exception("Audio file must be in .mp3 format")
    file_wav = mp3_file_name[0:-4] + ".wav"
    sound = AudioSegment.from_mp3(mp3_file_name)
    sound = sound.set_channels(1) # Convert to MONO CHANNEL
    sound.export(file_wav, format="wav")
    return file_wav

# wav_file = mp3_to_wav("federalplaza.mp3")
# print(wav_file)
# text = speech_to_text(wav_file, to_file=True)
# print(text)
