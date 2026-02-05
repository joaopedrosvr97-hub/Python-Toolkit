import argparse
import platform
import sys
import time

from canivete.core.network import (
    scan_network,
    network_info,
    flush_dns,
    ip_release,
    ip_renew,
    winsock_reset,
)
from canivete.core.system import system_info, is_admin
from canivete.core.traffic import monitor_traffic  
from canivete.core.utils import confirm_action


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="canivete",
        description="Canivete Suíço Network Toolkit"
    )

    subparsers = parser.add_subparsers(
        title="comandos",
        dest="command",
        required=True
    )

    # ---------- Configuração dos Subparsers ----------
    
    # GUI (Novo comando para abrir a interface gráfica)
    subparsers.add_parser("gui", help="Abre a interface gráfica (Dashboard)")

    # SCAN 
    scan_parser = subparsers.add_parser("scan", help="Executa scan de rede paralelo")
    scan_parser.add_argument("target", help="IP ou CIDR (ex: 192.168.1.0/24)")
    scan_parser.add_argument("--output", "-o", help="Caminho do arquivo para exportar (ex: resultado.json)")

    subparsers.add_parser("netinfo", help="Exibe informações de rede detalhadas")
    subparsers.add_parser("traffic", help="Monitora tráfego de rede em tempo real")
    subparsers.add_parser("flushdns", help="Limpa o cache DNS (Windows/Linux)")
    subparsers.add_parser("release", help="Libera o IP atual (Windows)")
    subparsers.add_parser("renew", help="Renova o IP atual (Windows)")
    subparsers.add_parser("winsock-reset", help="Reseta o Winsock (Windows)")
    subparsers.add_parser("system", help="Mostra informações de hardware e OS")
    subparsers.add_parser("info", help="Exibe versão e créditos")

    args = parser.parse_args()

    print("--- Canivete Suíço Network Toolkit ---")

    try:
        # -------- GUI (Passo Front-end) --------
        if args.command == "gui":
            try:
                from canivete.gui import launch_gui
                print("[GUI] Iniciando interface gráfica...")
                launch_gui()
            except ImportError:
                print("[ERRO] Biblioteca 'customtkinter' não encontrada.")
                print("Por favor, instale com: pip install customtkinter")
                return 1

        # -------- SCAN --------
        elif args.command == "scan":
            print(f"[SCAN] Analisando {args.target}...")
            results = scan_network(args.target)
            
            for host, status in results.items():
                print(f"  > {host}: {'ONLINE' if status else 'OFFLINE'}")
            
            if args.output:
                from canivete.core.export import save_to_json
                path = save_to_json(results, args.output)
                print(f"\n[EXPORT] Resultados salvos em: {path}")

        # -------- NETINFO --------
        elif args.command == "netinfo":
            data = network_info()
            print("[NETINFO] Dados da interface:")
            print(data.get("raw", "Erro ao obter dados de rede."))

        # -------- TRAFFIC --------
        elif args.command == "traffic":
            print("[TRAFFIC] Monitorando tráfego. Pressione Ctrl+C para parar.")
            try:
                while True:
                    stats = monitor_traffic(interval=1)
                    output = f"  > DOWNLOAD: {stats['download_kb_s']} KB/s | UPLOAD: {stats['upload_kb_s']} KB/s"
                    print(output.ljust(50), end="\r")
            except KeyboardInterrupt:
                print("\n[TRAFFIC] Monitoramento finalizado pelo usuário.")

        # -------- FLUSHDNS --------
        elif args.command == "flushdns":
            if not is_admin():
                print("[ERRO] Requer privilégios de administrador.")
                return 1

            if confirm_action("Deseja realmente limpar o cache DNS?"):
                result = flush_dns()
                if result.get("success"):
                    print("[FLUSHDNS] Cache DNS limpo com sucesso.")
                else:
                    print(f"[FLUSHDNS] Erro: {result.get('error')}")

        # -------- RELEASE --------
        elif args.command == "release":
            if platform.system().lower() != "windows":
                print("[ERRO] Comando exclusivo para Windows.")
                return 1
            if confirm_action("Deseja liberar o IP atual?"):
                result = ip_release()
                print("[RELEASE] Sucesso" if result.get("success") else "[RELEASE] Erro")

        # -------- RENEW --------
        elif args.command == "renew":
            if platform.system().lower() != "windows":
                print("[ERRO] Comando exclusivo para Windows.")
                return 1
            if confirm_action("Deseja renovar o IP agora?"):
                result = ip_renew()
                print("[RENEW] Sucesso" if result.get("success") else "[RENEW] Erro")

        # -------- WINSOCK RESET --------
        elif args.command == "winsock-reset":
            if not is_admin():
                print("[ERRO] Requer privilégios de administrador.")
                return 1
            if confirm_action("Deseja resetar o Winsock? (Requer reinicialização)"):
                result = winsock_reset()
                if result.get("success"):
                    print("[WINSOCK] Sucesso. Por favor, reinicie o computador.")
                else:
                    print(f"[WINSOCK] Erro: {result.get('error')}")

        # -------- SYSTEM --------
        elif args.command == "system":
            info = system_info()
            print("[SYSTEM] Status do Sistema:")
            for key, value in info.items():
                print(f"  {key}: {value}")

        # -------- INFO --------
        elif args.command == "info":
            print("Versão: 0.3.0 (Fase de Refatoração)")
            print("Autor: João Pedro")
            print("Módulos Ativos: Network, System, Traffic, Utils, Export, GUI")

    except KeyboardInterrupt:
        print("\n[ABORTADO] Operação cancelada pelo usuário.")
        return 130
    except Exception as exc:
        print(f"[ERRO FATAL] {exc}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())