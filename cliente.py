import socket

direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

def iniciar_cliente():
    # intercambio de datos y prevencion de perdida de datos
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((direccion_del_Servidor, puerto_Servidor))

        while True:
            #Se manda el documento a la espera de la respuesta del servidor
            documento = input("Ingrese su documento: ")
            cliente.sendall(documento.encode('utf-8'))

            #Se recibe respuesta del servidor y se procede a validarlas
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"Servidor: {respuesta}")

            if "Sesión cerrada" in respuesta:
                print("Conexión cerrada...")
                break

            #Mensaje para hacer saber al cliente de que puede escribirle al servidor y que la conexion se cerrará solo cuando escriba "salir"
            if "Ahora puedes salir" in respuesta:
                while True:
                    mensaje = input("Ingrese un mensaje (o 'salir' para cerrar la sesión): ")
                    cliente.sendall(mensaje.encode('utf-8'))

                    respuesta = cliente.recv(1024).decode('utf-8')
                    print(f"El servidor ha recibido esta respuesta de su parte: {respuesta}")

                    if mensaje.lower() == "salir":
                        print("Conexión cerrada.")
                        cliente.sendall("salir".encode('utf-8'))
                        return

if __name__ == "__main__":
    iniciar_cliente()
