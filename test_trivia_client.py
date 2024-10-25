# Importa las funciones  del users
from users import registerUser, openCloseSession, updateScore, getScore, usersList, question

def main():
    # Inicializa las variables para el usuario actual y la contraseña
    current_user, current_password = None, None

    while True:
        # Menú principal para opciones de usuario
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        # Solicita al usuario seleccionar una opción
        option = input("Selecciona una opción: ")

        if option == "1":
            # Opción para registrar un nuevo usuario
            name = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contraseña: ")
            print(registerUser(name, password))  # Llama a la función para registrar el usuario

        elif option == "2":
            # Opción para iniciar sesión
            name = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contraseña: ")
            session_result = openCloseSession(name, password, True)  # Intenta abrir sesión

            print(f"Resultado de sesión: {session_result}")  

            if session_result == "sesión iniciada":
                # Si la sesión se inicia correctamente
                current_user, current_password = name, password
                print(f"\n¡Bienvenido, {name}! {session_result}")

                while True:
                    # Menú de opciones para el usuario conectado
                    print("\nOpciones disponibles:")
                    print("1. Actualizar puntaje")
                    print("2. Ver puntaje actual")
                    print("3. Ver usuarios conectados")
                    print("4. Obtener pregunta aleatoria")
                    print("5. Cerrar sesión")
                    print("6. Volver al menú principal")

                    # Solicita al usuario seleccionar una opción
                    logged_option = input("Selecciona una opción: ")

                    if logged_option == "1":
                        # Opción para actualizar el puntaje del usuario
                        try:
                            new_score = int(input("Introduce el nuevo puntaje: "))  # Solicita el nuevo puntaje
                            print(updateScore(current_user, current_password, new_score))  # Actualiza el puntaje
                        except ValueError:
                            print("Por favor, introduce un número válido para el puntaje.")

                    elif logged_option == "2":
                        # Opción para ver el puntaje actual del usuario
                        print("Tu puntaje es:", getScore(current_user, current_password))

                    elif logged_option == "3":
                        # Opción para ver la lista de usuarios conectados
                        print(usersList())  

                    elif logged_option == '4':
                        # Opción para obtener una pregunta aleatoria
                        question()  

                    elif logged_option == "5":
                        # Opción para cerrar sesión
                        print(openCloseSession(current_user, current_password, False))  # Cierra sesión
                        current_user, current_password = None, None  # Reinicia las variables de usuario
                        break  

                    elif logged_option == "6":
                        # Opción para volver al menú principal
                        break  

                    else:
                        print("Opción inválida. Inténtalo de nuevo.")

                    # Pregunta al usuario si desea volver al menú principal
                    continue_choice = input("¿Quieres volver al menú principal? (si/no): ").strip().lower()
                    if continue_choice == "no":
                        print("Saliendo del juego...")
                        return  # Sale del programa 

            else:
                # Si no se pudo iniciar sesión, muestra el mensaje de error
                print(session_result)

        elif option == "3":
            # Opción para salir del programa
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()
