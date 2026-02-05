🌐 Overview do Projeto - v0.4.0 (Enterprise Edition)
O Canivete Suíço Network Toolkit evoluiu de um conjunto de scripts para uma suíte modular de alta performance voltada à administração de sistemas e diagnóstico de infraestrutura de rede.

Desenvolvido inteiramente em Python 3.9+, o projeto combina o poder do baixo nível (Win32 API e Subprocessos) com a sofisticação da interface CustomTkinter, entregando uma ferramenta rápida, segura e visualmente intuitiva.

✨ Principais Diferenciais (v0.4.0)
Diferente de scripts básicos, o Canivete Suíço foca em Estabilidade e Governança:

GUI Engine: Dashboard moderno com navegação dinâmica e suporte a temas (Dark/Light Mode).

System Integrity: Módulos integrados para reparo de sistema (SFC, DISM) e otimização de performance.

Real-time Telemetry: Monitoramento de tráfego de rede (I/O) em tempo real com processamento assíncrono.

Modular Architecture: Implementação do padrão src-layout, isolando a lógica de negócio da camada visual.

Logging System: Auditoria automática de todas as operações críticas, armazenadas com carimbos de data e evento.

🛠️ Pilares Funcionais
O toolkit está dividido em quatro esferas operacionais principais:

1. Diagnóstico de Rede
Varreduras de sub-redes (CIDR), descoberta de hosts ativos e testes de conectividade avançados.

2. Manutenção de Infraestrutura
Gerenciamento de serviços de impressão (Print Spooler) e correção de falhas de registro (RPC/PrintNightmare).

3. Otimização de Sistema
Limpeza de caches profundos (Windows Update, Temp files) e ativação de perfis de alto desempenho via hardware.

4. Telemetria e Monitoramento
Visualização tabular de processos ativos, conexões de rede (netstat) e fluxo de banda por interface.

🏗️ Blueprint da Arquitetura
O projeto utiliza o padrão de Camadas de Software para garantir que o código seja testável e escalável:

Plaintext

src/canivete/
 ┣ 📂 core/          # Business Logic (Motores de rede, sistema e tráfego)
 ┣ 📂 docs/          # Static Assets (Imagens e recursos da interface)
 ┣ 📜 gui.py         # Presentation Layer (Visual e UX)
 ┣ 📜 cli.py         # Bridge Layer (Suporte a comandos legados)
 ┗ 📜 __main__.py    # Application Bootloader
👥 Público-Alvo
O toolkit foi desenhado para atender às demandas de:

Analistas de Infraestrutura: Automação de diagnósticos diários.

SysAdmins: Reparos rápidos de sistema e gestão de serviços.

Técnicos de Suporte: Ferramenta unificada para atendimento de campo.

Engenheiros de Software: Estudo de integração Python com APIs de sistema.

🚀 Roadmap e Evolução
O projeto está em fase ativa (Beta v0.4.0). As próximas etapas de desenvolvimento incluem:

Integração de Scan de Portas (Port Scanner) multithreaded.

Módulo de segurança para análise de integridade de arquivos.

Empacotamento via PyInstaller para distribuição como executável (.exe) independente.

<p align="center"> <b>Canivete Suíço Toolkit</b> — "Simples o suficiente para usuários, robusto o suficiente para profissionais." </p>