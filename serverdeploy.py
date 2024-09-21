import socket
import threading
from usuarios import validar_usuario

# Dirección y puerto del servidor
direccion_de_Conexion = '127.0.0.1'
puerto = 8080

# Función que maneja cada conexión de cliente
def manejar_cliente(conexion, direccion):
    print(f"Conectado con {direccion}")
    
    try:
        while True:
            # Recibir documento del cliente
            documento = conexion.recv(1024).decode('utf-8')  # Decodificar el documento recibido
            if not documento:
                break

            # Valida el documento
            if validar_usuario(documento):
                conexion.sendall("Sesión iniciada".encode('utf-8'))  # Enviar respuesta codificada en UTF-8
                print(f"Bienvenido, su sesión ha comenzado satisfactoriamente.")
                
                # Mantener la sesión abierta hasta que el usuario escriba 'Salir'
                while True:
                    try:
                        mensaje = conexion.recv(1024).decode('utf-8')  # Recibir mensaje del cliente
                        if not mensaje:
                            break
                        if mensaje.lower() == "salir":
                            conexion.sendall("Sesión cerrada. Adiós.".encode('utf-8'))  # Enviar mensaje de cierre
                            print(f"El usuario {direccion} ha cerrado la sesión.")
                            break
                        else:
                            print(f"Mensaje del cliente {direccion}: {mensaje}")
                            conexion.sendall(f"Echo: {mensaje}".encode('utf-8'))  # Responder al cliente con el mensaje recibido
                    except ConnectionAbortedError:
                        print(f"Conexión con el cliente {direccion} ha sido abortada.")
                        break
                    except ConnectionResetError:
                        print(f"Conexión con el cliente {direccion} ha sido reiniciada.")
                        break

                break
            else:
                conexion.sendall("Documento no válido. Por favor intente de nuevo.".encode('utf-8'))  # Enviar mensaje codificado en UTF-8
    except ConnectionAbortedError:
        print(f"Conexión con el cliente {direccion} fue abortada.")
    except ConnectionResetError:
        print(f"Conexión con el cliente {direccion} fue reiniciada.")
    finally:
        conexion.close()

# Función principal del servidor
def iniciar_servidor():
    # Creando el socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((direccion_de_Conexion, puerto))
        s.listen()
        print(f"Servidor iniciado en {direccion_de_Conexion}:{puerto}")

        while True:
            # Esperando conexiones
            conexion, direccion = s.accept()
            # Crear un hilo para manejar cada cliente
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
            hilo_cliente.start()

if __name__ == "__main__":
    iniciar_servidor()