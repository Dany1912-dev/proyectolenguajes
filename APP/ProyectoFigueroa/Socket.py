import socket
import threading
from tkinter import messagebox

class Socket:
    def __init__(self, masterUi, host='127.0.0.1', puerto=65432):
        self.masterUi = masterUi
        self.host = host
        self.puerto = puerto
        self.Ejecucion = False
        self.serverSocket = None

    def iniciarServicio(self):
        self.Ejecucion = True

        hilo = threading.Thread(target=self.escuchar, daemon=True)
        hilo.start()

    def escuchar(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.host, self.puerto))
            self.serverSocket.listen()
            print(f"Socket escuchando en {self.host}:{self.puerto}")

            while self.Ejecucion:
                conn, addr = self.serverSocket.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        mensaje = data.decode('utf-8')
                        self.mostrarAlerta(mensaje)
        
        except Exception as e:
            print(f"Error socket: {e}")
        finally:
            if self.serverSocket:
                self.serverSocket.close()

    def mostrarAlerta(self, mensaje):
        self.masterUi.after(0, lambda: messagebox.showinfo("Notificacion automatica", mensaje))

    