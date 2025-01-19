#!/bin/bash

# -------------------------------------------------------------------
# CONFIGURACIÓN
# -------------------------------------------------------------------

# Extensiones de vídeo permitidas
EXTENSIONES_OK=("mkv" "mp4" "avi")

# Patrones de archivos residuales
PATRONES_RESIDUALES=("*.rar" "*.zip" "*.7z" "*.part" "*.txt" "*.nfo")

# Ruta del archivo de log
LOGFILE="/mnt/eter/FilePhantom/MovieMorph.log"

# -------------------------------------------------------------------
# FUNCIONES
# -------------------------------------------------------------------

log() {
    # Registra mensajes en el archivo de log y en consola
    local mensaje="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$mensaje" | tee -a "$LOGFILE"
}

mover_archivo() {
    local archivo="$1"
    local carpeta_destino="$2"

    local nombre_archivo
    nombre_archivo=$(basename "$archivo")

    local nuevo_path="${carpeta_destino}/${nombre_archivo}"

    # Mover el archivo al directorio principal
    if mv "$archivo" "$nuevo_path"; then
        log "[OK] Archivo movido: '$archivo' -> '$nuevo_path'"
    else
        log "[ERROR] No se pudo mover '$archivo' -> '$nuevo_path'"
    fi
}

limpiar_residuales() {
    # Elimina archivos residuales y carpetas vacías en la carpeta especificada
    local carpeta="$1"
    for patron in "${PATRONES_RESIDUALES[@]}"; do
        find "$carpeta" -type f -name "$patron" -exec rm -f {} \;
        log "[LIMPIEZA] Archivos residuales eliminados: $patron en $carpeta"
    done

    # Eliminar subcarpetas vacías
    find "$carpeta" -type d -empty -delete
    log "[LIMPIEZA] Subcarpetas vacías eliminadas en $carpeta"
}

procesar_carpeta() {
    local carpeta="$1"

    # Validar si la carpeta existe
    if [[ ! -d "$carpeta" ]]; then
        log "[ERROR] La carpeta '$carpeta' no existe o no es válida."
        return 1
    fi

    # Buscar subcarpetas
    local subcarpetas=()
    while IFS= read -r -d $'\0' subcarpeta; do
        subcarpetas+=("$subcarpeta")
    done < <(find "$carpeta" -mindepth 1 -type d -print0)

    # Procesar cada subcarpeta
    for subcarpeta in "${subcarpetas[@]}"; do
        log "[PROCESANDO] Subcarpeta: $subcarpeta"

        # Buscar archivos de vídeo en la subcarpeta
        while IFS= read -r -d $'\0' archivo; do
            mover_archivo "$archivo" "$carpeta"
        done < <(find "$subcarpeta" -type f \( -name "*.mkv" -o -name "*.mp4" -o -name "*.avi" \) -print0)
    done

    # Limpiar residuales y subcarpetas vacías
    limpiar_residuales "$carpeta"
}

# -------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------

if [[ $# -lt 1 ]]; then
    log "[ERROR] No se proporcionó ninguna carpeta para procesar."
    exit 1
fi

carpeta_procesada="$1"

# Procesar la carpeta especificada
procesar_carpeta "$carpeta_procesada"

log "[COMPLETADO] Procesamiento finalizado para '$carpeta_procesada'."
