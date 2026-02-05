import customtkinter as ctk
import threading
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from canivete.core.network import scan_network, flush_dns, ip_release, ip_renew, winsock_reset
from canivete.core.traffic import monitor_traffic
from canivete.core.system import system_info, is_admin, run_windows_repair
import subprocess
import re
import os
import sys
import webbrowser 
from datetime import datetime 


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CaniveteGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Canivete Suíço Network Toolkit - v0.4.0") 
        self.geometry("1100x750")

        # --- CONFIGURAÇÃO DE ÍCONE ---
        self.load_icon()

        # Configuração de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CANIVETE v0.4.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Botões da Lateral
        self.btn_scan = ctk.CTkButton(self.sidebar, text="Network Scan", command=self.show_scan_frame)
        self.btn_scan.grid(row=1, column=0, padx=20, pady=10)

        self.btn_traffic = ctk.CTkButton(self.sidebar, text="Monitor de Tráfego", command=self.show_traffic_frame)
        self.btn_traffic.grid(row=2, column=0, padx=20, pady=10)

        self.btn_maint = ctk.CTkButton(self.sidebar, text="Manutenção Rede", command=self.show_maintenance_frame)
        self.btn_maint.grid(row=3, column=0, padx=20, pady=10)

        self.btn_ms_tools = ctk.CTkButton(self.sidebar, text="Ferramentas MS", command=self.show_ms_tools_frame)
        self.btn_ms_tools.grid(row=4, column=0, padx=20, pady=10)

        self.btn_print = ctk.CTkButton(self.sidebar, text="Impressoras", command=self.show_printer_frame)
        self.btn_print.grid(row=5, column=0, padx=20, pady=10)

        self.btn_procs = ctk.CTkButton(self.sidebar, text="Processos/Rede", command=self.show_process_frame)
        self.btn_procs.grid(row=6, column=0, padx=20, pady=10)

        self.btn_system = ctk.CTkButton(self.sidebar, text="System Info", command=self.show_system_frame)
        self.btn_system.grid(row=7, column=0, padx=20, pady=10)

        # Botão Especial de Relatório
        self.btn_report = ctk.CTkButton(self.sidebar, text="Relatório HTML", fg_color="green", hover_color="darkgreen", command=self.generate_advanced_report)
        self.btn_report.grid(row=8, column=0, padx=20, pady=30)

        # --- ÁREA CENTRAL ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.show_welcome()

    def load_icon(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                base_path = os.path.abspath(os.path.join(current_dir, ".."))

            icon_path = os.path.join(base_path, "docs", "app_v4.ico")

            if os.path.exists(icon_path):
                icon_path = os.path.normpath(icon_path)
                self.wm_iconbitmap(icon_path)
                self.iconbitmap(icon_path)
                self.after(200, lambda: self.iconbitmap(icon_path))
            else:
                print(f"DEBUG: Ícone não encontrado em: {icon_path}")
        except Exception as e:
            print(f"DEBUG: Erro ao aplicar ícone: {e}")

    def safe_log(self, message):
        """Atualiza o console de forma segura para evitar erros de Thread e Atributo"""
        def update():
            if hasattr(self, 'console') and self.console.winfo_exists():
                self.console.insert("end", message)
                self.console.see("end")
        self.after(0, update)

    def clear_main_frame(self):
        self.is_monitoring = False
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Canivete Suíço v0.4.0", font=("Arial", 24, "bold")).pack(expand=True)
        ctk.CTkLabel(self.main_frame, text="Pronto para Diagnóstico Reativo", font=("Arial", 14)).pack(expand=True)

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
        self.safe_log(f">> Escaneando {target}...\n")
        threading.Thread(target=lambda: self.execute_scan(target), daemon=True).start()

    def execute_scan(self, target):
        results = scan_network(target)
        self.after(0, lambda: self.console.delete("1.0", "end"))
        for host, status in results.items():
            self.safe_log(f"[{'ONLINE' if status else 'OFFLINE'}] {host}\n")

    def show_maintenance_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Manutenção de Rede e OS", font=("Arial", 20, "bold")).pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(self.main_frame, width=600, height=400)
        scroll.pack(fill="both", expand=True, padx=20)

        # Botoões de Rede e Limpeza
        ctk.CTkLabel(scroll, text="Recursos de Rede", font=("Arial", 14, "bold"), text_color="#3b8ed0").pack(pady=5)
        btns_network = [
            ("IP Release", lambda: self.run_sys_cmd(ip_release)),
            ("IP Renew", lambda: self.run_sys_cmd(ip_renew)),
            ("Limpar Cache DNS", lambda: self.run_sys_cmd(flush_dns)),
            ("Resetar Winsock/Rede", lambda: self.run_sys_cmd(winsock_reset)),
            ("Exibir Configurações de IP", lambda: self.run_shell("ipconfig /all")),
        ]
        for text, cmd in btns_network:
            ctk.CTkButton(scroll, text=text, command=cmd, width=300).pack(pady=5)

        # Botões de Reparo de Sistema (Novidade v0.4.0)
        ctk.CTkLabel(scroll, text="Reparo de Imagem Windows (DISM/SFC)", font=("Arial", 14, "bold"), text_color="#e67e22").pack(pady=(15, 5))
        btns_repair = [
            ("SFC /Scannow (Reparo de Arquivos)", lambda: self.execute_repair_task("sfc")),
            ("DISM CheckHealth (Verificação Rápida)", lambda: self.execute_repair_task("dism_check")),
            ("DISM ScanHealth (Busca Profunda)", lambda: self.execute_repair_task("dism_scan")),
            ("DISM RestoreHealth (Reparo de Imagem)", lambda: self.execute_repair_task("dism_restore")),
        ]
        for text, cmd in btns_repair:
            ctk.CTkButton(scroll, text=text, command=cmd, width=300, fg_color="#444", hover_color="#555").pack(pady=5)

        ctk.CTkLabel(scroll, text="Limpeza", font=("Arial", 14, "bold"), text_color="#2ecc71").pack(pady=(15, 5))
        ctk.CTkButton(scroll, text="Limpar Arquivos Temp", command=self.clean_temp_action, width=300).pack(pady=5)

        self.console = ctk.CTkTextbox(self.main_frame, width=600, height=150)
        self.console.pack(pady=10)

    def execute_repair_task(self, repair_type):
        """Executa tarefas de reparo DISM/SFC em thread para não travar a GUI"""
        self.safe_log(f">> Iniciando tarefa: {repair_type.upper()}. Aguarde, isso pode demorar...\n")
        def task():
            result = run_windows_repair(repair_type)
            self.safe_log(f"{result}\n>> Tarefa concluída.\n")
        threading.Thread(target=task, daemon=True).start()

    def show_ms_tools_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Atalhos Administrativos Windows", font=("Arial", 20, "bold")).pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(self.main_frame, width=600, height=450)
        scroll.pack(fill="both", expand=True, padx=20)

        tools = [
            ("Configurações do Sistema", "sysdm.cpl"),
            ("Informações do Sistema", "msinfo32"),
            ("Configuração do MSConfig", "msconfig"),
            ("Opções de Internet", "inetcpl.cpl"),
            ("Serviços Windows", "services.msc"),
            ("Políticas de Segurança", "secpol.msc"),
            ("Visualizador de Eventos", "eventvwr.msc"),
            ("Monitor de Desempenho", "perfmon.msc"),
            ("Monitor de Recursos", "resmon"),
            ("Certificados (Usuário)", "certmgr.msc"),
            ("Certificados (Computador)", "certlm.msc"),
        ]

        for text, cmd in tools:
            ctk.CTkButton(scroll, text=text, fg_color="#333", command=lambda c=cmd: self.run_shell(c), width=300).pack(pady=5)

    def generate_advanced_report(self):
        if not hasattr(self, 'console') or not self.console.winfo_exists():
            self.show_maintenance_frame()

        def task():
            try:
                self.safe_log(">> Iniciando diagnóstico de gargalo...\n")
                ping_google = subprocess.check_output("ping 8.8.8.8 -n 2", shell=True).decode("cp850")
                ip_config = subprocess.check_output("ipconfig /all", shell=True).decode("cp850")
                
                report_path = os.path.abspath("diagnostico_canivete.html")
                html_content = f"""
                <html><head><style>
                    body {{ background: #1a1a1a; color: white; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
                    .card {{ background: #2d2d2d; padding: 15px; border-radius: 10px; border-left: 5px solid #3b8ed0; margin-bottom: 20px; }}
                    pre {{ background: #000; color: #00ff00; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    h1 {{ color: #3b8ed0; }}
                </style></head><body>
                    <h1>Relatório de Diagnóstico Canivete v0.4.0</h1>
                    <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <div class='card'><h2>Análise de Gargalo (Ping 8.8.8.8)</h2><pre>{ping_google}</pre></div>
                    <div class='card'><h2>Configurações de IP Completas</h2><pre>{ip_config}</pre></div>
                </body></html>
                """
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                webbrowser.open(report_path)
                self.safe_log(f">> Relatório gerado: {report_path}\n")
            except Exception as e:
                self.safe_log(f">> Erro ao gerar relatório: {str(e)}\n")

        threading.Thread(target=task, daemon=True).start()

    def show_printer_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Suporte de Impressão", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Abrir Painel de Impressoras", command=lambda: subprocess.run("control printers", shell=True)).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Reiniciar Spooler", fg_color="orange", command=self.restart_spooler).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Fix Registro PrintNightmare", command=self.fix_printer_registry).pack(pady=10)

    def show_process_frame(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Conexões de Rede Ativas", font=("Arial", 20, "bold")).pack(pady=10)
        columns = ("Protocolo", "Local", "Remoto", "Estado", "PID")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)
        for col in columns: self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(self.main_frame, text="Atualizar Lista", command=self.update_netstat).pack(pady=10)
        self.update_netstat()

    def update_netstat(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        cmd = "netstat -ano" if platform.system() == "Windows" else "ss -tulpn"
        try:
            out = subprocess.check_output(cmd, shell=True).decode("cp850")
            for line in out.splitlines()[4:]:
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 4:
                    self.tree.insert("", "end", values=parts[:5])
        except Exception as e:
            self.safe_log(f">> Erro ao atualizar netstat: {e}\n")

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

    def show_system_frame(self):
        self.clear_main_frame()
        info = system_info()
        for key, value in info.items():
            ctk.CTkLabel(self.main_frame, text=f"{key}: {value}", font=("Arial", 16)).pack(pady=5)

    def run_sys_cmd(self, func):
        if not hasattr(self, 'console') or not self.console.winfo_exists():
             self.show_maintenance_frame()
        res = func()
        self.safe_log(f">> {res.get('stdout') or res.get('error') or 'Sucesso'}\n")

    def run_shell(self, cmd):
        if not is_admin():
            messagebox.showerror("Erro", "Esta ação requer privilégios de Administrador!")
            return
        threading.Thread(target=lambda: subprocess.run(cmd, shell=True), daemon=True).start()
        self.safe_log(f">> Comando enviado: {cmd}\n")

    def restart_spooler(self):
        self.run_shell("net stop spooler && net start spooler")
        messagebox.showinfo("Impressoras", "Serviço de Spooler reiniciado!")

    def clean_temp_action(self):
        import shutil, tempfile
        temp = tempfile.gettempdir()
        for item in os.listdir(temp):
            try:
                p = os.path.join(temp, item)
                if os.path.isfile(p): os.unlink(p)
                else: shutil.rmtree(p)
            except: continue
        self.safe_log(">> Limpeza de temporários concluída.\n")

    def fix_printer_registry(self):
        cmd = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f'
        self.run_shell(cmd)
        messagebox.showinfo("Registro", "Correção aplicada! Reinicie o PC.")

def launch_gui():
    app = CaniveteGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()