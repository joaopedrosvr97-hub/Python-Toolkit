import json
import os
from datetime import datetime
from typing import Any, Dict

def save_to_json(data: Any, filename: str) -> str:
    """
    Guarda os dados num ficheiro JSON com timestamp.
    """
    # Garante que o nome termina em .json
    if not filename.endswith(".json"):
        filename += ".json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return os.path.abspath(filename)
    except Exception as e:
        return f"Erro ao exportar JSON: {e}"

def save_to_txt(data: Any, filename: str) -> str:
    """
    Guarda os dados num formato de texto simples.
    """
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO CANIVETE - {datetime.now()}\n")
            f.write("="*40 + "\n")
            if isinstance(data, dict):
                for k, v in data.items():
                    f.write(f"{k}: {v}\n")
            else:
                f.write(str(data))
        return os.path.abspath(filename)
    except Exception as e:
        return f"Erro ao exportar TXT: {e}"