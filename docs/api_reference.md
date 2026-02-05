# 📚 API Reference – Canivete Suíço (v0.4.0)

Este documento detalha as funções principais e os módulos do **Canivete Engine**. Desenvolvedores podem utilizar esses módulos de forma independente da interface gráfica.

---

## 🌐 Módulo: `canivete.core.network`

Responsável pela extração de metadados de adaptadores e diagnósticos de conectividade.

### `get_network_info()`
* **Descrição:** Coleta detalhes técnicos de todos os adaptadores ativos.
* **Retorno:** `dict` contendo IP, Gateway, Máscara e DNS.
```python
{
  "hostname": "workstation-01",
  "interfaces": [...],
  "public_ip": "201.x.x.x"
}
reset_network_stack()
Descrição: Executa o flush de DNS e reset de Winsock/TCP-IP.

Requisito: Privilégios de Administrador.

⚙️ Módulo: canivete.core.system
Interface de comunicação com o Sistema Operacional para tarefas de manutenção.

run_integrity_check(mode='sfc')
Parâmetros: mode (str): 'sfc' ou 'dism'.

Descrição: Inicia processos de reparo de imagem do Windows.

Retorno: str (Output do terminal ou log de sucesso/erro).

fix_print_spooler()
Descrição: Reinicia o serviço de Spooler e limpa a fila de arquivos temporários de impressão.

📊 Módulo: canivete.core.traffic
Motor de telemetria assíncrona para monitoramento de banda.

get_traffic_stats()
Descrição: Captura o total de bytes enviados e recebidos desde a última chamada.

Retorno: tuple (sent_bytes, recv_bytes).

calculate_speed(interval=1)
Descrição: Calcula a taxa de transferência em KB/s.

🔎 Módulo: canivete.core.export
Gerencia a persistência de dados e geração de relatórios.

save_to_log(data, module_name)
Parâmetros: * data (str/dict): Conteúdo a ser gravado.

module_name (str): Nome do módulo (ex: 'scanner').

Descrição: Grava arquivos em logs/{module_name}/{timestamp}.log.

🎨 Módulo: canivete.gui
Camada de apresentação (CustomTkinter).

class CaniveteGUI(customtkinter.CTk)
Descrição: Classe principal que gerencia a janela, o loop de eventos e a renderização dos módulos visuais.

Método switch_page(page_name): Alterna entre as abas do dashboard lateral.

🧪 Exemplo de Uso Interno (Engine Only)
Se desejar usar apenas a lógica de rede sem abrir a janela:

Python

from canivete.core.network import get_network_info

data = get_network_info()
print(f"Seu IP Interno é: {data['ip']}")
[!NOTE] Esta API é interna e está sujeita a alterações durante o ciclo beta da v0.4.x.