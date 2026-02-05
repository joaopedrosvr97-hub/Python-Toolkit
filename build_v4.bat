@echo off
title Build Canivete v0.4.0
echo [1/3] Limpando ambiente...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist "Canivete-v0.4.0.spec" del /q "Canivete-v0.4.0.spec"

echo [2/3] Compilando executavel v0.4.0...
:: O uso do --collect-all pode ser útil se você usar bibliotecas complexas, 
:: mas o --paths ja ajuda o script a enxergar a pasta core.
pyinstaller --noconfirm --onefile --windowed ^
 --add-data "src/docs;docs" ^
 --icon "src/docs/app_v4.ico" ^
 --name "Canivete-v0.4.0" ^
 --paths "src" ^
 src/canivete/gui.py

echo [3/3] Finalizado! Verifique a pasta 'dist'.
pause