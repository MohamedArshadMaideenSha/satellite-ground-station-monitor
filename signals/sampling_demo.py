import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

os.makedirs("plots", exist_ok=True)

#Save the Current Plot to a File

def save(name):
  plt.savefig(f"plots/{name}.png", dpi=300, bbox_inches='tight')
  plt.close()
  print(f"Plot saved as 'plots/{name}.png'")

# smooth 5 Hz sine wave

F=5  # Frequency of the sine wave in Hz
t=np.linspace(0, 1, 10000)  # Time vector from 0 to 1 second
smooth_signal=np.sin(2*np.pi*F*t)  # Generate the sine wave

plt.figure(figsize=(8, 4))
plt.plot(t, smooth_signal, label='5 Hz Sine Wave', color='Red')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Smooth 5 Hz Sine Wave')
plt.legend()
plt.grid(True)
plt.show()
save("smooth_5hz_sine_wave")

#sample the wave at different rates
# ---------------------------------------------------------------
# Sampling theorem: you need MORE than 2 x F = 10 samples per second.

print("\nFor sampling the 5 Hz sine wave, you need more than 10 samples per second (Nyquist rate).")

for fs in [20, 50, 13, 21, 25]:  # Different sampling frequencies
    t_sampled = np.arange(0, 1, 1/fs)  # Sampled time vector
    sampled_signal = np.sin(2 * np.pi * F * t_sampled)  # Sampled sine wave

    plt.figure(figsize=(8, 4))
    plt.plot(t, smooth_signal, label='Original Signal', color='Red')
    plt.plot(t_sampled, sampled_signal, 'o-', label=f'Sampled at {fs} Hz', color='Blue')

    aliasing=F-fs*np.round(F/fs)
    if abs(aliasing) !=F:
        fake=np.sin(2*np.pi*aliasing*t_sampled)
        plt.plot(t_sampled, fake, 'x--', label="fake wave the dots follow {abs(aliasing):g}Hz)")
        print(f"fs = {fs:>2}: ALIASING. The dots look like a {abs(aliasing):g} Hz wave.")

    elif fs== 2*F:
         print(f"fs = {fs:>2}: exactly 2 x F. Every sample lands on a zero crossing, "
              "so all samples are zero. Not enough!")

    else:
        print(f"fs={fs:>2}: above 2 x F, so frequency is captured correctly. ")
plt.title(f"Sampling a 5 Hz wave at {fs} samples per second")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend(loc="upper right", fontsize=7)
plt.show()
save(f"sampling_{fs}.png")
    
 #Filter out 8hz noise from a 5 Hz sine wave

fs2 = 30 # safe: more than 2 x 8 Hz
ts2 = np.arange(0, 2, 1 / fs2)
mixed = np.sin(2 * np.pi * 3 * ts2) + np.sin(2 * np.pi * 8 * ts2)  
wanted = np.sin(2 * np.pi * 3 * ts2)  # what we hope to get back             

# Ideal filter: cut everything above 5 Hz in the frequency domain, perfectly sharp.

nyquist = fs2 / 2
b, a = butter(4, 5 / nyquist, btype="low")
real_filtered = filtfilt(b, a, mixed)
spectrum = np.fft.rfft(mixed)
freqs = np.fft.rfftfreq(len(mixed), 1 / fs2)
spectrum_ideal = spectrum.copy()
spectrum_ideal[freqs > 5] = 0
ideal_filtered = np.fft.irfft(spectrum_ideal, n=len(mixed))
plt.figure(figsize=(8, 4))
plt.plot(ts2, mixed, label="3 Hz + 8 Hz mixed", alpha=0.5)
plt.plot(ts2, ideal_filtered, label="ideal low-pass (5 Hz)")
plt.plot(ts2, real_filtered, "--", label="real filter (Butterworth, 5 Hz)")
plt.plot(ts2, wanted, ":", label="pure 3 Hz wave", color="black")
plt.title("Low-pass filtering: removing the 8 Hz part")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend(loc="upper right", fontsize=7)
plt.show()
save("lowpass_filter.png")


#Ideal Filter(The spectrum before and after the real filter (peaks at 3 Hz and 8 Hz).)

spectrum = np.fft.rfft(mixed)
freqs = np.fft.rfftfreq(len(mixed), 1 / fs2)
spectrum_ideal[freqs > 5] = 0
ideal_filtered = np.fft.irfft(spectrum_ideal, n=len(mixed))

# The spectrum before and after the real filter (peaks at 3 Hz and 8 Hz).
spec_before = np.abs(np.fft.rfft(mixed)) / len(mixed) * 2
spec_after = np.abs(np.fft.rfft(real_filtered)) / len(mixed) * 2
plt.figure(figsize=(8, 3))
plt.plot(freqs, spec_before, "o-", label="before filter")
plt.plot(freqs, spec_after, "s--", label="after real filter")
plt.axvline(5, color="gray", linestyle=":")
plt.title("Spectrum before and after the low-pass filter")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Strength")
plt.legend()
plt.show()
save("lowpass_spectrum.png")

print("\nDone. Open the plots folder and look at every picture.")
print("Then write 3 to 5 lines in notes.txt for each experiment.")
