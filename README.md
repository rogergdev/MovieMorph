![MovieMorph](https://github.com/user-attachments/assets/682da312-ea00-40e9-85bd-c17cb0f7bb1a)

# MovieMorph agente renombrador y gestor de directorios

**MovieMorph** es un script bash diseñado para organizar automáticamente archivos de vídeo descargados. Su objetivo principal es mover archivos de vídeo desde subcarpetas a la carpeta principal, eliminar archivos residuales y subcarpetas vacías, dejando la carpeta limpia y organizada.

---

## **Características**

1. **Procesamiento Automático:**
   - Recorre todas las subcarpetas para buscar archivos de vídeo.
   - Mueve los archivos a la carpeta principal.

2. **Limpieza de Residuos:**
   - Elimina archivos no deseados como `.rar`, `.zip`, `.txt`, etc.
   - Borra subcarpetas vacías después de procesar los archivos.

3. **Compatibilidad con JDownloader:**
   - Puede configurarse para ejecutarse automáticamente al finalizar una descarga.

4. **Registro de Operaciones:**
   - Genera un log detallado en `/mnt/eter/FilePhantom/MovieMorph.log` con las acciones realizadas.

---

## **Requisitos del Sistema**

- **Sistema Operativo:** Linux
- **Dependencias:**
  - Bash
  - Comando `find`

---

## **Instalación**

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tuusuario/MovieMorph.git
   ```

2. **Copia el script a la ubicación deseada:**
   ```bash
   cp MovieMorph.sh /mnt/eter/FilePhantom/
   ```

3. **Da permisos de ejecución al script:**
   ```bash
   chmod +x /mnt/eter/FilePhantom/MovieMorph.sh
   ```

4. **Crea el archivo de log:**
   ```bash
   touch /mnt/eter/FilePhantom/MovieMorph.log
   chmod 666 /mnt/eter/FilePhantom/MovieMorph.log
   ```

---

## **Uso Manual**

Ejecuta el script con la carpeta que deseas procesar como argumento:

```bash
/mnt/eter/FilePhantom/MovieMorph.sh "/ruta/a/la/carpeta"
```

### **Ejemplo:**

```bash
/mnt/eter/FilePhantom/MovieMorph.sh "/mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)"
```

---

## **Integración con JDownloader**

### **Configuración del EventScripter**

1. Abre **JDownloader**.
2. Ve a **Ajustes** > **Extensiones** > **EventScripter**.
3. Haz clic en **Configurar**.
4. Crea un nuevo evento:
   - **Nombre del Evento:** `Ejecutar MovieMorph`
   - **Trigger (Disparador):** `Un archivo/carpeta ha terminado de descargarse`.
5. Usa el siguiente script:

```javascript
// Ejecuta MovieMorph.sh después de finalizar una descarga

// Ruta del script
var scriptPath = "/mnt/eter/FilePhantom/MovieMorph.sh";

// Ruta de la carpeta donde se guardó la descarga
var path = package.getDownloadFolder();

// Ejecutar el script en bash
if (isLinux()) {
    callAsync(function(exitCode) {
        if (exitCode === 0) {
            log("Script ejecutado correctamente: " + scriptPath);
        } else {
            log("Error ejecutando el script: " + scriptPath);
        }
    }, "/bin/bash", scriptPath, path);
} else {
    log("Este script solo funciona en sistemas Linux.");
}
```

### **Verificación de Integración**
1. Descarga algo en JDownloader.
2. Verifica los logs de JDownloader para asegurarte de que el script se ejecutó correctamente.
3. Confirma que los archivos se organizaron en las carpetas correspondientes.

---

## **Estructura del Log**

El archivo `/mnt/eter/FilePhantom/MovieMorph.log` contiene un registro detallado de las acciones realizadas. Ejemplo:

```
[2025-01-20 12:00:00] [PROCESANDO] Subcarpeta: /mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)/050125_11
[2025-01-20 12:00:01] [OK] Archivo movido: '/mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)/050125_11/El Señor De Los Anillos.mkv' -> '/mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)/El Señor De Los Anillos.mkv'
[2025-01-20 12:00:02] [LIMPIEZA] Archivos residuales eliminados: *.rar en /mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)
[2025-01-20 12:00:03] [COMPLETADO] Procesamiento finalizado para '/mnt/eter/peliculasanimacion/El señor de los anillos; La guerra de los Rohirrim (2024)'.
```

---
## Licencia

Este proyecto usa la [Licencia Apache 2.0](LICENSE).
