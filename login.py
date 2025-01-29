import customtkinter as ctk
import sqlite3
import bcrypt
import webbrowser
from tkinter import messagebox

# Criar banco de dados e tabela se não existir
def criar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Verificar login
def verificar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and bcrypt.checkpw(senha.encode(), resultado[0]):
        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
        abrir_site()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Abrir site após login
def abrir_site():
    webbrowser.open("https://miike1000.github.io/Repositorio/")

# Registrar novo usuário
def registrar_usuario():
    def salvar_usuario():
        usuario = entry_usuario_registrar.get().strip()
        senha = entry_senha_registrar.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registro", "Usuário registrado com sucesso!")
            registrar_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe!")

    # Criar janela de registro
    registrar_window = ctk.CTkToplevel(app)
    registrar_window.title("Registrar Usuário")
    registrar_window.geometry("350x300")
    
    ctk.CTkLabel(registrar_window, text="Nome de Usuário", font=("Arial", 14)).pack(pady=10)
    entry_usuario_registrar = ctk.CTkEntry(registrar_window, placeholder_text="Usuário", width=250)
    entry_usuario_registrar.pack(pady=5)

    ctk.CTkLabel(registrar_window, text="Senha", font=("Arial", 14)).pack(pady=10)
    entry_senha_registrar = ctk.CTkEntry(registrar_window, placeholder_text="Senha", width=250, show="*")
    entry_senha_registrar.pack(pady=5)

    ctk.CTkButton(registrar_window, text="Registrar", command=salvar_usuario, width=200).pack(pady=20)

# Criar a janela principal (Login)
ctk.set_appearance_mode("dark")  # Ativar modo escuro
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Login")
app.geometry("400x350")

# Título
ctk.CTkLabel(app, text="Bem-vindo!", font=("Arial", 24)).pack(pady=20)

# Campos de entrada
entry_usuario = ctk.CTkEntry(app, placeholder_text="Usuário", width=250)
entry_usuario.pack(pady=10)

entry_senha = ctk.CTkEntry(app, placeholder_text="Senha", width=250, show="*")
entry_senha.pack(pady=10)

# Botões
ctk.CTkButton(app, text="Entrar", command=verificar_login, width=200).pack(pady=10)
ctk.CTkButton(app, text="Registrar", command=registrar_usuario, width=200).pack(pady=10)

# Criar banco de dados e iniciar app
criar_banco()
app.mainloop()
