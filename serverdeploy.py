import socket
from usuarios import validacion_planilla

# variables para direccionamiento del servidor
direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

# uso de socket: Objeto mi_socket y metodos bind (para usar el metodo de conexion) y socket.listen para la cantidad de intentos de conexion
mi_socket = socket.socket()
mi_socket.bind((direccion_del_Servidor, puerto_Servidor))
mi_socket.listen(5)
print(f"Servidor iniciando sesión en --> {direccion_del_Servidor} en el puerto --> {puerto_Servidor}")

# While que permite hacer el bucle que valida las conexiones
while True:
    conexion, direccion = mi_socket.accept()
    print(f"Inicio de sesión desde el servidor --> {direccion}")

    i = 0  # Para controlar los intentos de validación
    usuario_valido = False  # Uso de bandera para saber si el usuario es válido

    while i < 3 and not usuario_valido:
        # recepcion de datos del cliente
        documento = conexion.recv(1024).decode('utf-8')
        print(f"Validando la información suministrada... El documento '{documento}' lo estamos verificando en nuestra base de datos.")

        # Validacion del usuario en la dbplanilla.py
        nombre_usuario = validacion_planilla(documento)
        if nombre_usuario:  # Cambiado de booleano a nombre de usuario
            usuario_valido = True
            conexion.send(f"Sesión abierta. Ahora puedes salir.".encode('utf-8'))
            print(f"Usuario válido: {nombre_usuario}. Sesión iniciada.")
        else:
            i += 1
            if i < 3: # conteo regresivo de los intentos, al tercer intento se cierra la conexión
                conexion.send(f"Documento no válido. Intento {i}/3. Por favor, intente de nuevo.".encode('utf-8'))
            else:
                conexion.send("Ha superado el número máximo de intentos. Sesión cerrada.".encode('utf-8'))
                print(f"El cliente {direccion} ha superado los intentos permitidos. Conexión cerrada.")
                conexion.close()
                break

    # Si el usuario es válidado, la conexion se mantiene hasta que el usuario escriba salir
    if usuario_valido:
        while True:
            mensaje = conexion.recv(1024).decode('utf-8')
            if not mensaje or mensaje.lower() == "salir":
                conexion.send("Sesión cerrada. Adiós.".encode('utf-8'))
                print(f"El cliente {direccion} ha cerrado la sesión.")
                break
            else:
                conexion.send(f"{mensaje}".encode('utf-8'))
                print(f"Mensaje recibido de {direccion}: {mensaje}")

    # cierre de la conexion
    conexion.close()
