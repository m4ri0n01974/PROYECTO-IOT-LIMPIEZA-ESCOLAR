import json
import requests

URL = "http://127.0.0.1:5000/api/telemetria"

muestras = [
    {"distancia_cm": 45, "bateria_pct": 88, "estado_seguridad": "SEGURO", "alerta_preventiva": "NINGUNA", "estado_cofre": "DISPONIBLE"},
    {"distancia_cm": 26, "bateria_pct": 42, "estado_seguridad": "PRECAUCION", "alerta_preventiva": "BAT_MEDIA_Y_PROXIMIDAD", "estado_cofre": "MEDIO"},
    {"distancia_cm": 11, "bateria_pct": 16, "estado_seguridad": "ALERTA_COLISION", "alerta_preventiva": "BAT_BAJA_Y_FRENO", "estado_cofre": "CASI_LLENO"}
]

# Enviar al servidor API REST
for m in muestras:
    r = requests.post(URL, json=m, timeout=5)
    print("POST:", r.status_code, r.json().get("registro", {}).get("nivel_riesgo"))

# ETL: Extract -> Transform -> Load
crudos = requests.get(URL, timeout=5).json().get("registros", [])
transformados = [
    {
        "timestamp": x["timestamp"],
        "distancia_cm": x["distancia_cm"],
        "bateria_pct": x["bateria_pct"],
        "nivel_riesgo": x["nivel_riesgo"],
        "alerta_preventiva": x["alerta_preventiva"],
        "estado_cofre": x["estado_cofre"]
    }
    for x in crudos
]

with open("etl_salida.json", "w", encoding="utf-8") as f:
    json.dump(transformados, f, indent=2, ensure_ascii=False)

print("ETL listo. Total:", len(transformados))