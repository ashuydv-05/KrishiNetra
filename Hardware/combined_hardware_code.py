import serial
import json
import joblib
import numpy as np
import time

model = joblib.load("cotton_disease_model.pkl")

esp = serial.Serial('/dev/ttyTHS1', 9600, timeout=0.5)
npk = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)



print("📡 Sent to ESP")
print("-----------------------------")
print("✅ System Ready...")

temp = hum = soil = light = None
N = P = K = None

while True:
    try:
        # -------- ESP --------
        if esp.in_waiting:
            esp_line = esp.readline().decode(errors='ignore').strip()

            if esp_line.startswith("{"):
                print("ESP RAW:", esp_line)

                data = json.loads(esp_line)
                temp = data["temp"]
                hum = data["hum"]
                soil = data["soil"]
                light = data["light"]

        # -------- NPK --------
        if npk.in_waiting:
            line = npk.readline().decode(errors='ignore').strip()

            if "Nitrogen" in line:
                N = int(line.split(":")[1].split()[0])

            elif "Phosphorous" in line:
                P = int(line.split(":")[1].split()[0])

            elif "Potassium" in line:
                K = int(line.split(":")[1].split()[0])

        # -------- PREDICTION --------
        if None not in (temp, hum, soil, light, N, P, K):

            print("\n--- COMBINED DATA ---")
            print(f"T:{temp} H:{hum} Soil:{soil} Light:{light}")
            print(f"N:{N} P:{P} K:{K}")

            input_data = np.array([[N, P, K, soil, temp, hum, light]])
            prediction = model.predict(input_data)[0]

            print("🔥 FINAL PREDICTION:", prediction)
            print("-----------------------------")

            # -------- SEND BACK TO ESP --------
            send_data = {
                "temp": temp,
                "hum": hum,
                "soil": soil,
                "light": light,
                "N": N,
                "P": P,
                "K": K,
                "prediction": str(prediction)
            }

            print("📤 Sending to ESP:", send_data)

            esp.write((json.dumps(send_data) + "\n").encode())
            time.sleep(2)

            # reset NPK
            N = P = K = None

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
