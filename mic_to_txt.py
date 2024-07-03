import os
import wave
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
import io

# Google Cloud 서비스 계정 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

def record_audio(file_path, record_seconds=5):
    """
    마이크 입력을 받아 WAV 파일로 저장하는 함수
    :param file_path: 저장할 WAV 파일 경로
    :param record_seconds: 녹음할 시간(초)
    """
    chunk = 1024  # 1024 샘플 단위로 녹음
    sample_format = pyaudio.paInt16  # 16비트 샘플 포맷
    channels = 1  # 모노 채널
    fs = 44100  # 초당 44100 샘플

    p = pyaudio.PyAudio()  # PortAudio 인터페이스 생성

    print('Recording')

    # 녹음 스트림 열기
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # 프레임을 저장할 배열 초기화

    # 지정된 시간 동안 데이터를 청크 단위로 저장
    for _ in range(0, int(fs / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # 스트림 정지 및 종료
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    # 녹음된 데이터를 WAV 파일로 저장
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(file_path):
    """
    WAV 파일을 텍스트로 변환하는 함수
    :param file_path: 입력 WAV 파일 경로
    :return: 변환된 텍스트 리스트
    """
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",  # 한국어로 설정
    )

    response = client.recognize(config=config, audio=audio)

    # 응답에서 변환된 텍스트 추출
    transcriptions = []
    for result in response.results:
        transcriptions.append(result.alternatives[0].transcript)

    return transcriptions

def save_transcriptions(transcriptions, output_file):
    """
    변환된 텍스트를 TXT 파일로 저장하는 함수
    :param transcriptions: 변환된 텍스트 리스트
    :param output_file: 저장할 TXT 파일 경로
    """
    with open(output_file, 'w') as f:
        for transcription in transcriptions:
            f.write(transcription + '\n')

def main():
    audio_file = 'output.wav'  # 녹음할 WAV 파일 경로
    text_file = 'output.txt'  # 저장할 TXT 파일 경로

    # Step 1: 마이크 입력을 받아 WAV 파일로 저장
    record_audio(audio_file, record_seconds=10)

    # Step 2: WAV 파일을 텍스트로 변환
    transcriptions = transcribe_audio(audio_file)

    # Step 3: 변환된 텍스트를 TXT 파일로 저장
    save_transcriptions(transcriptions, text_file)

    print(f"Transcriptions saved to {text_file}")

if __name__ == "__main__":
    main()
