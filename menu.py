import os 
import json

# Nombre del archivo de persistencia
ARCHIVO_CAMPERS = "campers.json"
# Lista global para guardar campers
campers = []

# ============================== Persistencia =======================================
def guardar_datos():
    """Guarda la lista de campers en el archivo JSON"""
    with open(ARCHIVO_CAMPERS, "w", encoding="utf-8") as f:
        json.dump(campers, f, indent=4, ensure_ascii=False)

def cargar_datos():
    """Carga la lista de campers desde el archivo JSON"""
    global campers
    if os.path.exists(ARCHIVO_CAMPERS):
        with open(ARCHIVO_CAMPERS, "r", encoding="utf-8") as f:
            try:
                campers = json.load(f)
            except json.JSONDecodeError:
                campers = []  # si el archivo está vacío o corrupto
    else:
        campers = []


#=============================== Menus ================================== 
def menu_principal():
    cargar_datos()  # Cargamos los campers al iniciar
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('===== MENU PRINCIPAL =====')
            print('Por favor elige tu categoria: ')
            print('1. 🤖 Camper 🤖 ')
            print('2. ⌨️ Trainer ⌨️ ')
            print('3. 👽 Coordinador 👽')
            print('4. Salir')

            opcion = input('Ingresa un numero (1-4): ')

            if opcion == "1":
                pass
                
            elif opcion == "2":
                print('⌨️ Ingreso Trainer ⌨️')
                ID_trainer = input('Trainer, ingrese su ID: ')
                input("Presiona ENTER para continuar...")

            elif opcion == "3":
                menu_coordinador()

            elif opcion == "4":
                print("👋 Saliendo del programa...")
                break

            else:
                print('❌ Por favor ingrese una opción válida ❌')
                input("Presiona ENTER para continuar...")

        except KeyboardInterrupt:
            print("\nPrograma terminado por el usuario.")
            break

#======================= Menu coordinandor ========================
def menu_coordinador():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('===== 👽 MENU DEL COORDINADOR 👽 =====')
        print('1. Registrar nuevo estudiante')
        print('2. Ver datos de los estudiantes')
        print('3. Volver al menú principal')

        opcion = input('Selecciona una opción (1-3): ')
        
        if opcion == "1":
            registro_estudiante()
        elif opcion == "2":
            ver_estudiantes()
        elif opcion == "3":
            break
        else:
            print("❌ Opción inválida ❌")
            input("Presiona ENTER para continuar...")


def registro_estudiante():
    os.system('cls' if os.name == 'nt' else 'clear')
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
        "estado": "Inscrito",
        "riesgo": "Bajo",
        "ruta": None
    }
    campers.append(camper)
    guardar_datos()  # ✅ Persistimos después de registrar
    print("\n✅ Camper registrado exitosamente ✅")
    input("Presiona ENTER para continuar...")


def ver_estudiantes():
    os.system('cls' if os.name == 'nt' else 'clear')
    if not campers:
        print("⚠️ No hay estudiantes registrados aún.")
    else:
        print("=== Lista de Estudiantes Registrados ===")
        for i, camper in enumerate(campers, 1):
            print(f"{i}. {camper['nombres']} {camper['apellidos']} - ID: {camper['id']} - Estado: {camper['estado']}")
    input("\nPresiona ENTER para continuar...")


# Iniciar el programa
menu_principal()
