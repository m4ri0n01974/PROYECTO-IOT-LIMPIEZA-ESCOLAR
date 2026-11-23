import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "telemetria.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/api/telemetria", methods=["POST"])
def post_telemetria():
    d = request.get_json(force=True)
    distancia = int(d.get("distancia_cm", 0))
    bateria = int(d.get("bateria_pct", 100))
    seguridad = str(d.get("estado_seguridad", "SEGURO")).upper()
    alerta = str(d.get("alerta_preventiva", "NINGUNA")).upper()
    cofre = str(d.get("estado_cofre", "DISPONIBLE")).upper()

    # Transformación preventiva (riesgo / prevención de incidentes)
    if seguridad == "ALERTA_COLISION" or bateria <= 20:
        riesgo = "ALTO"
    elif seguridad == "PRECAUCION" or bateria <= 50 or cofre == "CASI_LLENO":
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    item = {
        "timestamp": datetime.now().isoformat(),
        "distancia_cm": distancia,
        "bateria_pct": bateria,
        "estado_seguridad": seguridad,
        "alerta_preventiva": alerta,
        "estado_cofre": cofre,
        "nivel_riesgo": riesgo
    }

    data = load_data()
    data.append(item)
    save_data(data)
    return jsonify({"ok": True, "registro": item}), 201

@app.route("/api/telemetria", methods=["GET"])
def get_telemetria():
    data = load_data()
    return jsonify({"ultimo": data[-1] if data else None, "total": len(data), "registros": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)