#!/bin/bash

# sudo apt install inotify-tools

# Arquivos a serem monitorados
FILES=("app.py" "mcp.py" "request.py" "sidebar.py")

# Verifica se os arquivos existem
for file in "${FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "[ERRO] Arquivo $file não encontrado."
        exit 1
    fi
done

# Arquivo principal a executar (pode ser qualquer um dos dois)
MAIN_FILE="app.py"

# Inicia o processo Python
echo "[INFO] Iniciando $MAIN_FILE..."
python "$MAIN_FILE" &
PID=$!

# Loop de monitoramento
echo "[INFO] Monitorando alterações em: ${FILES[*]}"
while inotifywait -e modify "${FILES[@]}"; do
    echo "[INFO] Alteração detectada em um dos arquivos! Reiniciando..."
    kill $PID
    wait $PID 2>/dev/null
    python3 "$MAIN_FILE" &
    PID=$!
done
