import os
import time
import datetime
import threading
import scipy.io.wavfile
import sounddevice as sd

speech_mic = False

stop_event = threading.Event()

def record_audio(iteration=0):
    filename = f"recording_{iteration}.wav"
    os.system(f"python3 mic_to_wav.py {filename}")
    return filename


def convert_wav_to_txt(wav_file, iteration=0):
    input_txt = f"input_{iteration}.txt"
    os.system(f"python3 speech_recognition_wav.py --model=/home/jhw/workdir/food_pj/ingredient_check/speech_reco/public/wav2vec2-base/FP16/wav2vec2-base.xml -i {wav_file} --output={input_txt}")
    return input_txt



def thread_speech():
    while not stop_event.is_set():
         # 1. 마이크 입력을 .wav 파일로 저장
        wav_file = record_audio()
            
        # 2. .wav 파일을 .txt 파일로 변환
        input_txt = convert_wav_to_txt(wav_file)
        
        if "re" in input_txt:
            v_samplerate, v_data = scipy.io.wavfile.read('output.wav')
            sd.play(v_data, v_samplerate)