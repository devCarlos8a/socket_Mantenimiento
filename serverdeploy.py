import socket
import threading
from usuarios import validacion_planilla

# variables para direccionamiento del servidor
direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

# uso de socket: Objeto mi_socket y metodos bind (para usar el metodo de conexion) y socket.listen para la cantidad de tiempo de espera de la conexion
mi_socket = socket.socket()
mi_socket.bind((direccion_del_Servidor, puerto_Servidor))
mi_socket.listen(5)
print(f"Servidor iniciado en {direccion_del_Servidor}:{puerto_Servidor}")

#conteo de clientes
clientes_activos = 0
lock = threading.Lock()

# implementación de hilos para permitir conexión de varios clientes al tiempo
def manejar_cliente(conexion, direccion):
    global clientes_activos
    print(f"Cliente conectado desde {direccion}")

    # Iterador para los intentos de logueo del cliente
    i = 0  
    usuario_valido = False  # Esta bandera nos dirá si el cliente es válido o no

    #validacion de i
    while i < 3 and not usuario_valido:
        # Recibimos el documento del cliente
        documento = conexion.recv(1024).decode('utf-8')
        print(f"Validando la información suministrada... El documento '{documento}' lo estamos verificando en nuestra base de datos.")

        # Validación del usuario en la dbplanilla.py
        nombre_usuario = validacion_planilla(documento)
        if nombre_usuario:
            usuario_valido = True
            conexion.send("Sesión abierta. Puedes escribir 'salir' para terminar.".encode('utf-8'))
            print(f"Usuario válido: {nombre_usuario}. Sesión iniciada.")
        else:
            i += 1
            if i < 3:
                conexion.send(f"Documento no válido. Intento {i}/3. Intenta de nuevo.".encode('utf-8'))
            else:
                conexion.send("Has agotado tus intentos. Sesión cerrada.".encode('utf-8'))
                print(f"Cliente {direccion} ha agotado sus intentos. Conexión cerrada.")
                conexion.close()

                # restriccion para cerrar la sesion cuando no hayan clientes.
                with lock:
                    clientes_activos -= 1
                return

    # Si el usuario es validado, la conexión se mantiene hasta que el usuario escriba "salir"
    if usuario_valido:
        while True:
            mensaje = conexion.recv(1024).decode('utf-8')
            if not mensaje or mensaje.lower() == "salir":  # Si el cliente quiere salir
                conexion.send("Sesión cerrada. Adiós.".encode('utf-8'))
                print(f"El cliente {direccion} ha cerrado la sesión.")
                break
            else:
                conexion.send(f"Mensaje recibido: {mensaje}".encode('utf-8'))
                print(f"Mensaje de {direccion}: {mensaje}")

# fin de la conexión
    conexion.close()

    # conteo de clientes hasta cerrar la sesion cuando ya no haya clientes conectados.
    with lock:
        clientes_activos -= 1
        print(f"Clientes activos: {clientes_activos}")
    if clientes_activos == 0:
        print("Todos los clientes se han desconectado. Cerrando servidor...")
        mi_socket.close()

# Funcion para nuevas conexiones
def inicio_server():
    global clientes_activos
    while True:
        try:
            conexion, direccion = mi_socket.accept()
        except OSError:
            print("El servidor no está disponible en estos momentos, intenta mas tarde.")
            break

        print(f"Conexión aceptada de {direccion}")

        # conteo de clientes para nuevas conexiones
        with lock:
            clientes_activos += 1
            print(f"Clientes activos: {clientes_activos}")

        # Hilos "threading" para separar las conexiones clientes nuevos
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo_cliente.start()

# Funcion para iniciar el servidor si se ejecuta.
if __name__ == "__main__":
    inicio_server()