import numpy as np
import pandas as pd

np.random.seed(42)

NUM_SAMPLES = 7500

data = []

def decide_remedy(n, p, k, moisture, light, temp, humidity):
    if moisture < 30:
        return "Irrigation_Needed"

    elif light < 300:
        return "Shade_Or_Light_Adjustment"

    elif n < 40:
        return "Urea"

    elif p < 25:
        
        return "DAP"

    elif k < 30:
        return "MOP"

    elif n < 50 and p < 35 and k < 40:
        return "NPK_19_19_19"

    elif temp > 36 and humidity > 75:
        return "Fungal_Disease_Remedy"

    elif temp > 35 and moisture > 70:
        return "Root_Rot_Prevention"

    elif humidity < 35 and moisture < 40:
        return "Organic_Compost"

    elif n > 100 or p > 80 or k > 90:
        return "No_Fertilizer_Needed"

    else:
        return "No_Remedy_Needed"


for _ in range(NUM_SAMPLES):
    nitrogen = np.random.randint(10, 130)
    phosphorus = np.random.randint(10, 100)
    potassium = np.random.randint(10, 120)

    soil_moisture = np.random.uniform(15, 90)
    light_intensity = np.random.uniform(100, 1200)

    temperature = np.random.uniform(20, 42)
    humidity = np.random.uniform(25, 95)

    remedy = decide_remedy(
        nitrogen,
        phosphorus,
        potassium,
        soil_moisture,
        light_intensity,
        temperature,
        humidity
    )

    data.append([
        nitrogen,
        phosphorus,
        potassium,
        round(soil_moisture, 2),
        round(light_intensity, 2),
        round(temperature, 2),
        round(humidity, 2),
        remedy
    ])

df = pd.DataFrame(data, columns=[
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Soil_Moisture",
    "Light_Intensity",
    "Temperature",
    "Humidity",
    "Remedy"
])

df.to_csv("cotton_remedy_dataset.csv", index=False)

print("Dataset generated successfully!")
print("File saved as cotton_remedy_dataset.csv")
print(df.head())
print(df["Remedy"].value_counts())