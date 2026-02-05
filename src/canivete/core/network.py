import subprocess
import platform
import ipaddress
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

from canivete.core.utils import setup_logger

logger = setup_logger()


# ==========================================================
# PING / SCAN (REFATORADO V0.3.0)
# ==========================================================

def ping_host(host: str) -> bool:
    """
    Executa ping simples no host.
    Retorna True se o host responder, False caso contrário.
    """
    system_name = platform.system().lower()
    # No Windows é '-n', no Linux/Mac é '-c'
    param = "-n" if system_name == "windows" else "-c"
    
    # Timeout de 1 segundo para não travar o scan paralelo
    timeout_param = "-w" if system_name == "windows" else "-W"
    
    command = ["ping", param, "1", timeout_param, "1000", host] if system_name == "windows" else ["ping", param, "1", timeout_param, "1", host]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def expand_target(target: str) -> List[str]:
    """
    Expande o alvo:
    - IP único → [IP]
    - CIDR → lista de IPs utilizáveis
    """
    try:
        if "/" in target:
            network = ipaddress.ip_network(target, strict=False)
            return [str(ip) for ip in network.hosts()]
        else:
            return [target]
    except ValueError as exc:
        logger.error(f"Alvo inválido: {target}")
        raise ValueError(f"Alvo inválido: {target}") from exc


def scan_network(target: str, max_workers: int = 50) -> Dict[str, bool]:
    """
    Executa scan de rede paralelo via ping (Passo 8 Refatorado).
    Retorna dict no formato: { "host": True | False }
    """
    logger.info(f"Iniciando scan paralelo em: {target}")

    hosts = expand_target(target)
    results: Dict[str, bool] = {}

    # Image of parallel processing vs sequential
    # Utilizamos ThreadPoolExecutor para disparar pings simultâneos
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Mapeia cada host para uma tarefa de ping
        future_to_host = {executor.submit(ping_host, host): host for host in hosts}
        
        for future in future_to_host:
            host = future_to_host[future]
            try:
                results[host] = future.result()
            except Exception as exc:
                logger.error(f"Erro ao escanear {host}: {exc}")
                results[host] = False

    return results


# ==========================================================
# INFORMAÇÕES DE REDE
# ==========================================================

def network_info() -> Dict[str, str]:
    """
    Retorna informações gerais de rede do sistema (Passo 9).
    """
    system = platform.system().lower()
    info: Dict[str, str] = {}

    try:
        if system == "windows":
            output = subprocess.check_output(
                ["ipconfig", "/all"],
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
        else:
            output = subprocess.check_output(
                ["ip", "a"],
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

        info["raw"] = output

    except Exception as exc:
        info["error"] = str(exc)

    return info


# ==========================================================
# COMANDOS DE MANUTENÇÃO (NETFIX - PASSO 11/12)
# ==========================================================

def run_network_command(command: List[str]) -> Dict[str, str]:
    """
    Executa comando de rede de forma segura.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc)
        }


def flush_dns() -> Dict[str, str]:
    """Limpa cache DNS."""
    system = platform.system().lower()
    if system == "windows":
        return run_network_command(["ipconfig", "/flushdns"])
    if system == "linux":
        # Tenta systemd-resolve ou resolvectl dependendo da distro
        return run_network_command(["resolvectl", "flush-caches"])
    
    return {"success": False, "error": "Sistema operacional não suportado"}


def ip_release() -> Dict[str, str]:
    """Libera IP (Windows)."""
    if platform.system().lower() != "windows":
        return {"success": False, "error": "Comando disponível apenas no Windows"}
    return run_network_command(["ipconfig", "/release"])


def ip_renew() -> Dict[str, str]:
    """Renova IP (Windows)."""
    if platform.system().lower() != "windows":
        return {"success": False, "error": "Comando disponível apenas no Windows"}
    return run_network_command(["ipconfig", "/renew"])


def winsock_reset() -> Dict[str, str]:
    """Reseta Winsock (Windows)."""
    if platform.system().lower() != "windows":
        return {"success": False, "error": "Comando disponível apenas no Windows"}
    return run_network_command(["netsh", "winsock", "reset"])