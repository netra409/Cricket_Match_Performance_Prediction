import random
import time
from datetime import datetime

while True:

    pm25 = random.randint(20,200)
    pm10 = random.randint(40,250)

    aqi = int(pm25*0.5 + pm10*0.5)

    alert = "High Pollution" if aqi > 150 else "Normal"

    print("Time:", datetime.now())
    print("PM2.5:", pm25)
    print("PM10:", pm10)
    print("AQI:", aqi)
    print("Alert:", alert)
    print("-------------------")

    time.sleep(5)