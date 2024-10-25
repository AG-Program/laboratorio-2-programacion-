import random

# Diccionario para almacenar usuarios conectados
connected_users = {}

# Función para registrar un nuevo usuario
def registerUser(name, password):
    name = name.strip().lower() 
    password = password.strip()    

    # Intenta abrir el archivo de usuarios para verificar si el usuario ya está registrado
    try:
        file = open("usuarios.txt", "r")
        for line in file:
            # Verifica si el usuario ya está registrado
            if line.strip() and line.split(",")[0].strip().lower() == name:
                file.close()
                return "ya registrado"  # Usuario ya registrado
        file.close()
    except FileNotFoundError:
        # Si el archivo no existe, lo crea
        open("usuarios.txt", "w").close()

    # Agrega el nuevo usuario al archivo
    file = open("usuarios.txt", "a")
    file.write(f"{name},{password},0,no_conectado\n")  # Guarda el nombre, contraseña, puntaje inicial y estado
    file.close()
    return "registrado"  # Confirma el registro

# Función para abrir o cerrar sesión de un usuario
def openCloseSession(name, password, flag):
    name = name.strip().lower()  # Normaliza el nombre
    password = password.strip()    # Elimina espacios en blanco
    lines, user_found = [], False  

    # Lee el archivo de usuarios
    file = open("usuarios.txt", "r")
    for line in file:
        if line.strip():
            user, passw, user_score, status = line.split(",")
            # Verifica las credenciales del usuario
            if user == name and passw == password:
                user_found = True
                status = "conectado" if flag else "desconectado"  # Cambia el estado según el flag
            lines.append(f"{user},{passw},{user_score},{status}")  # Guarda el estado actual
    file.close()

    if user_found:
        # Escribe las líneas de vuelta en el archivo con el estado actualizado
        file = open("usuarios.txt", "w")
        file.write("\n".join(lines) + "\n")
        file.close()
        return "sesión iniciada" if flag else "sesión cerrada"  # Devuelve el estado de la sesión

    return "error"  # Si no se encuentra al usuario

# Función para actualizar el puntaje de un usuario
def updateScore(name, password, new_score):
    name = name.strip().lower()  # Normaliza el nombre
    password = password.strip()    # Elimina espacios en blanco
    lines, updated = [], False  # Inicializa las variables

    # Lee el archivo de usuarios
    file = open("usuarios.txt", "r")
    for line in file:
        if line.strip():
            user, passw, user_score, status = line.split(",")
            # Verifica las credenciales del usuario
            if user == name and passw == password:
                user_score = new_score  # Actualiza el puntaje
                updated = True
            lines.append(f"{user},{passw},{user_score},{status}")  # Guarda la línea con el estado actual
    file.close()

    if updated:
        # Escribe las líneas de vuelta en el archivo con el puntaje actualizado
        file = open("usuarios.txt", "w")
        file.write("\n".join(lines) + "\n")
        file.close()
        return "actualizado"  # Confirma la actualización

    return "error de usuario o contraseña"  # Si no se encuentra el usuario o la contraseña es incorrecta

# Función para obtener el puntaje de un usuario
def getScore(name, password):
    name = name.strip().lower()  # Normaliza el nombre
    password = password.strip()    # Elimina espacios en blanco

    # Lee el archivo de usuarios
    file = open("usuarios.txt", "r")
    for line in file:
        if line.strip():
            user, passw, user_score, status = line.split(",")
            # Verifica las credenciales del usuario
            if user == name and passw == password:
                file.close()
                return user_score  # Devuelve el puntaje del usuario
    file.close()
    return "error de usuario o contraseña"  # Si no se encuentra el usuario o la contraseña es incorrecta

# Función para obtener la lista de usuarios conectados
def usersList():
    connected_users = []  # Inicia la lista de usuarios conectados

    try:
        # Lee el archivo de usuarios
        file = open("usuarios.txt", "r")
        for line in file:
            if line.strip():
                parts = line.split(",")
                # Verifica si el estado es 'conectado'
                if len(parts) >= 4 and parts[3].strip().lower() == "conectado":
                    connected_users.append(parts[0].strip())  # Agrega el usuario a la lista
        file.close()
    except FileNotFoundError:
        return "usuario no registrado"  # Si el archivo no existe

    # Devuelve la lista de usuarios conectados
    return f"Usuarios conectados: {', '.join(connected_users)}" if connected_users else "No hay usuarios conectados."

# Función para manejar las preguntas del servidor 
def question():
    total_points = 0  # Inicia contador puntos 
    asked_questions, user_answers = [], []  # Inicializa las listas
    question_list = []  # Lista para almacenar preguntas

    # Carga preguntas de dos archivos de categorías
    for selected_file in ["preguntas_categoria_1.txt", "preguntas_categoria_2.txt"]:
        try:
            file = open(selected_file, "r", encoding="utf-8")
            question_buffer = []  #almacenar preguntas temporales
            for line in file:
                line = line.strip()
                if line:
                    question_buffer.append(line)
                else:
                    # Procesa las preguntas cuando encuentra una línea vacía
                    question_text = question_buffer[0]
                    options = question_buffer[1:5]  # Obtiene las opciones
                    correct_answer = question_buffer[-1].split(":")[1].strip()  # Obtiene la respuesta correcta
                    question_list.append({"question": question_text, "options": options, "answer": correct_answer})
                    question_buffer = []  
            file.close()
        except FileNotFoundError:
            print(f"Error: El archivo {selected_file} no existe.")
            return 0  # Si no se encuentra el archivo, termina la función

    if not question_list:
        print("No se encontraron preguntas en los archivos.")
        return 0  # Si no hay preguntas, termina la función

    # Bucle para hacer preguntas hasta que no queden
    while question_list:
        question_data = random.choice(question_list)  # Selecciona una pregunta al azar
        print(f"\nPregunta: {question_data['question']}")
        for option in question_data['options']:
            print(option)  # Muestra las opciones

        user_answer = input("Escribe tu respuesta (A, B, C o D): ").strip().upper()
        # Valida la respuesta del usuario
        while user_answer not in ['A', 'B', 'C', 'D']:
            print("Por favor, ingresa una opción válida (A, B, C o D).")
            user_answer = input("Escribe tu respuesta (A, B, C o D): ").strip().upper()

        asked_questions.append(question_data['question'])  # Agrega la pregunta a las ya preguntadas
        user_answers.append(user_answer)  # Agrega la respuesta del usuario

        # Verifica si la respuesta es correcta
        if user_answer == question_data['answer']:
            total_points += 1  # Incrementa el puntaje
            print("¡Correcto!")
        else:
            print("Incorrecto.")

        question_list.remove(question_data)  # Elimina la pregunta de la lista

        # Pregunta si desea continuar
        if input("¿Quieres continuar? (si/no): ").strip().lower() != 'si':
            break

    total_questions = len(asked_questions)  # Total de preguntas realizadas
    correct_answers = total_points  # Total de respuestas correctas
    incorrect_answers = total_questions - correct_answers  # Total de respuestas incorrectas

    # Muestra los resultados finales
    print("\nFin del juego.")
    print(f"Tu puntaje total es: {total_points}")
    print(f"Preguntas correctas: {correct_answers}")
    print(f"Preguntas incorrectas: {incorrect_answers}")

    return total_points  # Devuelve el puntaje total
