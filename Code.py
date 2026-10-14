import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = "COM9" \
""   # Arduino COM port
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=2)

time.sleep(2)

print("Connected to", PORT)

# ---------------------------------
# Function to request sensor values
# ---------------------------------
def request_reading(command):

    ser.reset_input_buffer()

    print(f"Sending command: {command}")

    ser.write((command + "\n").encode())

    values = []

    while True:

        line = ser.readline().decode(errors='ignore').strip()

        if not line:
            continue

        print("Received:", line)

        if line == "END":
            break

        try:
            led, val = line.split(",")
            values.append(int(val))

        except:
            pass

    return values


# -----------------------------
# STEP 1 → Get I0
# -----------------------------
input("Press ENTER for I0...")
I0 = request_reading("I0")

# -----------------------------
# STEP 2 → Get I
# -----------------------------
input("Press ENTER for I...")
I = request_reading("I")

# -----------------------------
# STEP 3 → Calculate Absorbance
# -----------------------------
I0 = np.array(I0, dtype=float)
I = np.array(I, dtype=float)

I[I == 0] = 1e-6

# Absorbance formula
Absorbance = np.log10(I0 / I)

# Convert to percentage scale
Absorbance = Absorbance * 100

# Remove negative values
Absorbance[Absorbance < 0] = 0

# Swap 2nd and 3rd values
if len(Absorbance) >= 3:
    Absorbance[1], Absorbance[2] = Absorbance[2], Absorbance[1]

print("\nFinal Absorbance Values (%):")
print(Absorbance)

# -----------------------------
# STEP 4 → Plot Graph
# -----------------------------
wavelengths = [405, 465, 520, 585, 605, 625]

plt.plot(wavelengths, Absorbance, marker='o')

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance (%)")

plt.title("Absorbance Spectrum (Final Processed)")

plt.grid(True)

plt.show()

# -----------------------------
# STEP 5 → Send to Arduino (HC-05)
# -----------------------------
abs_string = ",".join([f"{x:.4f}" for x in Absorbance])

send_command = "ABS:" + abs_string

ser.write((send_command + "\n").encode())

print("\nSent to Arduino:")
print(send_command)

ser.close()