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
        'message': 'Interact with ChatGPT with your voice or text',
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
        response['transcription'] = recognizer.recognize_google(audio, show_all=True)['alternative'][0]['transcript']
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def listen():
    with mic as source:
        print("Start talking, I'm listening...")
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
        temperature=0.6,
    )
    response = completion.choices[0].text
    print('\nResponse from OpenAI: \n\n', f'"""{response}\n\n"""')


def main() -> None:
    
    active_session = True
    
    while active_session:
        options = prompt(questions, style=custom_style_3)
        if options.get('user_option') == 'Exit':
            print('Exiting GPT CLI...')
            active_session = False
        elif options.get('user_option') == 'Voice input':
            audio = listen()
            speech_response = recognize_using_google(audio)
            if speech_response['success']:
                text = speech_response['transcription']
                print(f'\nGenerated prompt: {text}\n')
                forward_to_openai_chat(text)
            else:
                print(f'There was an error with the speech recognition tool: {speech_response["error"]}')
        elif options.get('user_option') == 'Text input':
            text = input('Type your input here: ')
            forward_to_openai_chat(text)
        


if __name__ == '__main__':
    main()
