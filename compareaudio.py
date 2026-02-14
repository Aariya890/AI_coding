import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore

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
        p.terminate()

        return b"".join(frames), rate
    

def analyse_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    energy = float(np.mean(samples.astype(np.float64) ** 2))
    return{
        "samples": samples,
        "duration": len(samples) / rate,
        "avg_volume": float(np.mean(np.abs(samples))),
        "max_amplitude": int(np.max(np.abs(samples))),
        "energy": energy
    }


def compare_adio(a, b):
    print(Fore.CYAN + "\nComparison Result")
    print(Fore.CYAN + "-" * 40)

    duration_diff = abs(a["duration"] - b["duration"]) / min(a["duration"], b["duration"]) * 100
    volume_diff = abs(a["avg_volume"] - b["avg_volume"]) / min(a["avg_volume"], b["avg_volume"]) * 100
    energy_diff = abs(a["energy"] - b["energy"]) / min(a["energy"], b["energy"]) * 100

    print("Longer Recording       :", "File 1" if a["duration"] > b["duration"] else "File 2")
    print("Duration Difference %  :", f"{duration_diff:.2f}")

    print("Louder Recording       :", "File 1" if a["avg_volume"] > b["avg_volume"] else "File 2")
    print("Volume Difference %    :", f"{volume_diff:.2f}")
    
    print("Higher peak amplitude :", "File 1" if a["max_amplitude"] > b["max_amplitude"] else "File 2")
    print("Higher signal energy  :", "File 1" if a["energy"] > b["energy"] else "File 2")
    print("Energy Difference %   :", f"{energy_diff:.2f}")


def     