import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio

def plot_audio(frequencies, amplitudes, waveform, sample_rate, zoom=None, volume=0.1):
    
    time = np.arange(waveform.shape[0]) / sample_rate

    fig, axes = plt.subplots(3, 1, sharex=True)
    axes[0].plot(time, amplitudes)
    axes[0].set(ylabel="Amplitude", xlabel="Time, s", ylim=[-0.03 if np.all(amplitudes >= 0.0) else None, None])
    axes[1].plot(time, waveform)
    axes[1].set(ylabel="Amplitude", xlabel="Time, s")
    axes[2].specgram(waveform, Fs=sample_rate)
    axes[2].set(ylabel="Frequency, Hz", xlabel="Time, s", xlim=[-0.01, time[-1] + 0.01], ylim=[0,3000])

    for ax in axes:
        ax.grid(True)
    pos = axes[1].get_position()
    fig.tight_layout()

    if zoom is not None:
        zoom_ax = fig.add_axes([pos.x0 + 0.02, pos.y0 + 0.03, pos.width / 2.5, pos.height / 2.0])
        zoom_ax.plot(time, waveform)
        zoom_ax.set(xlim=zoom, xticks=[], yticks=[])

    waveform /= np.abs(waveform).max()
    return Audio(volume * waveform, rate=sample_rate, normalize=False)