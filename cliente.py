import socket

direccion_del_Servidor = 'localhost'
puerto_Servidor = 8080

def iniciar_cliente():
    # Intercambio de datos y prevención de pérdida de datos
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((direccion_del_Servidor, puerto_Servidor))

        while True:
            # Se manda el documento a la espera de la respuesta del servidor
            documento = input("Ingrese su documento: ")
            cliente.sendall(documento.encode('utf-8'))

            # Se recibe respuesta del servidor y se procede a validarlas
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"Servidor: {respuesta}")

            if "Sesión cerrada" in respuesta:
                print("Conexión cerrada...")
                break
            
            # Si la sesión está abierta, permite enviar mensajes
            if "Sesión abierta" in respuesta:
                while True:
                    mensaje = input("¿Qué quieres mandarle al servidor? (o 'salir' para cerrar la sesión): ")
                    cliente.sendall(mensaje.encode('utf-8'))

                    respuesta = cliente.recv(1024).decode('utf-8')
                    print(f"El servidor ha respondido: {respuesta}")

                    if mensaje.lower() == "salir":
                        print("Conexión cerrada.")
                        break

                # Salir del bucle principal para volver a solicitar el documento
                break

if __name__ == "__main__":
    iniciar_cliente()
