import json
import requests
from datetime import datetime

# default app configuration, if None is provided
DEFAULT_CONFIG = {
    "installation_id": "LIVINGRY ARTIFACT",
    "ip": "192.168.1.70",
    "api_key": "TAW4NdoM1J79P22r9tfPkspouUaS/jLo3/SUYQ9pvnDQtongYMbMmJuj86JCOpk0hjVH0UhIEGQmECPo4KxytvAYNeq7dBNy91Q3BLkPlZ0XlDj/yilb7znLlYfkiAWsJDJndzUgy+VoxwGJxgTUn3WoU386yBAZTeYcg7rrcHE=",
    "input": "cb7c9727-15ec-464f-be9c-a06d5e7d1ea0",
    "outputs": [
        "47aaf93e-c13b-4b6e-9076-f17f456a2410",
        "75dbe534-24ba-4e61-b554-81e4961d0726",
        "924464f6-8023-44e8-b799-fc1543463c8e",
        "17f73007-d5a9-458f-88ea-8d9253b5b956",
    ],
    "conf": {
        "HUM_LOW": 55,
        "HUM_HIGH": 90,
        "CO2_HIGH": 1000,
        "ALERT_HUM_LOW": 50,
        "ALERT_HUM_HIGH": 98,
        "ALERT_TEMP_LOW": 23,
        "ALERT_TEMP_HIGH": 30.5,
        "AIR_MINUTES": [11, 12, 41, 42],
    },
}


class Pizdec:
    def __init__(
        self,
        conf=DEFAULT_CONFIG,
    ):
        self.installation_id = conf["installation_id"]
        self.ip = conf["ip"]
        self.api_key = conf["api_key"]
        self.headers = {
            "Accept": "application/vnd.mycodo.v1+json",
            "X-API-KEY": self.api_key,
        }
        self.switch1 = conf["outputs"][0]
        self.switch2 = conf["outputs"][1]
        self.switch3 = conf["outputs"][2]
        self.switch4 = conf["outputs"][3]
        self.hum_low = conf["conf"]["HUM_LOW"]
        self.hum_high = conf["conf"]["HUM_HIGH"]
        self.co2_high = conf["conf"]["CO2_HIGH"]
        self.alert_hum_low = conf["conf"]["ALERT_HUM_LOW"]
        self.alert_hum_high = conf["conf"]["ALERT_HUM_HIGH"]
        self.alert_temp_low = conf["conf"]["ALERT_TEMP_LOW"]
        self.alert_temp_high = conf["conf"]["ALERT_TEMP_HIGH"]
        self.air_minutes = conf["conf"]["AIR_MINUTES"]
        self.input_id = conf["input"]

    def run(self):
        self._ctrl_hum()
        self._ctrl_air()
        self._ctrl_temp()

    def _switch(self, output_id: str, state: bool):
        data = {
            "state": state,  # False = turning power ON
            "channel": 0,
        }
        endpoint = f"outputs/{output_id}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers, verify=False)
        print(response.json())
        return response.status_code

    def _notify(self, installation_id: str, message: str):
        requests.post(
            f"https://api.telegram.org/bot7081645135:AAEljjW626aZ7y70nNJMY54fEkaBOBjld_A/sendMessage?chat_id=-4139438850&text={installation_id}\n{message}"
        )

    def _ctrl_hum(self):
        """
        humidifier power + alerts for humidity level
        """
        input_unit = "percent"
        input_ch = "2"
        endpoint = f"/measurements/last/{self.input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self._notify(self.installation_id, "humidity measurement is offline")
            return None

        cur_minute = datetime.now().minute
        if cur_minute in self.air_minutes:
            self._switch(self.switch2, True)

        if value < self.hum_low:
            self._switch(self.switch3, False)

        if value > self.hum_high:
            self._switch(self.switch3, True)

        if value > self.alert_hum_high or value < self.alert_hum_low:
            self._notify(self.installation_id, f"humidity level: {value} %")
        return None

    def _ctrl_air(self):
        """
        fan power
        """
        input_unit = "ppm"
        input_ch = "0"
        endpoint = f"/measurements/last/{self.input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self._notify(self.installation_id, "CO2 measurement is offline")
            return None

        if value > self.co2_high:
            self._switch(self.switch2, False)
            return None

        cur_minute = datetime.now().minute
        if cur_minute in self.air_minutes:
            self._switch(self.switch2, False)
        else:
            self._switch(self.switch2, True)

        return None

    def _ctrl_temp(self):
        """
        alerts for temperature
        """
        input_unit = "C"
        input_ch = "1"
        endpoint = f"/measurements/last/{self.input_id}/{input_unit}/{input_ch}/{3000}"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.get(url, headers=self.headers, verify=False)
        value = json.loads(response.text)["value"]
        print(value, type(value))

        if value is None:
            self._notify(self.installation_id, "temperature measurement is offline")
            return None

        if value < self.alert_temp_low or value > self.alert_temp_high:
            self._notify(self.installation_id, f"temperature: {value}")
