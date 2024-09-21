import socket


direccion_de_Conexion = '127.0.0.1'
puerto = 8080

def iniciar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((direccion_de_Conexion, puerto))

        while True:
            documento = input("Ingrese su documento: ")
            s.sendall(documento.encode('utf-8'))  

            # Respuesta del servidor
            respuesta = s.recv(1024).decode('utf-8')  
            print(f"Servidor: {respuesta}")

            if respuesta == "Sesión iniciada":
                print("Conexión exitosa. bienvenido")
                break

if __name__ == "__main__":
    iniciar_cliente()