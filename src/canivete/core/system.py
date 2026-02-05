import platform
import sys
import os
import ctypes
import subprocess
from typing import Dict

def is_admin() -> bool:
    """Verifica se o usuário tem privilégios de administrador (Windows/Linux)."""
    system = platform.system()
    try:
        if system == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # os.geteuid() não existe no Windows, por isso o try/except ou check de SO
            return os.geteuid() == 0
    except Exception:
        return False

def system_info() -> Dict[str, str]:
    """Retorna informações básicas do sistema para o comando 'system'."""
    return {
        "Sistema": platform.system(),
        "Versão": platform.version(),
        "Arquitetura": platform.machine(),
        "Python": platform.python_version(),
    }

def doctor_info() -> Dict[str, str]:
    """Informações detalhadas para diagnóstico do toolkit."""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Python": sys.version.split()[0],
        "Admin": str(is_admin()),
        "Executable": sys.executable,
        "CWD": os.getcwd(),
    }

def run_windows_repair(command_type: str) -> str:
    """
    Executa comandos de reparo do Windows (SFC ou DISM).
    Tipos: 'sfc', 'dism_check', 'dism_scan', 'dism_restore'
    """
    if platform.system() != "Windows":
        return "Operação abortada: Este módulo requer Microsoft Windows."

    if not is_admin():
        return "Erro: Privilégios de Administrador são necessários para reparos de sistema."

    # Mapeamento de comandos Enterprise
    commands = {
        "sfc": ["sfc", "/scannow"],
        "dism_check": ["dism", "/online", "/cleanup-image", "/checkhealth"],
        "dism_scan": ["dism", "/online", "/cleanup-image", "/scanhealth"],
        "dism_restore": ["dism", "/online", "/cleanup-image", "/restorehealth"]
    }

    cmd = commands.get(command_type)
    if not cmd:
        return "Erro: Comando de manutenção desconhecido."

    try:
        # Execução via subprocess com shell=True para comandos nativos do sistema
        process = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if process.returncode == 0:
            return f"Sucesso:\n{process.stdout}"
        else:
            return f"O comando retornou um aviso ou erro:\n{process.stderr if process.stderr else process.stdout}"
    except Exception as e:
        return f"Falha crítica na execução do subprocesso: {str(e)}"