from tts import tts_module
import threading

stop_event = threading.Event()

def thread_tts():
    while not stop_event.is_set():
        with open('/home/jhw/workdir/food_pj/ingredient_check/ingred_list.txt', 'r') as file:
            content = file.read()
                
            
        tts_model_duration = '/home/jhw/workdir/food_pj/ingredient_check/tts/text-to-speech_xml/text-to-speech-en-0001-duration-prediction/FP16/text-to-speech-en-0001-duration-prediction.xml'
        tts_model_forward = '/home/jhw/workdir/food_pj/ingredient_check/tts/text-to-speech_xml/text-to-speech-en-0001-regression/FP16/text-to-speech-en-0001-regression.xml'
        tts_model_melgan = '/home/jhw/workdir/food_pj/ingredient_check/tts/text-to-speech_xml/text-to-speech-en-0001-generation/FP16/text-to-speech-en-0001-generation.xml'    
        device = 'CPU'

            
        tts_module.text_to_speech(content, tts_model_duration, tts_model_forward, tts_model_melgan, device)