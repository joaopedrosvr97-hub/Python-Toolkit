🔪 Canivete Suíço - Network Toolkit (v0.4.0)
<p align="center"> <img src="https://img.shields.io/badge/Status-Ativo-32CD32?style=for-the-badge"> <img src="https://img.shields.io/badge/Versão-0.4.0-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux-lightgrey?style=for-the-badge"> <img src="https://img.shields.io/badge/Licença-MIT-purple?style=for-the-badge"> </p>

Uma ferramenta de administração de sistemas e redes multiplataforma, desenvolvida em Python com a moderna interface CustomTkinter. O projeto centraliza funções essenciais de diagnóstico de rede, manutenção de sistema e segurança em uma interface intuitiva e profissional.

⚠️ Requisitos e Privilégios
Python 3.9 ou superior.

Privilégios de Administrador: A maioria das ações (SFC, DISM, Spooler, Reset de Rede) exige execução como Administrador (Windows) ou Root (Linux).

🚀 Como Instalar e Rodar
Agora o projeto utiliza o padrão de empacotamento moderno do Python.

1. Clonar o Repositório
Bash

HEAD
git clone https://github.com/joaopedrosvr97-hub/Python-Toolkit.git
cd canivete-suico-toolkit
2. Instalar Dependências (Opcional)
A única dependência externa real para rodar é o pyinstaller (se quiser gerar o .exe). Para rodar o código diretamente, não há módulos de terceiros:
=======
git clone https://github.com/joaopedrosvr97-hub/Canivete-Sui-o-Python-Toolkit.git
cd Canivete-Suico-Network-Toolkit/Python-Toolkit/Python-Toolkit
2. Instalar em Modo Editável
Isso instalará automaticamente todas as dependências necessárias (customtkinter, psutil):
(feat: upgrade to v0.4.0 - integrate maintenance tools and modern gui)

Bash

pip install -e .
3. Iniciar a Aplicação
Você pode iniciar a interface gráfica diretamente pelo comando registrado no seu sistema:

Bash

canivete-gui
Ou via módulo: python -m canivete.gui

🛠️ Funcionalidades Integradas (v0.4.0)
🌐 Redes e Tráfego
Network Scanner: Varredura de sub-redes (CIDR) para identificar hosts ativos.

Monitor de Tráfego: Visualização em tempo real de Upload/Download (KB/s).

Manutenção de Rede: Flush DNS, Reset de Winsock, IP Release/Renew.

⚙️ Manutenção de Sistema
Reparos Críticos: Atalhos para SFC /Scannow e DISM Restore Health.

Limpeza Automática: Exclusão de arquivos temporários e caches do Windows Update.

Otimização: Ativação de perfis de alto desempenho via powercfg.

🖨️ Suporte a Impressoras
Fix PrintNightmare: Correções de registro para erros de compartilhamento (RPC).

Gestão de Spooler: Reinício rápido do serviço de impressão.

📈 Visualização de Dados
Tabelas Dinâmicas: Lista de processos e conexões de rede (netstat) exibidas em grades organizadas.

Console Integrado: Saída de texto em tempo real com suporte a grandes volumes de dados.

📂 Estrutura do Projeto
Plaintext

src/canivete/
├── core/     # Lógica de rede, sistema e tráfego
├── gui.py    # Interface gráfica (CustomTkinter)
├── cli.py    # Interface de linha de comando
└── __main__.py
🤝 Contribuição
Faça um Fork do projeto.

Crie uma Branch para sua feature (git checkout -b feature/NovaFeature).

Dê um Commit nas suas mudanças (git commit -m 'feat: Adiciona nova funcionalidade').

Faça o Push da Branch (git push origin feature/NovaFeature).

Abra um Pull Request.

⚖️ Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

Dicas para o Commit Final:
Verifique o Link do Repositório: No README acima, substitua os links se o nome da pasta no GitHub for diferente.

Conventional Commits: Ao subir esse README junto com as outras mudanças, use: git commit -m "docs: update README to v0.4.0 and reflect new project structure"