from modules.utils import guardar_datos

def registro_estudiante(campers):
    print("=== Registro de nuevo estudiante ===")
    id_camper = input("ID: ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    direccion = input("Dirección: ")
    acudiente = input("Nombre del acudiente: ")
    celular = input("Teléfono celular: ")
    fijo = input("Teléfono fijo: ")

    camper = {
        "id": id_camper,
        "nombres": nombres,
        "apellidos": apellidos,
        "direccion": direccion,
        "acudiente": acudiente,
        "telefonos": {"celular": celular, "fijo": fijo},
        "estado": "proceso de ingreso",
        "riesgo":  None,
        "ruta": None
    }
    campers.append(camper)
    guardar_datos(campers)
    print("\n✅ Camper registrado exitosamente ✅")
    input("Presiona ENTER para continuar...")
    return campers
