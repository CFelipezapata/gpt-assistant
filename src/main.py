import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()
    
def recognize_using_google(audio) -> dict:
    
    response = {
            "success": True,
            "error": None,
            "transcription": None
        }
    try:
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    
    return response

def main() -> None:

    with mic as source:
        print('listening...')
        audio = recognizer.listen(source)
        print('Completed!!')
    
    print('Calling whisper to recognize audio')
    recognize_using_google(audio)


if __name__ == '__main__':
    main()
    
