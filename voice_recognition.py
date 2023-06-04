import pyttsx3
import requests
import speech_recognition as sr

# Text to speech recognition
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of the speaker
engine.setProperty("volume", 1.0)  # volume level of the speaker (0.0 to 1.0)


def speak_message(message: str) -> None:
    """Speaks a message to the speaker

    Args:
        message (str): A message to be sent to the speaker
    """
    engine.say(message)
    engine.runAndWait()


def ask_to_chatgpt(prompt: str) -> dict:
    """This method asks the prompt to the chatgpt and gets back its result

    Args:
        prompt (str): A prompt message to be sent to the chatgpt

    Returns:
        dict: Containing all the information about the prompt message
    """
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "e5e9d912c4msh3097411c99d1555p125313jsn61d97f29495a",
        "X-RapidAPI-Host": "openai80.p.rapidapi.com",
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(
        "https://openai80.p.rapidapi.com/chat/completions",
        headers=headers,
        json=payload,
    )
    data = response.json()
    return data


def process_chatgpt_data(data: dict):
    """Extract chatgpt data from a dictionary

    Args:
        data (dict): A raw data got from the chatgpt server

    Returns:
        dict: A dictionary containing its id, message, model and finish reason
    """
    try:
        response = {
            "id": data["id"],
            "message": data["choices"][0]["message"]["content"],
            "model": data["model"],
            "finish_reason": data["choices"][0]["finish_reason"],
        }
        return response
    except KeyError:
        speak_message("Oops! I cannot understand what you said.")
        print("Key not found in dictionary...")
        return None


def take_mic_input() -> str:
    """Takes a audio input from the microphone and converts it to a string.

    Returns:
        str: Converted texted from the audio input
    """
    r = sr.Recognizer()
    with sr.Microphone(device_index=18) as microphone:
        print("Listening...")
        r.adjust_for_ambient_noise(microphone)
        audio = r.listen(microphone)
        print("Processing your audio input...")
        try:
            text = r.recognize_google(audio, language="en-in")
            print(f"DEBUG: {text}")
            return text
        except sr.UnknownValueError:
            print("Unable to recognize audio input. Please try again...")
        except sr.RequestError:
            print(
                "Speech recognition service failed to recognize audio input. Please try again..."
            )


if __name__ == "__main__":
    try:
        prompt = take_mic_input()
        print("Analyzing your question, please wait... (can take some while)... ")
        if prompt is not None or prompt != "none" or prompt != "None":
            data = ask_to_chatgpt(prompt)
            response = process_chatgpt_data(data)
            if response is not None:
                speak_message(response["message"])
    except Exception as e:
        print(str(e))
    except KeyboardInterrupt:
        print("*--- You must have pressed ctrl+c to exit ---*")
        speak_message("Have a nice day!")
