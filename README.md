![MovieMorph](https://github.com/user-attachments/assets/682da312-ea00-40e9-85bd-c17cb0f7bb1a)

# MovieMorph

**MovieMorph** es un sistema de postprocesado automático para películas descargadas en Windows.  
Puede integrarse con **JDownloader** (Event Scripter) o ejecutarse manualmente.

## Características

- **Renombra** los archivos con el nombre de la carpeta.
- **Admite** extensiones `.mkv`, `.mp4`, `.avi`.
- **Verifica** que ocupen al menos **300 MB**.
- **Mueve** el archivo a `Z:\Peliculas` (personalizable).
- **Sobrescribe** si ya existe un archivo con el mismo nombre en destino.
- **Elimina** la carpeta de la película si se procesa correctamente.
- **Registra** acciones en un log (`MovieMorph.log`) dentro de la carpeta `Movies`.

## Requisitos

- **Python 3** instalado en Windows y accesible como `python` en el path.
- (Opcional) Puedes instalar librerías como **`colorama`** y **`tqdm`** si quieres usar barras de progreso y colores (no incluidas por defecto).

## Instalación

1. Clona el repositorio o descarga el código fuente.
2. Crea una carpeta para los scripts, por ejemplo, `C:\scripts\MovieMorph`.
3. Pon los archivos `MovieMorph.py` y `MovieMorph_run_all.cmd` en esa carpeta.
4. Instala y agrega Python al path de tu sistema si no lo tienes instalado.

## Uso

### Postprocesado manual
Ejecuta el siguiente comando en la terminal:
```cmd
python "C:\scripts\MovieMorph\MovieMorph.py" "%USERPROFILE%\Downloads\Movies\CarpetaDePelicula\archivo.mkv"
```

### Postprocesado masivo
Ejecuta el script `MovieMorph_run_all.cmd` para procesar todos los archivos en `Downloads\Movies`:
```cmd
C:\scripts\MovieMorph_run_all.cmd
```

### Integración con JDownloader (Event Scripter)

1. Abre **JDownloader** > **Ajustes** > **Extensiones** > **Event Scripter**.
2. Crea un **nuevo script** (JavaScript) con el **Trigger** “Extractor de Archivos Finalizado”:
   ```javascript
   if (archive) {
       var extractedFiles = archive.getExtractedFiles();
       if (extractedFiles && extractedFiles.length > 0) {
           var filePath = extractedFiles[0];
           var pyScript = "C:\\scripts\\MovieMorph\\MovieMorph.py";
           callSync("python.exe", pyScript, filePath);
       }
   }
   ```

Este script llamará automáticamente a `MovieMorph.py` cada vez que se extraiga un archivo en JDownloader.

## Configuración personalizada

Puedes personalizar las rutas en `MovieMorph.py`:

- **Carpeta de destino**:
  Cambia la variable `DESTINO` para mover las películas a otra ruta.
  ```python
  DESTINO = r"D:\PeliculasOrganizadas"
  ```

- **Tamaño mínimo**:
  Modifica `TAMANIO_MINIMO` para aceptar archivos de menor o mayor tamaño (en bytes).
  ```python
  TAMANIO_MINIMO = 500 * 1024 * 1024  # 500 MB
  ```

- **Extensiones permitidas**:
  Agrega más extensiones a `EXTENSIONES_OK`.
  ```python
  EXTENSIONES_OK = [".mkv", ".mp4", ".avi", ".mov"]
  ```

## Licencia

Este proyecto usa la [Licencia Apache 2.0](LICENSE).
