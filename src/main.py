from dotenv import load_dotenv
import os
from PyInquirer import prompt
from examples import custom_style_3
import speech_recognition as sr
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')

recognizer = sr.Recognizer()
mic = sr.Microphone()

questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'Interacting with ChatGPT with your voice',
        'choices': ["Voice input", "Text input", "Exit"]
    }
]


def recognize_using_google(audio) -> dict:

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        print('Calling google to recognize audio')
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def listen():
    with mic as source:
        print('listening...')
        audio = recognizer.listen(source)
        print('Done!!')
    return audio


def forward_to_openai_chat(prompt):
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = completion.choices[0].text
    return response


def main() -> None:
    while True:
        options = prompt(questions, style=custom_style_3)
        if options.get('user_option') == 'Exit':
            print('Exiting GPT CLI...')
            break
        elif options.get('user_option') == 'Voice input':
            print('Start Talking...')
            audio = listen()
            text = recognize_using_google(audio)['transcription']
            print('generated prompt: ', text)
        elif options.get('user_option') == 'Text input':
            text = input('Write your input here: ')

        response = forward_to_openai_chat(text)
        print(f'Response from OpenAI:\n """{response}\n"""')


if __name__ == '__main__':
    main()
