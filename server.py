import socket
import threading
import tkinter as tk
from tkinter import font, messagebox
from typing import Dict

class ChatServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BuzzChat Server Setup")
        self.root.geometry("400x300")
        self.root.configure(bg="#2C3E50")

        self.server_socket = None
        self.clients: Dict[str, tuple] = {}
        self.password = "JARKOM"
        self.running = True
        self.host = ""
        self.port = None

        # Warna chat dan fontnya
        self.custom_font = font.Font(family="Helvetica", size=12)
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.text_color = "#ECF0F1"
        self.entry_bg = "#34495E"
        self.button_bg = "#1ABC9C"

        self.setup_page()

    def setup_page(self):
        # Judul page
        self.title_label = tk.Label(self.root, text="BuzzChat Server Setup", font=self.title_font, fg="#1ABC9C", bg="#2C3E50")
        self.title_label.pack(pady=10)

        # Server IP and Port
        tk.Label(self.root, text="Server IP Address:", bg="#2C3E50", fg=self.text_color).pack()
        self.host_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.host_entry.pack(pady=5)

        tk.Label(self.root, text="Server Port Number:", bg="#2C3E50", fg=self.text_color).pack()
        self.port_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.port_entry.pack(pady=5)

        # Start Server Button
        self.start_button = tk.Button(self.root, text="Start Server", font=self.custom_font, bg=self.button_bg, fg="#ffffff", command=self.start_server)
        self.start_button.pack(pady=20)

    def start_server(self):
        try:
            # Meminta input users
            self.host = self.host_entry.get()
            self.port = int(self.port_entry.get())

            # Inisialisasi socket and bind server address
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((self.host, self.port))

            # Menutup setup page dan membuka main server GUI
            self.run_server_gui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the port.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")

    def run_server_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("BuzzChat Server")
        self.root.geometry("500x500")

        # Judul page
        self.title_label = tk.Label(self.root, text="BuzzChat Server", font=self.title_font, fg="#1ABC9C", bg="#2C3E50")
        self.title_label.pack(pady=10)

        # Server status display area
        self.status_display = tk.Text(self.root, state="disabled", wrap="word", font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.status_display.pack(pady=10, padx=10, expand=True, fill="both")

        # Stop Server Button
        self.stop_button = tk.Button(self.root, text="Stop Server", font=self.custom_font, bg=self.button_bg, fg="#ffffff", command=self.stop_server)
        self.stop_button.pack(pady=10)

        # Start the server thread
        self.update_status("Server started. Waiting for clients to connect...")
        threading.Thread(target=self.run_server, daemon=True).start()

    def run_server(self):
        while self.running:
            try:
                message, client_address = self.server_socket.recvfrom(1024)
                threading.Thread(target=self.handle_client, args=(message, client_address)).start()
            except Exception as e:
                self.update_status(f"Server error: {e}")

    def handle_client(self, message: bytes, client_address: tuple):
        decoded_message = message.decode('utf-8')

        if decoded_message.startswith("JOIN"):
            try:
                _, username, client_password = decoded_message.split(" ", 2)
            except ValueError:
                self.server_socket.sendto("Invalid join format.".encode('utf-8'), client_address)
                return

            # Ketika salah memasukkan password
            if client_password != self.password:
                self.server_socket.sendto("Incorrect password.".encode('utf-8'), client_address)
                return
            
            # Baru saja memasuki chatroom
            if username not in self.clients:
                self.clients[username] = client_address
                self.update_status(f"{username} joined from {client_address}")
                self.server_socket.sendto("Password correct. You have joined the chat.".encode('utf-8'), client_address)
                self.broadcast(f"{username} has joined the chat.", client_address)
            else:
                self.server_socket.sendto("Username taken.".encode('utf-8'), client_address)

        elif decoded_message.startswith("MSG"):
            _, username, msg_content = decoded_message.split(" ", 2)
            if username in self.clients:
                self.update_status(f"Message from {username}: {msg_content}")
                self.broadcast(f"{username}: {msg_content}", client_address)

        # Ketika memencet tombol quit
        elif decoded_message.startswith("QUIT"):
            _, username = decoded_message.split(" ", 1)
            if username in self.clients:
                self.update_status(f"{username} left the chat.")
                self.broadcast(f"{username} has left the chat.", client_address)
                del self.clients[username]

    def broadcast(self, message: str, sender_address: tuple):
        for address in self.clients.values():
            if address != sender_address:
                try:
                    self.server_socket.sendto(message.encode('utf-8'), address)
                except Exception as e:
                    self.update_status(f"Error sending message to {address}: {e}")

    def update_status(self, message: str):
        self.status_display.config(state="normal")
        self.status_display.insert(tk.END, message + "\n")
        self.status_display.config(state="disabled")
        self.status_display.see(tk.END)

    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.update_status("Server stopped.")
        messagebox.showinfo("BuzzChat Server", "Server has been stopped.")
        self.root.quit()

if __name__ == "__main__":
    server_app = ChatServer()
    server_app.root.mainloop()
