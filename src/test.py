from werkzeug.security import generate_password_hash

# Genera el hash de la contraseña
hashed_password = generate_password_hash("1234")

# Imprime el hash generado
print(hashed_password)