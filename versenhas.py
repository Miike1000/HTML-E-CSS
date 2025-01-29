import sqlite3
import bcrypt

usuario_input = input("Digite o nome de usuário: ")
senha_input = input("Digite a senha: ")

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Buscar a senha criptografada do usuário
cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario_input,))
resultado = cursor.fetchone()

if resultado:
    senha_armazenada = resultado[0]

    # Comparar a senha digitada com a senha criptografada
    if bcrypt.checkpw(senha_input.encode(), senha_armazenada.encode()):
        print("Senha correta!")
    else:
        print("Senha incorreta!")
else:
    print("Usuário não encontrado.")

conn.close()
