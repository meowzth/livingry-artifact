from pizdec import Pizdec

CONFIG = {
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


Pizdec(conf=CONFIG).run()
