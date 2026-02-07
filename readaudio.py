import sys
import pyaudio
import numpy as np
import speech_recognition as sr

from speech_recognition import AudioData
from colorama import Fore, Style, init

init(autoreset=True)

def record_audio(seconds, rate=16000):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=1024
    )

    frames = []
    for _ in range(int(rate / 1024 * seconds)):
        frames.append(stream.read(1024, exception_on_overflow=False))

    stream.stop_stream()
    stream.close()

    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    return b"".join(frames), rate, width


def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)

    return {
        "duration": len(samples) / rate,
        "avg_amplitude": float(np.mean(np.abs(samples))),
        "max_amplitude": int(np.max(np.abs(samples)))
    }


def recognize_speech(data, rate, width):
    recognizer = sr.Recognizer()
    audio = AudioData(data, rate, width)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


def main():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "========== AUDIO RECOGNIZER ==========")
    print(Fore.CYAN + "=" * 40)

    while True:
        user_input = input(
            Fore.YELLOW + "Enter duration in seconds (or type 'exit'): "
        ).strip().lower()

        if user_input == "exit":
            print(
                Fore.MAGENTA +
                "System exit acknowledged. Shutting down gracefully."
            )
            break

        if not user_input.isdigit() or int(user_input) <= 0:
            print(
                Fore.RED +
                "Invalid input. Please enter a positive number."
            )
            continue

        seconds = int(user_input)

        print(Fore.GREEN + "Recording audio...")
        audio, rate, width = record_audio(seconds)

        stats = analyze_audio(audio, rate)
        text = recognize_speech(audio, rate, width)

        print(Fore.CYAN + "\nResults")
        print(Fore.CYAN + "-" * 40)
        print(Fore.WHITE + f"Duration: {stats['duration']:.2f} seconds")
        print(Fore.WHITE + f"Avg amplitude: {stats['avg_amplitude']:.0f}")
        print(Fore.WHITE + f"Max amplitude: {stats['max_amplitude']}")

        if text:
            print(Fore.GREEN + f"Recognized text: {text}")
        else:
            print(
                Fore.RED +
                "Recognized text: Speech could not be recognised."
            )


if __name__ == "__main__":
    main()
