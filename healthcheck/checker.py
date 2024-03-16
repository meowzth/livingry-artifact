import requests


class Checker:
    def __init__(
        self,
    ):
        self.ip = "192.168.1.70"
        self.api_key = "TAW4NdoM1J79P22r9tfPkspouUaS/jLo3/SUYQ9pvnDQtongYMbMmJuj86JCOpk0hjVH0UhIEGQmECPo4KxytvAYNeq7dBNy91Q3BLkPlZ0XlDj/yilb7znLlYfkiAWsJDJndzUgy+VoxwGJxgTUn3WoU386yBAZTeYcg7rrcHE="
        self.headers = {
            "Accept": "application/vnd.mycodo.v1+json",
            "X-API-KEY": self.api_key,
        }

    def _notify(self, text: str):
        requests.post(
            f"https://api.telegram.org/bot7081645135:AAEljjW626aZ7y70nNJMY54fEkaBOBjld_A/sendMessage?chat_id=-4139438850&text={text}"
        )

    def check(self):
        input_id = "cb7c9727-15ec-464f-be9c-a06d5e7d1ea0"
        endpoint = f"inputs/{input_id}/force-measurement"
        url = f"https://{self.ip}/api/{endpoint}"
        response = requests.post(url=url, headers=self.headers, verify=False)
        if response.status_code != 200:
            self._notify(
                f"Input {input_id} is offline. API status code: {response.status_code}"
            )


Checker().check()
