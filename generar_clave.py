from cryptography.fernet import Fernet

# Generar la clave
def generar_clave():
    clave = Fernet.generate_key()
    
    # Guardar la clave en un archivo llamado "secret.key"
    with open("secret.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

# Llamamos a la función para generar la clave
generar_clave()
