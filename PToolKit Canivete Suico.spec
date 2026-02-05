# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Configuração de inclusão de arquivos estáticos (Imagens/Ícones)
# O PyInstaller precisa saber onde estão os assets da sua v0.4.0
added_files = [
    ('src/canivete/docs/*', 'canivete/docs'), # Inclui imagens da interface
]

a = Analysis(
    ['src/canivete/gui.py'],              # Novo ponto de entrada (Interface Gráfica)
    pathex=[],
    binaries=[],
    datas=added_files,                   # Adiciona os assets configurados acima
    hiddenimports=['customtkinter'],      # Garante a inclusão do framework visual
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Canivete Suico Toolkit',        # Nome final do seu .exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                            # Comprime o executável
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                       # Define como FALSE para não abrir o CMD
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/canivete/docs/icon.ico'    # Caminho opcional para o ícone do .exe
)