# 🛠️ Troubleshooting – Solução de Problemas (v0.4.0)

Este documento centraliza as falhas comuns, diagnósticos e resoluções para garantir a estabilidade do **Canivete Suíço – Network Toolkit**.

---

## ❗ 1. Erros de Inicialização e Caminhos

### 🔹 Erro: *"ModuleNotFoundError: No module named 'canivete'"*
**Causa:** O Python não consegue localizar o pacote dentro da pasta `src` ou o pacote não foi instalado no ambiente atual.
**Solução:** Certifique-se de que você está na pasta que contém o arquivo `pyproject.toml` e execute:
```bash
pip install -e .