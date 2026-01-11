# Guía de Construcción del Paquete DEB

Esta guía explica cómo construir el paquete `.deb` de Keyflow para distribución en sistemas Linux basados en Debian/Ubuntu.

## Requisitos

- Sistema Debian/Ubuntu o derivado
- `dpkg-deb` (generalmente pre-instalado)
- Permisos de sudo para instalar el paquete después de construirlo

## Construcción Automática

El método más simple es usar el script automatizado:

```bash
# Hacer el script ejecutable (solo la primera vez)
chmod +x build-deb.sh

# Construir el paquete
./build-deb.sh
```

El script realizará automáticamente:
1. Limpieza de construcciones previas
2. Creación de la estructura de directorios requerida
3. Copia de archivos de la aplicación
4. Generación de metadatos DEBIAN
5. Construcción del paquete `.deb`

## Resultado

Al finalizar, se generará el archivo:
```
keyflow_1.0.0_all.deb
```

## Instalación

```bash
sudo dpkg -i keyflow_1.0.0_all.deb
sudo apt-get install -f  # Instala dependencias faltantes
```

## Estructura del Paquete

El paquete instalará los archivos en las siguientes ubicaciones:

```
/opt/keyflow/                    # Código fuente de la aplicación
├── main.py
├── src/
├── assets/
├── requirements.txt
└── venv/                        # Entorno virtual (creado en postinst)

/usr/bin/keyflow                 # Script launcher ejecutable

/usr/share/applications/         # Integración con menú del sistema
└── keyflow.desktop

/usr/share/pixmaps/              # Icono de la aplicación
└── keyflow.png

/usr/share/doc/keyflow/          # Documentación
├── README.md
└── copyright
```

## Scripts de Instalación

### postinst
Se ejecuta después de la instalación:
- Crea un entorno virtual en `/opt/keyflow/venv`
- Instala las dependencias de Python desde `requirements.txt`
- Configura permisos adecuados

### prerm
Se ejecuta antes de la desinstalación:
- Limpia el entorno virtual

## Desarrollo

Para modificar el paquete:

1. Edita `build-deb.sh` para cambiar la lógica de construcción
2. Modifica las plantillas de archivos DEBIAN dentro del script:
   - `control`: Metadatos del paquete
   - `postinst`: Script post-instalación
   - `prerm`: Script pre-desinstalación
   - `keyflow` (wrapper): Script de ejecución
   - `keyflow.desktop`: Integración con el sistema

## Verificación

Después de construir, puedes inspeccionar el contenido del paquete:

```bash
# Ver información del paquete
dpkg-deb --info keyflow_1.0.0_all.deb

# Listar contenido
dpkg-deb --contents keyflow_1.0.0_all.deb
```

## Distribución

El archivo `.deb` generado se puede distribuir directamente a usuarios de sistemas Debian/Ubuntu y derivados. Ellos solo necesitarán:

```bash
sudo dpkg -i keyflow_1.0.0_all.deb
sudo apt-get install -f
```

## Notas

- El paquete tiene arquitectura `all` porque es código Python puro
- Las dependencias del sistema se instalan automáticamente via APT
- Las dependencias de Python se instalan en un entorno virtual aislado
- El paquete es compatible con Debian 11+, Ubuntu 20.04+ y derivados
