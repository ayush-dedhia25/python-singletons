import speech_recognition as sr


def list_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Device index {index}: {name}")


if __name__ == "__main__":
    list_microphones()
