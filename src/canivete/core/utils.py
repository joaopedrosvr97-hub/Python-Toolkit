def banner():
    return "=== Canivete ==="
import logging

def setup_logger(name: str = "canivete") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
def confirm_action(message: str) -> bool:
    """
    Solicita confirmação explícita do usuário.
    Retorna True se confirmado, False caso contrário.
    """
    try:
        response = input(f"{message} [s/N]: ").strip().lower()
        return response in ("s", "sim", "y", "yes")
    except KeyboardInterrupt:
        print("\n[AÇÃO CANCELADA]")
        return False


