from dbplanilla import obtener_usuarios_validos

#Validacion para obtener el nombre del usuario una vez validado
def validacion_planilla(documento):
    usuarios = obtener_usuarios_validos()
    if documento in usuarios:
        return usuarios[documento] 
    else:
        return None