import os
import json

# =========================================================
#                 PERSISTENCIA 
# =========================================================
FILE = "data/campers.json"

# Estructura por defecto del "DB"
DEFAULT_DB = {
    "campers": [],
    "trainers": [],
    "rutas": [
        {
            "nombre": "NodeJS",
            "capacidad": 33,     # capacidad concurrente (simple)
            "modulos": [
                "Fundamentos de programación",
                "Programación Web",
                "Programación formal",
                "Bases de datos",
                "Backend"
            ]
        },
        {
            "nombre": "Java",
            "capacidad": 33,
            "modulos": [
                "Fundamentos de programación",
                "Programación Web",
                "Programación formal",
                "Bases de datos",
                "Backend"
            ]
        },
        {
            "nombre": "NetCore",
            "capacidad": 33,
            "modulos": [
                "Fundamentos de programación",
                "Programación Web",
                "Programación formal",
                "Bases de datos",
                "Backend"
            ]
        }
    ]
}

DB = DEFAULT_DB.copy()

def cargar_db():
    global DB
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Compatibilidad: si era lista de campers antes
                if isinstance(data, list):
                    DB = DEFAULT_DB.copy()
                    DB["campers"] = data
                elif isinstance(data, dict):
                    # mezclar con defaults por si faltan llaves
                    DB = DEFAULT_DB.copy()
                    DB.update({k: v for k, v in data.items() if k in DEFAULT_DB})
                else:
                    DB = DEFAULT_DB.copy()
            except json.JSONDecodeError:
                DB = DEFAULT_DB.copy()
    else:
        DB = DEFAULT_DB.copy()

def guardar_db():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(DB, f, indent=4, ensure_ascii=False)

# Helpers cortos
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPresiona ENTER para continuar...")

# =========================================================
#                LÓGICA COMÚN / UTILIDADES
# =========================================================
def buscar_camper_por_id(cid):
    for c in DB["campers"]:
        if c["id"] == cid:
            return c
    return None

def buscar_trainer_por_id(tid):
    for t in DB["trainers"]:
        if t["id"] == tid:
            return t
    return None

def listar_rutas():
    for i, r in enumerate(DB["rutas"], start=1):
        print(f"{i}. {r['nombre']} (capacidad {r['capacidad']})")

def seleccionar_ruta_por_indice():
    try:
        idx = int(input("Seleccione una ruta (número): "))
        if 1 <= idx <= len(DB["rutas"]):
            return DB["rutas"][idx - 1]
    except ValueError:
        pass
    print("❌ Selección inválida.")
    return None

def calcular_nota_final(teoria, practica, quices):
    # 30% teoría, 60% práctica, 10% quices
    return teoria * 0.3 + practica * 0.6 + quices * 0.1

def set_riesgo_desde_nota(camper, nota_final):
    # Si nota < 60, riesgo alto; si entre 60 y 75 medio; si >= 75 bajo
    if nota_final < 60:
        camper["riesgo"] = "Alto"
    elif nota_final < 75:
        camper["riesgo"] = "Medio"
    else:
        camper["riesgo"] = "Bajo"

def campers_en_ruta(nombre_ruta, estados=None):
    estados = estados or []
    return [
        c for c in DB["campers"]
        if c.get("ruta") == nombre_ruta and (not estados or c.get("estado") in estados)
    ]

# =========================================================
#                 CAMPPER (rol y funciones)
# =========================================================
def registrar_camper():
    clear()
    print("===== Registro de Camper =====")
    camper = {
        "id": int(input("Identificación: ").strip()),
        "nombres": str(input("Nombres: ")).capitalize().strip(),
        "apellidos": str(input("Apellidos: ")).capitalize().strip(),
        "direccion": input("Dirección: ").strip(),
        "acudiente": str(input("Acudiente: ")).capitalize().strip(),
        "telefonos": {
            "celular": int(input("Teléfono celular: ").strip()),
            "fijo": int(input("Teléfono fijo: ").strip())
        },
        "estado": "proceso de ingreso ",            # alineado con enunciado
        "riesgo": None,
        "ruta": None,                    # se asigna tras aprobar
        "notas": [],                     # histórico de pruebas iniciales u otras
        "modulos": {}                    # notas por módulo (llenado por Trainer)
    }
    # Evitar duplicados
    if buscar_camper_por_id(camper["id"]):
        print("❌ Ya existe un camper con ese ID.")
    else:
        DB["campers"].append(camper)
        guardar_db()
        print("✅ Camper registrado exitosamente.")
    pause()

def ver_campers():
    clear()
    print("===== Lista de Campers =====")
    if not DB["campers"]:
        print("No hay campers registrados.")
    else:
        for c in DB["campers"]:
            print(f"{c['id']} - {c['nombres']} {c['apellidos']} | Estado: {c['estado']} | Ruta: {c['ruta']} | Riesgo: {c['riesgo']}")
    pause()

def menu_camper():
    while True:
        clear()
        print("===== Menú Camper =====")
        print("1. Registrarse")
        print("2. Ver lista de campers")
        print("3. Volver al menú principal")
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            registrar_camper()
        elif op == "2":
            ver_campers()
        elif op == "3":
            break

# =========================================================
#                 COORDINADOR (rol y funciones)
# =========================================================
def editar_camper_coordinador():
    ver_campers()
    cid = int(input("Ingrese el ID del camper a editar: ").strip())

    c = buscar_camper_por_id(cid)
    if not c:
        print("⚠️ Camper no encontrado.")
        pause(); return

    clear()
    print("=== Edición de Camper ===")
    print("Deja vacío si no deseas cambiar un campo.\n")

    c["nombres"] = str(input(f"Nombres ({c['nombres']}): ").strip() or c["nombres"])
    c["apellidos"] = str(input(f"Apellidos ({c['apellidos']}): ").strip() or c["apellidos"])
    c["direccion"] = input(f"Dirección ({c['direccion']}): ").strip() or c["direccion"]
    c["acudiente"] = str(input(f"Acudiente ({c['acudiente']}): ").strip() or c["acudiente"])
    c["telefonos"]["celular"] = int(input(f"Celular ({c['telefonos']['celular']}): ".strip()) or c["telefonos"]["celular"])
    c["telefonos"]["fijo"] = int(input(f"Fijo ({c['telefonos']['fijo']}): ".strip()) or c["telefonos"]["fijo"])

    # Cambio de estado manual opcional
    est = input(f"Estado actual ({c['estado']}) [Enter para no cambiar]: ").strip()
    if est:
        c["estado"] = est

    guardar_db()
    print("✅ Información actualizada.")
    pause()

def registrar_prueba_inicial():
    # Coordinador registra nota teórica/práctica de examen inicial
    ver_campers()
    cid = int(input("Ingrese el ID del camper a calificar (prueba inicial): ").strip())

    c = buscar_camper_por_id(cid)
    if not c:
        print("⚠️ Camper no encontrado.")
        pause(); return

    try:
        teoria = float(input("Nota teórica (0-100) [30%]: "))
        practica = float(input("Nota práctica (0-100) [60%]: "))
        quiz_trabajos = float(input("Quices/trabajos (0-100) [10%]: "))
    except ValueError:
        print("❌ Valores inválidos.")
        pause(); return

    final = calcular_nota_final(teoria, practica, quiz_trabajos)
    c["notas"].append({
        "tipo": "prueba_inicial",
        "teoria": teoria, "practica": practica, "quices": quiz_trabajos,
        "final": final
    })
    # Si final >= 60 → Aprobado; si no, queda en "Inscrito" o "Rechazado"
    if final >= 60:
        c["estado"] = "Aprobado"
    else:
        c["estado"] = "Inscrito"  # puedes optar por "Rechazado" si lo deseas
    set_riesgo_desde_nota(c, final)

    guardar_db()
    print(f"✅ Nota registrada. Final: {final:.2f} | Estado: {c['estado']} | Riesgo: {c['riesgo']}")
    pause()

def asignar_ruta_coordinador():
    clear()
    print("===== Asignar Ruta a Camper =====")
    cid = int(input("ID del camper Aprobado para asignar ruta: ").strip())
    camper = buscar_camper_por_id(cid)

    if not camper:
        print("❌ Camper no encontrado.")
        return pause()

    if camper["estado"] != "Aprobado":
        print("❌ El camper no está en estado 'Aprobado'.")
        return pause()

    # Mostrar rutas disponibles
    print("\nRutas disponibles:")
    for i, ruta in enumerate(DB["rutas"], start=1):
        print(f"{i}. {ruta['nombre']} (Cupos: {ruta['capacidad']})")

    try:
        opcion = int(input("Seleccione la ruta: "))
        ruta = DB["rutas"][opcion - 1]
    except (ValueError, IndexError):
        print("❌ Opción inválida.")
        return pause()

    # Verificar capacidad
    if ruta["capacidad"] <= 0:
        print(f"❌ La ruta {ruta['nombre']} ya está llena. Intente con otra.")
        return pause()

    # Asignar camper a la ruta
    camper["ruta"] = ruta["nombre"]
    camper["estado"] = "Cursando"
    ruta["capacidad"] -= 1  # Restar cupo
    guardar_db()

    print(f"✅ Camper {camper['nombres']} asignado a la ruta {ruta['nombre']}.")
    print(f"📉 Cupos restantes: {ruta['capacidad']}")
    pause()


def reportes():
    clear()
    print("===== Reportes =====")
    print("1. Campers en estado 'Inscrito'")
    print("2. Campers 'Aprobado'")
    print("3. Campers con 'Riesgo Alto'")
    print("4. Campers por ruta")
    print("5. Volver")
    op = input("Seleccione: ").strip()

    if op == "1":
        for c in DB["campers"]:
            if c["estado"] == "Inscrito":
                print(f"{c['id']} - {c['nombres']} {c['apellidos']}")
        pause()
    elif op == "2":
        for c in DB["campers"]:
            if c["estado"] == "Aprobado":
                print(f"{c['id']} - {c['nombres']} {c['apellidos']}")
        pause()
    elif op == "3":
        for c in DB["campers"]:
            if c.get("riesgo") == "Alto":
                print(f"{c['id']} - {c['nombres']} {c['apellidos']} | Ruta: {c['ruta']}")
        pause()
    elif op == "4":
        for r in DB["rutas"]:
            print(f"\nRuta: {r['nombre']}")
            grupo = [c for c in DB["campers"] if c.get("ruta") == r["nombre"]]
            if not grupo:
                print("  (sin campers)")
            for c in grupo:
                print(f"  - {c['id']} {c['nombres']} {c['apellidos']} | Estado: {c['estado']}")
        pause()

def menu_coordinador():
    while True:
        clear()
        print("===== Menú Coordinador =====")
        print("1. Editar camper")
        print("2. Registrar prueba inicial (cambia estado a Aprobado si ≥ 60)")
        print("3. Asignar ruta (solo Aprobados)")
        print("4. Reportes")
        print("5. Volver")
        op = input("Seleccione: ").strip()
        if op == "1":
            editar_camper_coordinador()
        elif op == "2":
            registrar_prueba_inicial()
        elif op == "3":
            asignar_ruta_coordinador()
        elif op == "4":
            reportes()
        elif op == "5":
            break

# =========================================================
#                   TRAINER (rol y funciones)
# =========================================================
def registrar_trainer():
    clear()
    print("===== Registrar Trainer =====")
    trainer = {
        "id": int(input("ID del trainer: ").strip()),
        "nombre": str(input("Nombre completo: ")).capitalize().strip(),
        "rutas_asignadas": [],   # nombres de rutas
        "horario": input("Horario (texto libre): ").strip()
    }
    if buscar_trainer_por_id(trainer["id"]):
        print("❌ Ya existe un trainer con ese ID.")
    else:
        DB["trainers"].append(trainer)
        guardar_db()
        print("✅ Trainer registrado.")
    pause()

def listar_trainers():
    clear()
    print("===== Trainers =====")
    if not DB["trainers"]:
        print("(sin trainers)")
    else:
        for t in DB["trainers"]:
            rutas = ", ".join(t["rutas_asignadas"]) if t["rutas_asignadas"] else "—"
            print(f"{t['id']} - {t['nombre']} | Rutas: {rutas} | Horario: {t['horario']}")
    pause()

def asignar_ruta_a_trainer():
    listar_trainers()
    tid = input("ID del trainer a asignar ruta: ").strip()
    t = buscar_trainer_por_id(tid)
    if not t:
        print("⚠️ Trainer no encontrado.")
        pause(); return

    clear()
    print("Rutas disponibles:")
    listar_rutas()
    ruta = seleccionar_ruta_por_indice()
    if not ruta:
        pause(); return

    if ruta["nombre"] in t["rutas_asignadas"]:
        print("⚠️ Esa ruta ya está asignada a este trainer.")
    else:
        t["rutas_asignadas"].append(ruta["nombre"])
        guardar_db()
        print(f"✅ Ruta '{ruta['nombre']}' asignada a {t['nombre']}.")
    pause()

def campers_de_mis_rutas(t):
    # Campers cursando una de las rutas del trainer
    lista = [c for c in DB["campers"] if c.get("ruta") in t["rutas_asignadas"]]
    return lista

def ver_mis_campers():
    listar_trainers()
    tid = input("ID del trainer: ").strip()
    t = buscar_trainer_por_id(tid)
    if not t:
        print("⚠️ Trainer no encontrado.")
        pause(); return
    clear()
    print(f"===== Campers de {t['nombre']} =====")
    lista = campers_de_mis_rutas(t)
    if not lista:
        print("(sin campers en tus rutas)")
    else:
        for c in lista:
            print(f"{c['id']} - {c['nombres']} {c['apellidos']} | Ruta: {c['ruta']} | Estado: {c['estado']}")
    pause()

def registrar_nota_modulo_trainer():
    # Trainer califica un módulo de un camper de sus rutas
    listar_trainers()
    tid = input("Tu ID de trainer: ").strip()
    t = buscar_trainer_por_id(tid)
    if not t:
        print("⚠️ Trainer no encontrado.")
        pause(); return

    lista = campers_de_mis_rutas(t)
    if not lista:
        print("No tienes campers en tus rutas.")
        pause(); return

    clear()
    print("===== Campers que puedes calificar =====")
    for c in lista:
        print(f"{c['id']} - {c['nombres']} {c['apellidos']} | Ruta: {c['ruta']}")

    cid = input("ID del camper a calificar: ").strip()
    c = buscar_camper_por_id(cid)
    if not c or c not in lista:
        print("❌ No puedes calificar a este camper (no está en tus rutas).")
        pause(); return

    # Seleccionar módulo según la ruta
    ruta_name = c.get("ruta")
    ruta = next((r for r in DB["rutas"] if r["nombre"] == ruta_name), None)
    if not ruta:
        print("❌ La ruta del camper no existe.")
        pause(); return

    print("\nMódulos de la ruta:")
    for i, m in enumerate(ruta["modulos"], start=1):
        print(f"{i}. {m}")
    try:
        idx = int(input("Seleccione módulo: "))
        if not (1 <= idx <= len(ruta["modulos"])):
            raise ValueError()
    except ValueError:
        print("❌ Selección inválida.")
        pause(); return
    modulo = ruta["modulos"][idx - 1]

    # Ingreso de notas
    try:
        teoria = float(input("Nota teórica (0-100) [30%]: "))
        practica = float(input("Nota práctica (0-100) [60%]: "))
        quices  = float(input("Quices/trabajos (0-100) [10%]: "))
    except ValueError:
        print("❌ Valores inválidos.")
        pause(); return

    final = calcular_nota_final(teoria, practica, quices)
    aprobado = final >= 60

    if "modulos" not in c or not isinstance(c["modulos"], dict):
        c["modulos"] = {}

    c["modulos"][modulo] = {
        "teoria": teoria,
        "practica": practica,
        "quices": quices,
        "final": final,
        "aprobado": aprobado
    }

    # Ajustar riesgo general del camper con esta nueva nota
    set_riesgo_desde_nota(c, final)

    # Si aprobó todos los módulos de la ruta → podría pasar a Graduado
    todos = c["modulos"]
    mod_names = ruta["modulos"]
    if all(m in todos and todos[m].get("aprobado") for m in mod_names):
        c["estado"] = "Graduado"
    else:
        # Si reprobó este módulo, mantener Cursando pero riesgo podría ser alto
        if not aprobado:
            # Puedes poner lógica adicional (llamado de atención, etc.)
            pass

    guardar_db()
    print(f"✅ Nota registrada para '{modulo}'. Final: {final:.2f} | {'Aprobado' if aprobado else 'Reprobado'}")
    print(f"Estado actual del camper: {c['estado']} | Riesgo: {c['riesgo']}")
    pause()

def menu_trainer():
    while True:
        clear()
        print("===== Menú Trainer =====")
        print("1. Registrar trainer")
        print("2. Ver trainers")
        print("3. Asignar ruta a trainer")
        print("4. Ver mis campers (por rutas asignadas)")
        print("5. Registrar nota de módulo a un camper")
        print("6. Volver")
        op = input("Seleccione: ").strip()
        if op == "1":
            registrar_trainer()
        elif op == "2":
            listar_trainers()
        elif op == "3":
            asignar_ruta_a_trainer()
        elif op == "4":
            ver_mis_campers()
        elif op == "5":
            registrar_nota_modulo_trainer()
        elif op == "6":
            break

# =========================================================
#                   MENÚ PRINCIPAL
# =========================================================
def menu_principal():
    cargar_db()
    while True:
        clear()
        print("===== CampusLands ERP =====")
        print("1. Camper")
        print("2. Trainer")
        print("3. Coordinador")
        print("4. Salir")
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            menu_camper()
        elif op == "2":
            menu_trainer()
        elif op == "3":
            menu_coordinador()
        elif op == "4":
            print("👋 Saliendo del sistema...")
            break

if __name__ == "__main__":
    menu_principal()