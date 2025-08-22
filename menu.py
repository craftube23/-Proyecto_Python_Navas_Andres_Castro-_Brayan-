import os 
def menu_principal():
    while True:
        try:
            os.system('cls' if os.name == 'nt'else 'clear')
            print(' Menu ')
            print('Porfavor elige tu categoria: ')
            print('1. 🤖 Camper 🤖 ')
            print('2. ⌨️  Trainer ⌨️ ')
            print('3. 👽 Coordinador 👽')
        
            

            opcion= input('Ingresa un numero (1-3): ')

            if opcion == "1":
                while True:
                    print()
                    print(' 🤖 Ingreso Camper 🤖 ')
                    ID_camper= input(' Camper Ingrese su ID: ')
                    

                    break

            elif opcion == "2":
                while True:
                    print()
                    print(' ⌨️ Ingreso Trainer ⌨️ ')
                    ID_trainer= input(' Trainer Ingrese su ID: ')

                    break

            elif opcion == "3":
                while True:
                    menu_cordinador()
                                ##print()## 
                                ##print(' 👽 Ingreso Coordinador ')##
                                ##ID_coordinador= input(' Coordinador Ingrese su ID: ')##

                    break

            else:
                while True:
                    opcion == print('❌ Porfavor ingrese una opcion valida ❌')
                    print()

                    break

def menu_cordinador():
    print ('MENU DEL CORDINADOR ')
    print ('1. registra nuevo estudiante ')
    print ('2. datos de los estudiante ')
    print ('3. salir')

    opcion = input ('seleciona una de las 3 opciones ')
    if opcion == "1":
         pass
    else:
        pass







menu_principal
