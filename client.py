import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, font

# Fungsi untuk mengvalidasi IP address yang diinput
def validate_ipv4(ip):
    if ip == "localhost":
        return True
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        number = int(part)
        if number < 0 or number > 255:
            return False
    return True

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BuzzChat Setup")
        self.root.geometry("400x350")
        self.root.configure(bg="#2C3E50")

        self.client_ip = ""
        self.client_port = None
        self.server_ip = ""
        self.server_port = None
        self.client_socket = None
        self.username = ""
        self.password = "JARKOM" #password chatroom
        self.running = True

        # Warna chat dan fontnya
        self.custom_font = font.Font(family="Helvetica", size=12)
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.text_color = "#ECF0F1"
        self.entry_bg = "#34495E"
        self.button_bg = "#1ABC9C"

        self.setup_page()

    def setup_page(self):
        # Judul page input IP
        self.title_label = tk.Label(self.root, text="Enter Connection Info", font=self.title_font, fg="#1ABC9C", bg="#2C3E50")
        self.title_label.pack(pady=(15, 10))

        # Client IP dan Port
        tk.Label(self.root, text="Client IP Address:", bg="#2C3E50", fg=self.text_color).pack()
        self.client_ip_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.client_ip_entry.pack(pady=5)
        
        tk.Label(self.root, text="Client Port Number:", bg="#2C3E50", fg=self.text_color).pack()
        self.client_port_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.client_port_entry.pack(pady=5)

        # Server IP dan Port
        tk.Label(self.root, text="Server IP Address:", bg="#2C3E50", fg=self.text_color).pack()
        self.server_ip_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.server_ip_entry.pack(pady=5)
        
        tk.Label(self.root, text="Server Port Number:", bg="#2C3E50", fg=self.text_color).pack()
        self.server_port_entry = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.server_port_entry.pack(pady=5)

        # Connect Button
        self.connect_button = tk.Button(self.root, text="Connect", font=self.custom_font, bg=self.button_bg, fg="#ffffff", command=self.connect_to_server)
        self.connect_button.pack(pady=(20, 10))

    def connect_to_server(self):
        try:
            # Meminta input users
            self.client_ip = self.client_ip_entry.get()
            self.client_port = int(self.client_port_entry.get())
            self.server_ip = self.server_ip_entry.get()
            self.server_port = int(self.server_port_entry.get())

            # Mengvalidasi IP address dan port
            if not validate_ipv4(self.client_ip) or not validate_ipv4(self.server_ip):
                messagebox.showerror("Error", "Invalid IP address format.")
                return
            if not (0 <= self.client_port <= 65535) or not (0 <= self.server_port <= 65535):
                messagebox.showerror("Error", "Port numbers must be between 0 and 65535.")
                return

            # Inisialisasi socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.bind((self.client_ip, self.client_port))

            # Return kesalahan port
            self.start_chatroom()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for port.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def start_chatroom(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("BuzzChat")
        self.root.geometry("500x600")
        
        # Chatroom UI elements
        self.title_label = tk.Label(self.root, text="BuzzChat", font=self.title_font, fg="#1ABC9C", bg="#2C3E50")
        self.title_label.pack(pady=10)
        
        # Chat display area
        self.chat_display = tk.Text(self.root, state="disabled", wrap="word", font=self.custom_font, bg=self.entry_bg, fg=self.text_color)
        self.chat_display.pack(pady=10, padx=10, expand=True, fill="both")
        
        # Message entry box
        self.entry_msg = tk.Entry(self.root, font=self.custom_font, bg=self.entry_bg, fg=self.text_color, relief="flat")
        self.entry_msg.pack(fill="x", padx=10, pady=10)
        self.entry_msg.bind("<Return>", self.send_message)
        
        # Quit button
        self.quit_button = tk.Button(self.root, text="Quit", font=self.custom_font, bg=self.button_bg, fg="#ffffff", command=self.quit_chat)
        self.quit_button.pack(pady=10)

        # Autentikasi dan set up koneksi di chatroom
        self.authenticate_user()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    # Handling password success dan error
    def authenticate_user(self):
        while True:
            password_input = simpledialog.askstring("Password", "Enter the password to join the chat:", show='*', parent=self.root)
            if password_input == self.password:
                messagebox.showinfo("Success", "Password correct. Connecting to server...", parent=self.root)
                break
            else:
                messagebox.showerror("Error", "Incorrect password. Please try again.", parent=self.root)
        
        # Handling username success dan error
        while True:
            self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.root)
            self.client_socket.sendto(f"JOIN {self.username} {self.password}".encode('utf-8'), (self.server_ip, self.server_port))
            response, _ = self.client_socket.recvfrom(1024)
            response_message = response.decode('utf-8')
            if response_message == "Username taken.":
                messagebox.showerror("Error", "Username taken. Please choose another username!", parent=self.root)
            else:
                messagebox.showinfo("Connected", "Connected to server. You can now start chatting!", parent=self.root)
                break

    def send_message(self, event=None):
        message = self.entry_msg.get()
        if message.lower() == "quit":
            self.quit_chat()
        else:
            self.display_message(f"You: {message}")
            self.client_socket.sendto(f"MSG {self.username} {message}".encode('utf-8'), (self.server_ip, self.server_port))
            self.entry_msg.delete(0, tk.END)

    def receive_messages(self):
        while self.running:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                self.display_message(message.decode('utf-8'))
            except OSError:
                break

    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def quit_chat(self):
        self.running = False
        self.client_socket.sendto(f"QUIT {self.username}".encode('utf-8'), (self.server_ip, self.server_port))
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    client_app = ChatClient()
    client_app.root.mainloop()
