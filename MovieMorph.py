#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import glob
import time

# -------------------------------------------------------------------
# CONFIGURACIÓN (por defecto)
# -------------------------------------------------------------------

# 1. Carpeta base del usuario actual (ej. "C:\Users\pepito")
carpeta_base = os.path.expanduser("~")

# 2. Carpeta donde están las películas (ej. "C:\Users\pepito\Downloads\Movies")
CARPETA_PELICULAS = os.path.join(carpeta_base, "Downloads", "Movies")

# 3. Carpeta de destino (La puedes personalizar y poner una ubicación de red o una carpeta)
DESTINO = r"Z:\Peliculas"

# 4. Log en la carpeta de Movies
LOGPATH = os.path.join(CARPETA_PELICULAS, "MovieMorph.log")

# 5. Tamaño mínimo (300 MB)
TAMANIO_MINIMO = 300 * 1024 * 1024
# 1024 * 1024 no tiene nada que ver con la resolución de vídeo, sino que es una conversión de megabytes (MB) a bytes, ya que el sistema operativo gestiona los firechos en bytes

# 6. Extensiones de vídeo permitidas
EXTENSIONES_OK = [".mkv", ".mp4", ".avi"]

# 7. Patrones de archivos residuales (archivos que quedan después de descargar o descomprimir contenido, pero que no son necesarios para la película en sí)

PATRONES_RESIDUALES = ["*.rar", "*.zip", "*.7z", "*.part"]

# -------------------------------------------------------------------
def log(texto):
    """
    Registra un mensaje en consola y en MovieMorph.log
    """
    fecha = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    linea = f"{fecha} {texto}"
    print(linea)

    # Nos aseguramos de que la carpeta Movies exista
    os.makedirs(CARPETA_PELICULAS, exist_ok=True)

    # Guardamos en el log
    with open(LOGPATH, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def main():
    if len(sys.argv) < 2:
        log("[ERROR] No se recibió ningún archivo.")
        sys.exit(1)

    archivo_extraido = sys.argv[1]

    # 1. Validar existencia del archivo
    if not os.path.isfile(archivo_extraido):
        log(f"[ERROR] El archivo '{archivo_extraido}' no existe o no es un archivo.")
        sys.exit(1)

    # 2. Comprobar que viene de la carpeta Movies
    carpeta_archivo = os.path.dirname(archivo_extraido)
    if not carpeta_archivo.lower().startswith(CARPETA_PELICULAS.lower()):
        log(f"[IGNORADO] El archivo no viene de '{CARPETA_PELICULAS}': '{archivo_extraido}'")
        sys.exit(99)

    # 3. Validar extensión y tamaño
    extension_original = os.path.splitext(archivo_extraido)[1].lower()
    tamanio = os.path.getsize(archivo_extraido)

    if extension_original not in EXTENSIONES_OK:
        log(f"[IGNORADO] Extensión no permitida ({extension_original}): {archivo_extraido}")
        sys.exit(99)

    if tamanio < TAMANIO_MINIMO:
        mb = round(tamanio / (1024*1024), 2)
        log(f"[IGNORADO] Tamaño insuficiente: {mb} MB (< 300 MB): {archivo_extraido}")
        sys.exit(99)

    # 4. Renombrar con el nombre de la carpeta
    nombre_carpeta = os.path.basename(carpeta_archivo)  # p.ej. "MiPelicula (2024)"
    nombre_final   = nombre_carpeta + extension_original
    destino_final  = os.path.join(DESTINO, nombre_final)

    # Crear la carpeta destino si no existe
    os.makedirs(DESTINO, exist_ok=True)

    # Si ya existe en destino, se elimina para sobrescribir
    if os.path.exists(destino_final):
        try:
            os.remove(destino_final)
        except Exception as e:
            log(f"[ERROR] No se pudo borrar '{destino_final}': {e}")
            sys.exit(2)

    # 5. Mover (renombrar)
    try:
        shutil.move(archivo_extraido, destino_final)
        log(f"[OK] Película procesada: '{nombre_final}' movida a '{destino_final}'")
    except Exception as e:
        log(f"[ERROR] No se pudo mover '{archivo_extraido}' a '{destino_final}': {e}")
        sys.exit(2)

    # 6. Borrar archivos residuales
    for patron in PATRONES_RESIDUALES:
        ruta_patron = os.path.join(carpeta_archivo, patron)
        for f_residual in glob.glob(ruta_patron):
            try:
                os.remove(f_residual)
            except:
                pass

    # 7. Borrar la carpeta si no es la base
    if carpeta_archivo.lower() != CARPETA_PELICULAS.lower():
        try:
            shutil.rmtree(carpeta_archivo)
            log(f"[OK] Carpeta '{carpeta_archivo}' eliminada tras procesar correctamente.")
        except Exception as e:
            log(f"[WARN] No se pudo eliminar '{carpeta_archivo}': {e}")

    # 8. Exit code 0 => procesado con éxito
    sys.exit(0)


if __name__ == "__main__":
    main()
