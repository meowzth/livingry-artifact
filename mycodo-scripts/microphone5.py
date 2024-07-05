import json
import requests
from datetime import datetime


# app configuration
HUM_LOW = 84
HUM_HIGH = 90
CO2_HIGH = 1800
ALERT_HUM_LOW = 3
ALERT_HUM_HIGH = 98
ALERT_TEMP_LOW = 23
ALERT_TEMP_HIGH = 35
AIR_MINUTES = []


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
        self.ip = "10.42.0.99"
        self.api_key = "mnV33GeApzb6T4Jfe4E0+iLyXW4QRRrI/hBs8G2msBXGqJarD2fK8tn6vr6UwmLSB9jeXNOT6VG3qfkMSOYaFLMP5406tmS4cuvtH1kWA3EA8KnjDp2PrJ5lUhapTZHqeqIcngR5Q2kyCv7vr6T4DYFnqhoVTMKAdEZWXia+RuU="
        self.headers = {
            "Accept": "application/vnd.mycodo.v1+json",
            "X-API-KEY": self.api_key,
        }
        self.switch1 = "1f2fd544-5d36-4f33-9989-9a3839bb526f"
        self.switch2 = "d2095d22-56a2-438c-b31c-2d59b3ec042f"
        self.switch3 = "f4684276-8c5d-4ec8-836d-e79bb380ce7f"
        self.switch4 = "2fd77367-2b93-4666-a015-8bf7bd875d91"
        self.hum_low = hum_low
        self.hum_high = hum_high
        self.co2_high = co2_high
        self.alert_hum_low = alert_hum_low
        self.alert_hum_high = alert_hum_high
        self.alert_temp_low = alert_temp_low
        self.alert_temp_high = alert_temp_high
        self.air_minutes = air_minutes

    def run(self):
        self.ctrl_air()
        self.ctrl_hum()
        self.ctrl_temp()

    def switch(self, output_id: str, state: bool):
        data = {
            "state": state,
            "channel": 0,
        }
        endpoint = f"outputs/{output_id}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers, verify=False)
        return response.status_code

    def notify(self, text: str):
        requests.post(
            f"https://api.telegram.org/bot7081645135:AAEljjW626aZ7y70nNJMY54fEkaBOBjld_A/sendMessage?chat_id=-4139438850&text={text}"
        )

    def ctrl_hum(self):
        """
        humidifier power + alerts for humidity level
        """
        input_id = "33c38678-f6bc-4402-bd6d-d5c1970d02ff"
        input_unit = "percent"
        input_ch = "1"
        endpoint = f"/measurements/last/{input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]

        if value is None:
            self.notify("humidity measurement is offline")
            return None

        if value < self.hum_low:
            self.switch(self.switch3, True)

        if value > self.hum_high:
            self.switch(self.switch3, False)

        if value > self.alert_hum_high or value < self.alert_hum_low:
            self.notify(f"humidity level: {value} %")
        return None

    def ctrl_air(self):
        """
        fan power
        """
        cur_minute = datetime.now().minute
        #if cur_minute in self.air_minutes:
        if (cur_minute // 2) == (cur_minute / 2):
            self.switch(self.switch2, False)
        else:
            self.switch(self.switch2, True)

        return None

    def ctrl_temp(self):
        """
        alerts for temperature
        """
        input_id = "33c38678-f6bc-4402-bd6d-d5c1970d02ff"
        input_unit = "C"
        input_ch = "0"
        endpoint = f"/measurements/last/{input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]

        if value is None:
            self.notify("temperature measurement is offline")
            return None

        if value < self.alert_temp_low or value > self.alert_temp_high:
            self.notify(f"temperature: {value}")


Pizdec().run()
