import platform
import sys
import os
import ctypes
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