import os
import time
import datetime

def convert_wav_to_txt(wav_file):
    input_txt = f"input.txt"
    os.system(f"python3 speech_recognition_wav2vec_demo.py --model=public/wav2vec2-base/FP16/wav2vec2-base.xml -i {wav_file} --output={input_txt}")
    return input_txt

