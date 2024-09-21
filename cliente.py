import socket

direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

def iniciar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((direccion_del_Servidor, puerto_Servidor))

        while True:
            # Enviar el documento del cliente
            documento = input("Ingrese su documento: ")
            cliente.sendall(documento.encode('utf-8'))

            # Recibir la respuesta del servidor
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"Servidor: {respuesta}")

            if "Sesión cerrada" in respuesta:
                print("Conexión cerrada...")
                break

            if "Sesión iniciada" in respuesta:
                # Si la sesión es iniciada correctamente, permite enviar mensajes
                while True:
                    mensaje = input("Ingrese un mensaje (o 'salir' para cerrar la sesión): ")
                    cliente.sendall(mensaje.encode('utf-8'))
                    
                    respuesta = cliente.recv(1024).decode('utf-8')
                    print(f"El servidor ha recibido esta respuesta de su parte: {respuesta}")

                    if "Sesión cerrada" in respuesta:
                        print("Conexión cerrada.")
                        return

if __name__ == "__main__":
    iniciar_cliente()
