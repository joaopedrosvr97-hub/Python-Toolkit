# 🚀 Roadmap — Canivete Suíço Network Toolkit

**Versão Atual:** v0.4.0 (GUI Milestone)  
**Última Atualização:** 2026-02-05  
**Maintainer:** João Pedro (@joaopedrosvr97-hub)

---

## 🎯 Visão Estratégica
O objetivo é transformar o **Canivete Suíço** na principal suíte *open-source* de diagnóstico rápido para administradores de sistemas, unindo a facilidade de uma interface moderna à robustez de scripts de baixo nível.

---

## 📑 Ciclo de Lançamentos

### ✅ v0.4.0 — Refatoração e GUI (Concluído)
**Objetivo:** Migração de scripts soltos para um pacote Python estruturado com interface gráfica.
- [x] Implementação do padrão **src-layout** (PEP 517).
- [x] Interface moderna com **CustomTkinter** e suporte a Dark Mode.
- [x] Módulos de Manutenção OS (SFC, DISM, Spooler).
- [x] Monitor de Tráfego de rede em tempo real.
- [x] Sistema de logs modularizado.

---

### 🟡 v0.5.0 — Network Deep Scan (Curto Prazo)
**Prioridade:** Alta  
**Objetivo:** Expandir as capacidades de descoberta de rede e análise de segurança.
- [ ] **Port Scanner Multithreaded:** Varredura rápida de portas TCP/UDP comuns.
- [ ] **Service Detection:** Identificação básica de banners (HTTP, SSH, RDP).
- [ ] **Exportação Avançada:** Botão na GUI para gerar relatórios em PDF e CSV das tabelas de rede.
- [ ] **Tratamento de Exceções Global:** Sistema de pop-ups de erro para interações com o SO.

**DoD (Definition of Done):**
* Scan de 100 portas em um host local em menos de 5 segundos.
* Relatório PDF gerado com o logo do projeto e timestamp.

---

### 🔵 v0.6.0 — Automação e Notificações (Médio Prazo)
**Prioridade:** Média  
**Objetivo:** Permitir que a ferramenta monitore o sistema passivamente e emita alertas.
- [ ] **Webhooks/Alertas:** Integração para envio de alertas de "Host Down" via Telegram ou Discord.
- [ ] **Verificação de Integridade:** Monitoramento agendado de integridade de arquivos do sistema.
- [ ] **Dashboard de Performance:** Gráficos históricos de uso de CPU/RAM junto ao tráfego de rede.

---

### 🔷 v1.0.0 — Estabilização e Distribuição (Enterprise Ready)
**Prioridade:** Alta  
**Objetivo:** Lançamento da primeira versão oficial estável para uso corporativo.
- [ ] **CI/CD Pipeline:** Automação completa de testes e publicação no PyPI via GitHub Actions.
- [ ] **Executable Build:** Geração de executáveis `.exe` (Windows) e binários Linux via PyInstaller/Nuitka.
- [ ] **Assinatura Digital:** Implementação de checksums (SHA-256) para downloads seguros.
- [ ] **Documentação Multilíngue:** Tradução técnica para Inglês e Espanhol.

**DoD:**
* `pip install canivete-suico-toolkit` funcional e sem bugs de dependência.
* Binário `.exe` rodando sem falsos positivos em antivírus comuns.

---

### 🟩 Long Term — Cloud & Remote Management
**Prioridade:** Baixa  
**Objetivo:** Expandir o toolkit para gerenciamento remoto.
- [ ] **API REST Integrada:** Permitir consulta de status da máquina via rede.
- [ ] **Agent Mode:** Versão minimalista (sem GUI) para rodar como serviço/daemon em servidores.

---

## 🛠️ Kanban de Desenvolvimento

| Backlog (Ideias) | To Do (Próxima Sprint) | In Progress | Done (v0.4.0) |
| :--- | :--- | :--- | :--- |
| Módulo Whois/ASN | Port Scanner | Refino do README | Estrutura src/ |
| Interface Web | Exportação PDF | Fix pyproject.toml | CustomTkinter GUI |
| Alertas Slack | Scan ARP/ICMP | | Monitor de Tráfego |

---

## 🤝 Contribuição
Se você deseja acelerar qualquer item deste roadmap:
1. Abra uma **Issue** descrevendo qual item vai atacar.
2. Siga o padrão de **Conventional Commits** para manter o histórico limpo.
3. Certifique-se de que sua alteração não quebre o suporte multiplataforma (Win/Linux).

---
<p align="center">
  <i>"O Roadmap é um organismo vivo. Sugestões de novas ferramentas de rede são sempre bem-vindas via Pull Requests."</i>
</p>