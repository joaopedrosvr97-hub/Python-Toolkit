
</p>

# 🔪 Canivete Suíço - Network Toolkit (v0.4.0)

<p align="center"> 
  <img src="https://img.shields.io/badge/Status-Ativo-32CD32?style=for-the-badge"> 
  <img src="https://img.shields.io/badge/Versão-0.4.0-blue?style=for-the-badge"> 
  <img src="https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python"> 
  <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux-lightgrey?style=for-the-badge"> 
  <img src="https://img.shields.io/badge/Licença-MIT-purple?style=for-the-badge"> 
</p>

O **Canivete Suíço** é uma suíte unificada de diagnóstico e manutenção para técnicos e sysadmins. Com uma interface moderna em **CustomTkinter**, o projeto automatiza desde a limpeza de cache DNS até reparos profundos de sistema (SFC/DISM).

---

## 📸 Preview do Projeto

<p align="center">
  <a href="https://github.com/joaopedrosvr97-hub/Canivete-Sui-o-Python-Toolkit">
    <img src="src/docs/interface.png" alt="Interface Principal" width="850" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
  <br>
  <i>Interface moderna v0.4.0 com suporte a Dark Mode.</i>
</p>

<table align="center" style="border: none;">
  <tr>
    <td align="center" style="border: none;">
      <a href="src/docs/config.png">
        <img src="src/docs/config.png" width="400px" alt="Configurações e Manutenção" style="border-radius: 8px; transition: transform .2s;"/>
      </a>
      <br><sub><b>Ferramentas de Manutenção OS</b></sub>
    </td>
    <td align="center" style="border: none;">
      <a href="src/docs/main_gui.png">
        <img src="src/docs/main_gui.png" width="400px" alt="Estrutura de Código" style="border-radius: 8px; transition: transform .2s;"/>
      </a>
      <br><sub><b>Arquitetura do Projeto (src-layout)</b></sub>
    </td>
  </tr>
</table>

---

## 🆕 Novidades da Versão 0.4.0

* **Interface Moderna:** Migração para `CustomTkinter` com navegação lateral dinâmica.
* **Reparo de Sistema:** Botões dedicados para comandos SFC, DISM e Limpeza de Temporários.
* **Gestão de Impressoras:** Reinício de Spooler e correção de erros de registro.
* **Monitoramento Real-time:** Dashboard de tráfego de rede integrado.

---

## 🚀 Como Instalar e Rodar

### Pré-requisitos
* **Python 3.9+**
* **Privilégios de Administrador** (necessário para funções de rede e sistema).

### Passo a Passo
```bash
# 1. Clone o repositório
git clone https://github.com/joaopedrosvr97-hub/Canivete-Sui-o-Python-Toolkit.git
cd Canivete-Suico-Network-Toolkit/Python-Toolkit/Python-Toolkit

# 2. Instale o pacote e dependências
pip install -e .

# 3. Execute a aplicação
canivete gui

