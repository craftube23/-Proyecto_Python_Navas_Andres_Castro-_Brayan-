import json, os

ARCHIVO_CAMPERS = "data/campers.json"

def guardar_datos(campers):
    with open(ARCHIVO_CAMPERS, "w", encoding="utf-8") as f:
        json.dump(campers, f, indent=4, ensure_ascii=False)

def cargar_datos():
    if os.path.exists(ARCHIVO_CAMPERS):
        with open(ARCHIVO_CAMPERS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
