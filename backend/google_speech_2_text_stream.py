import os
from google.cloud import speech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech as cloud_speech_types

PROJECT_ID = "assignmentdatacenterscale"

def transcribe_streaming_v2(
    # audio_content,
) -> cloud_speech_types.StreamingRecognizeResponse:
    """Transcribes audio from an audio file stream using Google Cloud Speech-to-Text API.
    Args:
        stream_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.wav"
    Returns:
        list[cloud_speech_types.StreamingRecognizeResponse]: A list of objects.
            Each response includes the transcription results for the corresponding audio segment.
    """
    # Instantiates a client
    stream_file = 'audio_stream.wav'
    client = SpeechClient()
    with open(stream_file, "rb") as f:
        audio_content = f.read()

    # # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = min(len(audio_content) // 5, 25500)
    stream = [
        audio_content[start : start + chunk_length]
        for start in range(0, len(audio_content), chunk_length)
    ]

    audio_requests = (
        cloud_speech_types.StreamingRecognizeRequest(audio=audio) for audio in stream
    )

    recognition_config = cloud_speech_types.RecognitionConfig(
        auto_decoding_config=cloud_speech_types.AutoDetectDecodingConfig(),
        # encoding=cloud_speech_types.RecognitionConfig.,
        language_codes=["en-US"],
        model="long",
        # sample_rate_hertz=16000,

    )
    streaming_config = cloud_speech_types.StreamingRecognitionConfig(
        config=recognition_config
    )
    config_request = cloud_speech_types.StreamingRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        streaming_config=streaming_config,
    )

    def requests(config: cloud_speech_types.RecognitionConfig, audio: list) -> list:
        yield config
        yield from audio

    # Transcribes the audio into text
    responses_iterator = client.streaming_recognize(
        requests=requests(config_request, audio_requests)
    )

    responses = []
    for response in responses_iterator:
        responses.append(response)
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

    return responses
