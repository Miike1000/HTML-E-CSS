import sqlite3

def ver_senhas():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Buscar todas as senhas salvas
    cursor.execute("SELECT id, usuario, senha FROM usuarios")
    usuarios = cursor.fetchall()
    
    if usuarios:
        print("Usuários cadastrados:")
        for id, usuario, senha in usuarios:
            print(f"ID: {id} | Usuário: {usuario} | Senha: {senha}")  # Senha aparece em texto normal
    else:
        print("Nenhum usuário cadastrado.")

    conn.close()

ver_senhas()
