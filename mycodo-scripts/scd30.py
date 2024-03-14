import json
import requests
from datetime import datetime


# app configuration
HUM_LOW = 55
HUM_HIGH = 90
CO2_HIGH = 1000
ALERT_HUM_LOW = HUM_LOW - 5
ALERT_HUM_HIGH = 98
ALERT_TEMP_LOW = 23
ALERT_TEMP_HIGH = 30.5
AIR_MINUTES = [11, 12, 41, 42]


class Pizdec:
    def __init__(
        self,
        hum_low=HUM_LOW,
        hum_high=HUM_HIGH,
        co2_high=CO2_HIGH,
        alert_hum_low=ALERT_HUM_LOW,
        alert_hum_high=ALERT_HUM_HIGH,
        alert_temp_low=ALERT_TEMP_LOW,
        alert_temp_high=ALERT_TEMP_HIGH,
        air_minutes=AIR_MINUTES,
    ):
        self.ip = "192.168.1.70"
        self.api_key = "TAW4NdoM1J79P22r9tfPkspouUaS/jLo3/SUYQ9pvnDQtongYMbMmJuj86JCOpk0hjVH0UhIEGQmECPo4KxytvAYNeq7dBNy91Q3BLkPlZ0XlDj/yilb7znLlYfkiAWsJDJndzUgy+VoxwGJxgTUn3WoU386yBAZTeYcg7rrcHE="
        self.headers = {
            "Accept": "application/vnd.mycodo.v1+json",
            "X-API-KEY": self.api_key,
        }
        self.switch1 = "47aaf93e-c13b-4b6e-9076-f17f456a2410"
        self.switch2 = "75dbe534-24ba-4e61-b554-81e4961d0726"
        self.switch3 = "924464f6-8023-44e8-b799-fc1543463c8e"
        self.switch4 = "17f73007-d5a9-458f-88ea-8d9253b5b956"
        self.hum_low = hum_low
        self.hum_high = hum_high
        self.co2_high = co2_high
        self.alert_hum_low = alert_hum_low
        self.alert_hum_high = alert_hum_high
        self.alert_temp_low = alert_temp_low
        self.alert_temp_high = alert_temp_high
        self.air_minutes = air_minutes

    def run(self):
        self.ctrl_hum()
        self.ctrl_air()
        self.ctrl_temp()

    def switch(self, output_id: str, state: bool):
        data = {
            "state": state,  # False = turning power ON
            "channel": 0,
        }
        endpoint = f"outputs/{output_id}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers, verify=False)
        print(response.json())
        return response.status_code

    def notify(self, text: str):
        requests.post(
            f"https://api.telegram.org/bot7081645135:AAEljjW626aZ7y70nNJMY54fEkaBOBjld_A/sendMessage?chat_id=-4139438850&text={text}"
        )

    def ctrl_hum(self):
        """
        humidifier power + alerts for humidity level
        """
        input_id = "cb7c9727-15ec-464f-be9c-a06d5e7d1ea0"
        input_unit = "percent"
        input_ch = "2"
        endpoint = f"/measurements/last/{input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self.notify("humidity measurement is offline")
            return None

        cur_minute = datetime.now().minute
        if cur_minute in self.air_minutes:
            self.switch(self.switch2, True)

        if value < self.hum_low:
            self.switch(self.switch3, False)

        if value > self.hum_high:
            self.switch(self.switch3, True)

        if value > self.alert_hum_high or value < self.alert_hum_low:
            self.notify(f"humidity level: {value} %")
        return None

    def ctrl_air(self):
        """
        fan power
        """
        input_id = "cb7c9727-15ec-464f-be9c-a06d5e7d1ea0"
        input_unit = "ppm"
        input_ch = "0"
        endpoint = f"/measurements/last/{input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self.notify("CO2 measurement is offline")
            return None

        if value > self.co2_high:
            self.switch(self.switch2, False)
            return None

        cur_minute = datetime.now().minute
        if cur_minute in self.air_minutes:
            self.switch(self.switch2, False)
        else:
            self.switch(self.switch2, True)

        return None

    def ctrl_temp(self):
        """
        alerts for temperature
        """
        input_id = "cb7c9727-15ec-464f-be9c-a06d5e7d1ea0"
        input_unit = "C"
        input_ch = "1"
        endpoint = f"/measurements/last/{input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self.notify("temperature measurement is offline")
            return None

        if value < self.alert_temp_low or value > self.alert_temp_high:
            self.notify(f"temperature: {value}")


Pizdec().run()
