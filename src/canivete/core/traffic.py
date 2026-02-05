import psutil
import time
from typing import Dict

def get_network_usage() -> Dict[str, int]:
    """
    Obtém o total de bytes enviados e recebidos desde o boot.
    Utiliza psutil.net_io_counters() para acessar os dados da interface.
    """
    stats = psutil.net_io_counters()
    return {
        "bytes_sent": stats.bytes_sent,
        "bytes_recv": stats.bytes_recv,
        "packets_sent": stats.packets_sent,
        "packets_recv": stats.packets_recv
    }

def monitor_traffic(interval: int = 1) -> Dict[str, float]:
    """
    Calcula a velocidade atual de download e upload em KB/s.
    Realiza duas medições com um intervalo de tempo entre elas.
    """
    # Primeira medição
    initial = get_network_usage()
    time.sleep(interval)
    # Segunda medição
    final = get_network_usage()
    
    # Cálculo da diferença (Delta) convertido para Kilobytes
    delta_sent = (final["bytes_sent"] - initial["bytes_sent"]) / 1024
    delta_recv = (final["bytes_recv"] - initial["bytes_recv"]) / 1024
    
    return {
        "upload_kb_s": round(delta_sent / interval, 2),
        "download_kb_s": round(delta_recv / interval, 2)
    }