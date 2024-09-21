import socket
from usuarios import validacion_planilla

# Configuración del servidor
direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

# Crear el socket del servidor
mi_socket = socket.socket()
mi_socket.bind((direccion_del_Servidor, puerto_Servidor))
mi_socket.listen(5)
print(f"Servidor iniciando sesion con el servidor --> {direccion_del_Servidor} en el puerto -->{puerto_Servidor}")

# Bucle principal para aceptar conexiones
while True:
    # Aceptar una nueva conexión
    conexion, direccion = mi_socket.accept()
    print(f"Inicio de sesion desde el servidor --> {direccion}")

    i = 0  # Para controlar los i de validación
    usuario_valido = False  # Bandera para saber si el usuario es válido

    while i < 3 and not usuario_valido:
        # Recibir el documento del cliente
        documento = conexion.recv(1024).decode('utf-8')
        print(f"Validando la informacion suministrada... El documento {documento} no se encuentra en nuestra base de datos, lo sentimos.")

        # Validar el usuario
        if validacion_planilla(documento):
            usuario_valido = True
            conexion.send(f"Sesión abierta. Ha iniciado sesión el usuario {documento}".encode('utf-8'))
            print(f"Usuario válido: {documento}. Sesión iniciada.")
        else:
            i += 1
            if i < 3:
                conexion.send(f"Documento no válido. Intento {i}/3. Por favor, intente de nuevo.".encode('utf-8'))
            else:
                conexion.send("Ha superado el número máximo de i. Sesión cerrada.".encode('utf-8'))
                print(f"El cliente {direccion} ha superado los i permitidos. Conexión cerrada.")
                conexion.close()
                break

    # Si el usuario es válido, mantener la sesión activa
    if usuario_valido:
        while True:
            mensaje = conexion.recv(1024).decode('utf-8')
            if not mensaje or mensaje.lower() == "salir":
                conexion.send("Sesión cerrada. Adiós.".encode('utf-8'))
                print(f"El cliente {direccion} ha cerrado la sesión.")
                break
            else:
                # Responder al cliente con eco
                conexion.send(f"Echo: {mensaje}".encode('utf-8'))
                print(f"Mensaje recibido de {direccion}: {mensaje}")

    # Cerrar la conexión con el cliente
    conexion.close()
