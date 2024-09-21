from dbplanilla import obtener_usuarios_validos
def validar_usuario(documento):
    usuarios = obtener_usuarios_validos()
    if documento in usuarios:
        print(f"Usuario válido: {usuarios[documento]}")
        return True
    else:
        return False
