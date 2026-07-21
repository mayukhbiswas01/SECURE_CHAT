# -*- coding: utf-8 -*-
<<<<<<< HEAD
# client_gui.py - Scalable GUI Client for Assignment 8
# Author: Mayukh Biswas

import socket
import threading
import json
import hashlib
import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

CONFIG_FILE = "config.json"
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"client": {"server_ip": "10.0.0.1", "server_port": 5000, "reconnect_attempts": 5, "reconnect_delay": 3}}

CONFIG = load_config()["client"]

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ISEA Secure Chat - Optimized")
        self.root.geometry("450x550")

        self.sock = None
        self.is_connected = False
        self.username = ""
        self.password = ""

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.user_entry = tk.Entry(self.login_frame)
        self.user_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.pass_entry = tk.Entry(self.login_frame, show="*")
        self.pass_entry.grid(row=1, column=1)

        self.btn_connect = tk.Button(self.login_frame, text="Connect", command=self.attempt_connection)
        self.btn_connect.grid(row=2, columnspan=2, pady=10)

        # Chat Display Frame
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', height=18)
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Input Frame
        self.msg_entry = tk.Entry(self.root)
        self.msg_entry.pack(padx=10, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log_ui(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def attempt_connection(self):
        self.username = self.user_entry.get().strip()
        self.password = self.pass_entry.get().strip()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Fields cannot be empty!")
            return

        threading.Thread(target=self.connect_and_auth, daemon=True).start()

    def connect_and_auth(self):
        attempts = CONFIG["reconnect_attempts"]
        for i in range(attempts):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((CONFIG["server_ip"], CONFIG["server_port"]))
                
                # Handshake
                prompt = self.sock.recv(1024).decode('utf-8')
                if "AUTH_REQUEST" in prompt:
                    hashed = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                    payload = f"{self.username}::{hashed}\n"
                    self.sock.sendall(payload.encode('utf-8'))

                    resp = self.sock.recv(1024).decode('utf-8')
                    if "WELCOME" in resp:
                        self.is_connected = True
                        self.log_ui("[SYSTEM] Connected Successfully!")
                        threading.Thread(target=self.receive_loop, daemon=True).start()
                        return
                    else:
                        self.log_ui(f"[REJECTED] {resp.strip()}")
                        self.sock.close()
                        return
            except Exception as e:
                self.log_ui(f"[WARN] Connection attempt {i+1} failed...")
                time.sleep(CONFIG["reconnect_delay"])

        self.log_ui("[ERROR] Could not connect to server.")

    def receive_loop(self):
        """Task 2: Reliability & Timeout handling"""
        while self.is_connected:
            try:
                data = self.sock.recv(4096).decode('utf-8')
                if not data:
                    break
                
                lines = data.strip().split('\n')
                for line in lines:
                    if line == "PING":
                        self.sock.sendall(b"PONG\n") # Task 1 Keep-alive
                    elif line == "SERVER_SHUTDOWN":
                        self.log_ui("[SYSTEM] Server has closed.")
                        self.is_connected = False
                    else:
                        self.log_ui(line)
            except Exception:
                break
        
        if self.is_connected:
            self.log_ui("[WARN] Connection lost. Attempting auto-reconnect...")
            self.is_connected = False
            self.connect_and_auth() # Task 2 Auto-reconnect

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg and self.is_connected:
            try:
                self.sock.sendall((msg + "\n").encode('utf-8'))
                self.msg_entry.delete(0, tk.END)
            except:
                self.log_ui("[ERROR] Failed to send message.")

    def on_closing(self):
        self.is_connected = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
=======
# client.py - Updated for Assignment 7 Security Standards
import socket
import threading
import sys
import hashlib

def get_sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data: 
                print("\n[SERVER] Connection closed.")
                break
            print(f"\n{data.decode('utf-8').strip()}", flush=True)
        except: 
            break

def main():
    # 1. Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("10.0.0.1", 5000))
    except:
        print("[ERROR] Server unreachable.")
        return

    # 2. Handshake & Authentication (The Secured Logic)
    try:
        prompt = sock.recv(1024).decode('utf-8')
        if "AUTH_REQUEST" in prompt:
            username = input("Enter Username: ").strip()
            password = input("Enter Password: ").strip()
            
            # Security Fix: Protocol Injection Prevention
            if "::" in username:
                print("[ERROR] Invalid characters in username.")
                sock.close()
                return

            # Security Fix: Client-side Hashing
            pwd_hash = get_sha256(password)
            auth_string = f"{username}::{pwd_hash}"
            
            sock.sendall(auth_string.encode('utf-8'))
            
            # 3. Validation Response
            response = sock.recv(1024).decode('utf-8')
            if "WELCOME" in response:
                print("[SUCCESS] Connected! Type your message and hit Enter.")
            else:
                print(f"[REJECTED] {response}")
                sock.close()
                return
    except Exception as e:
        print(f"[ERROR] Handshake failed: {e}")
        sock.close()
        return

    # Start chat thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    
    # 4. Main Chat Loop
    while True:
        try:
            msg = input()
            if not msg: continue
            if msg.lower() == 'exit': break
            sock.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt: break
    sock.close()

if __name__ == "__main__":
    main()
>>>>>>> b4499e4f5098d1e0c590fbc3dc86cd236be7eade
