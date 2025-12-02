import tkinter as tk
from tkinter import messagebox
import threading
from clienteApi import api
from MenuPrincipal import MenuPrincipal

class LoginForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.master.title("Login - Sistema Gestor")
        self.pack(padx=20, pady=20)
        self.crearDisenio()
    
    def crearDisenio(self):
        tk.Label(self, text="INICIO DE SESIÓN", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.grid(row=1, column=1, pady=5)
        self.email_entry.insert(0, "")

        tk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        self.password_entry.insert(0, "")

        self.login_button = tk.Button(self, text="Ingresar", command=self.iniciarSesionEnHilo)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

        self.status_label = tk.Label(self, text="", fg="blue")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)

    def iniciarSesionEnHilo(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        self.status_label.config(text="Iniciando sesión...")
        self.login_button.config(state=tk.DISABLED)
        
        threading.Thread(target=self.login_worker, args=(email, password)).start()

    def login_worker(self,email, password):
        try:
            usuario = api.login(email, password)
            self.master.after(0, self.loginExitoso, usuario)
        except Exception as e:
            self.master.after(0, self.loginFallido, e)

    def loginExitoso(self, usuario):
        self.status_label.config(text=f"Bienvenido, {usuario.nombre}", fg="green")

        self.master.withdraw()

        main_window = tk.Toplevel(self.master)
        MenuPrincipal(master=main_window)

    def loginFallido(self, error):
        self.status_label.config(text="Error de inicio de sesión.", fg="red")
        self.login_button.config(state=tk.NORMAL)
        messagebox.showerror("Error de Login", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(master=root)
    app.mainloop()