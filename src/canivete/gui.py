import customtkinter as ctk
import threading
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from canivete.core.network import scan_network, flush_dns, ip_release, ip_renew, winsock_reset
from canivete.core.traffic import monitor_traffic
from canivete.core.system import system_info, is_admin
import subprocess
import re

# Configurações visuais
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CaniveteGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Canivete Suíço Network Toolkit - v0.4.0")
        self.geometry("1100x700")

        # Configuração de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CANIVETE v0.4", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Botões da Lateral
        self.btn_scan = ctk.CTkButton(self.sidebar, text="Network Scan", command=self.show_scan_frame)
        self.btn_scan.grid(row=1, column=0, padx=20, pady=10)

        self.btn_traffic = ctk.CTkButton(self.sidebar, text="Monitor de Tráfego", command=self.show_traffic_frame)
        self.btn_traffic.grid(row=2, column=0, padx=20, pady=10)

        self.btn_maint = ctk.CTkButton(self.sidebar, text="Manutenção OS", command=self.show_maintenance_frame)
        self.btn_maint.grid(row=3, column=0, padx=20, pady=10)

        self.btn_print = ctk.CTkButton(self.sidebar, text="Impressoras", command=self.show_printer_frame)
        self.btn_print.grid(row=4, column=0, padx=20, pady=10)

        self.btn_procs = ctk.CTkButton(self.sidebar, text="Processos/Rede", command=self.show_process_frame)
        self.btn_procs.grid(row=5, column=0, padx=20, pady=10)

        self.btn_system = ctk.CTkButton(self.sidebar, text="System Info", command=self.show_system_frame)
        self.btn_system.grid(row=6, column=0, padx=20, pady=10)

        # --- ÁREA CENTRAL ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.show_welcome()

    def clear_main_frame(self):
        self.is_monitoring = False
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Bem-vindo ao Canivete Suíço", font=("Arial", 24, "bold")).pack(expand=True)

    # --- ABA: NETWORK SCAN ---
    def show_scan_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Network Scanner", font=("Arial", 20, "bold")).pack(pady=10)
        self.entry_target = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: 192.168.1.0/24", width=300)
        self.entry_target.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Iniciar Scan", command=self.run_scan_thread).pack(pady=10)
        self.console = ctk.CTkTextbox(self.main_frame, width=600, height=350)
        self.console.pack(pady=10, padx=20)

    def run_scan_thread(self):
        target = self.entry_target.get()
        if not target: return
        self.console.insert("end", f">> Escaneando {target}...\n")
        threading.Thread(target=lambda: self.execute_scan(target), daemon=True).start()

    def execute_scan(self, target):
        results = scan_network(target)
        self.console.delete("1.0", "end")
        for host, status in results.items():
            self.console.insert("end", f"[{'ONLINE' if status else 'OFFLINE'}] {host}\n")

    # --- ABA: MANUTENÇÃO (Resgatada da V1) ---
    def show_maintenance_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Reparos e Manutenção", font=("Arial", 20, "bold")).pack(pady=10)
        
        container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20)

        btns = [
            ("Limpar Cache DNS", lambda: self.run_sys_cmd(flush_dns)),
            ("Resetar Winsock/Rede", lambda: self.run_sys_cmd(winsock_reset)),
            ("SFC /Scannow (Reparo)", lambda: self.run_shell("sfc /scannow")),
            ("Limpar Arquivos Temp", self.clean_temp_action),
            ("Otimizar Energia", lambda: self.run_shell("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"))
        ]

        for text, cmd in btns:
            ctk.CTkButton(container, text=text, command=cmd, width=250).pack(pady=5)

        self.console = ctk.CTkTextbox(self.main_frame, width=600, height=200)
        self.console.pack(pady=10)

    # --- ABA: IMPRESSORAS (Resgatada da V1) ---
    def show_printer_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Suporte de Impressão", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkButton(self.main_frame, text="Abrir Painel de Impressoras", command=lambda: subprocess.run("control printers", shell=True)).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Reiniciar Spooler", fg_color="orange", command=self.restart_spooler).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Fix Registro PrintNightmare", command=self.fix_printer_registry).pack(pady=10)

    # --- ABA: PROCESSOS (Tabela Inteligente da V1) ---
    def show_process_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Conexões de Rede Ativas", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Treeview (Tabela estilo V1)
        columns = ("Protocolo", "Local", "Remoto", "Estado", "PID")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)
        for col in columns: self.tree.heading(col, text=col)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(self.main_frame, text="Atualizar Lista", command=self.update_netstat).pack(pady=10)
        self.update_netstat()

    def update_netstat(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        cmd = "netstat -ano" if platform.system() == "Windows" else "ss -tulpn"
        out = subprocess.check_output(cmd, shell=True).decode("cp850")
        for line in out.splitlines()[4:]:
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 4:
                self.tree.insert("", "end", values=parts[:5])

    # --- ABA: TRAFFIC MONITOR ---
    def show_traffic_frame(self):
        self.clear_main_frame()
        self.down_label = ctk.CTkLabel(self.main_frame, text="Download: 0 KB/s", font=("Arial", 30))
        self.down_label.pack(pady=40)
        self.up_label = ctk.CTkLabel(self.main_frame, text="Upload: 0 KB/s", font=("Arial", 30))
        self.up_label.pack(pady=10)
        self.is_monitoring = True
        self.update_traffic()

    def update_traffic(self):
        if hasattr(self, 'is_monitoring') and self.is_monitoring:
            stats = monitor_traffic(interval=1)
            self.down_label.configure(text=f"Download: {stats['download_kb_s']} KB/s")
            self.up_label.configure(text=f"Upload: {stats['upload_kb_s']} KB/s")
            self.after(1000, self.update_traffic)

    # --- ABA: SYSTEM INFO ---
    def show_system_frame(self):
        self.clear_main_frame()
        info = system_info()
        for key, value in info.items():
            ctk.CTkLabel(self.main_frame, text=f"{key}: {value}", font=("Arial", 16)).pack(pady=5)

    # --- FUNÇÕES DE SUPORTE ---
    def run_sys_cmd(self, func):
        res = func()
        self.console.insert("end", f">> {res.get('stdout') or res.get('error') or 'Sucesso'}\n")

    def run_shell(self, cmd):
        if not is_admin():
            messagebox.showerror("Erro", "Esta ação requer privilégios de Administrador!")
            return
        threading.Thread(target=lambda: subprocess.run(cmd, shell=True), daemon=True).start()
        self.console.insert("end", f">> Comando enviado: {cmd}\n")

    def restart_spooler(self):
        self.run_shell("net stop spooler && net start spooler")
        messagebox.showinfo("Impressoras", "Serviço de Spooler reiniciado!")

    def clean_temp_action(self):
        import shutil, os, tempfile
        temp = tempfile.gettempdir()
        for item in os.listdir(temp):
            try:
                p = os.path.join(temp, item)
                if os.path.isfile(p): os.unlink(p)
                else: shutil.rmtree(p)
            except: continue
        self.console.insert("end", ">> Limpeza de temporários concluída.\n")

    def fix_printer_registry(self):
        cmd = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f'
        self.run_shell(cmd)
        messagebox.showinfo("Registro", "Correção aplicada! Reinicie o PC.")

def launch_gui():
    app = CaniveteGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()