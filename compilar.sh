#!/bin/bash
# Script unificado para compilar e instalar Keyflow
# Autor: Maalfer
# Uso: ./compilar.sh [--instalar]

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
PKG_NAME="keyflow"
PKG_VERSION="1.0.0"
PKG_ARCH="all"
BUILD_DIR="debian-package"
DEB_FILE="${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}.deb"

# Verificar si se solicita instalación automática
AUTO_INSTALL=false
if [ "$1" == "--instalar" ] || [ "$1" == "-i" ]; then
    AUTO_INSTALL=true
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Keyflow - Compilador .deb${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Limpiar construcciones previas
if [ -d "$BUILD_DIR" ]; then
    echo -e "${YELLOW}Limpiando construcción previa...${NC}"
    rm -rf "$BUILD_DIR"
fi

if [ -f "$DEB_FILE" ]; then
    echo -e "${YELLOW}Eliminando paquete .deb anterior...${NC}"
    rm -f "$DEB_FILE"
fi

echo -e "${GREEN}✓${NC} Limpieza completada"
echo

# Crear estructura de directorios
echo -e "${YELLOW}Creando estructura de directorios...${NC}"
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/opt/keyflow"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/pixmaps"
mkdir -p "$BUILD_DIR/usr/share/doc/keyflow"
echo -e "${GREEN}✓${NC} Estructura creada"
echo

# Copiar archivos de la aplicación
echo -e "${YELLOW}Copiando archivos de la aplicación...${NC}"
cp -r src "$BUILD_DIR/opt/keyflow/"
cp -r assets "$BUILD_DIR/opt/keyflow/"
cp main.py "$BUILD_DIR/opt/keyflow/"
cp requirements.txt "$BUILD_DIR/opt/keyflow/"
echo -e "${GREEN}✓${NC} Archivos de la aplicación copiados"
echo

# Copiar icono
echo -e "${YELLOW}Copiando icono...${NC}"
cp assets/logo.png "$BUILD_DIR/usr/share/pixmaps/keyflow.png"
echo -e "${GREEN}✓${NC} Icono copiado"
echo

# Copiar documentación
echo -e "${YELLOW}Copiando documentación...${NC}"
cp README.md "$BUILD_DIR/usr/share/doc/keyflow/"
if [ -f "LICENSE" ]; then
    cp LICENSE "$BUILD_DIR/usr/share/doc/keyflow/copyright"
fi
echo -e "${GREEN}✓${NC} Documentación copiada"
echo

# Crear archivo control
echo -e "${YELLOW}Creando archivo de control DEBIAN...${NC}"
cat > "$BUILD_DIR/DEBIAN/control" << EOF
Package: keyflow
Version: ${PKG_VERSION}
Section: utils
Priority: optional
Architecture: ${PKG_ARCH}
Depends: python3 (>= 3.11), python3-pip, python3-venv
Maintainer: Maalfer <maalfer1@linkedin.com>
Description: Gestor de contraseñas seguro y moderno
 Keyflow es un gestor de contraseñas moderno desarrollado con Python y PySide6
 que permite almacenar y gestionar credenciales de forma segura utilizando
 el formato estándar .kdbx de KeePass.
 .
 Características principales:
  - Cifrado robusto compatible con archivos .kdbx (KeePass Database)
  - Interfaz moderna con tema oscuro
  - Generador de contraseñas seguras
  - Timer de portapapeles con limpieza automática
  - Menús completamente en español
Homepage: https://github.com/Maalfer/keyflow
EOF
echo -e "${GREEN}✓${NC} Archivo de control creado"
echo

# Crear script postinst (post-instalación)
echo -e "${YELLOW}Creando script de post-instalación...${NC}"
cat > "$BUILD_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

echo "Configurando Keyflow..."

# Crear entorno virtual
if [ ! -d "/opt/keyflow/venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv /opt/keyflow/venv
fi

# Activar entorno virtual e instalar dependencias
echo "Instalando dependencias de Python..."
/opt/keyflow/venv/bin/pip install --upgrade pip > /dev/null 2>&1
/opt/keyflow/venv/bin/pip install -r /opt/keyflow/requirements.txt > /dev/null 2>&1

# Configurar permisos
chmod -R 755 /opt/keyflow
chmod 755 /usr/bin/keyflow

echo "✓ Keyflow instalado correctamente"
echo "Ejecuta 'keyflow' desde la terminal o búscalo en el menú de aplicaciones"

exit 0
EOF
chmod 755 "$BUILD_DIR/DEBIAN/postinst"
echo -e "${GREEN}✓${NC} Script postinst creado"
echo

# Crear script prerm (pre-desinstalación)
echo -e "${YELLOW}Creando script de pre-desinstalación...${NC}"
cat > "$BUILD_DIR/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

echo "Desinstalando Keyflow..."

# Limpiar entorno virtual si existe
if [ -d "/opt/keyflow/venv" ]; then
    rm -rf /opt/keyflow/venv
fi

exit 0
EOF
chmod 755 "$BUILD_DIR/DEBIAN/prerm"
echo -e "${GREEN}✓${NC} Script prerm creado"
echo

# Crear wrapper script
echo -e "${YELLOW}Creando script de ejecución...${NC}"
cat > "$BUILD_DIR/usr/bin/keyflow" << 'EOF'
#!/bin/bash
# Keyflow launcher script

# Activar entorno virtual
source /opt/keyflow/venv/bin/activate

# Ejecutar la aplicación
cd /opt/keyflow
python3 main.py "$@"
EOF
chmod 755 "$BUILD_DIR/usr/bin/keyflow"
echo -e "${GREEN}✓${NC} Script de ejecución creado"
echo

# Crear archivo .desktop
echo -e "${YELLOW}Creando archivo .desktop...${NC}"
cat > "$BUILD_DIR/usr/share/applications/keyflow.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Keyflow Password Manager
Comment=Gestor de contraseñas seguro compatible con KeePass
Exec=/usr/bin/keyflow
Icon=keyflow
Terminal=false
Categories=Utility;Security;
Keywords=password;keepass;security;vault;
StartupNotify=true
StartupWMClass=keyflow
EOF
echo -e "${GREEN}✓${NC} Archivo .desktop creado"
echo

# Construir el paquete .deb
echo -e "${YELLOW}Construyendo paquete .deb...${NC}"
dpkg-deb --build "$BUILD_DIR" "$DEB_FILE" 2>&1 | grep -v "root directory" | grep -v "hint:" || true
echo

# Verificar el paquete
if [ -f "$DEB_FILE" ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ PAQUETE CONSTRUIDO EXITOSAMENTE${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo -e "Archivo: ${GREEN}${DEB_FILE}${NC}"
    echo -e "Tamaño: ${GREEN}$(du -h "$DEB_FILE" | cut -f1)${NC}"
    echo
    
    # Instalar automáticamente si se solicitó
    if [ "$AUTO_INSTALL" = true ]; then
        echo -e "${BLUE}Procediendo con la instalación...${NC}"
        echo
        
        # Desinstalar versión anterior si existe
        if dpkg -l | grep -q "^ii  keyflow "; then
            echo -e "${YELLOW}Desinstalando versión anterior...${NC}"
            sudo apt remove keyflow -y > /dev/null 2>&1
            echo -e "${GREEN}✓${NC} Versión anterior desinstalada"
        fi
        
        # Instalar nueva versión
        echo -e "${YELLOW}Instalando nueva versión...${NC}"
        sudo dpkg -i "$DEB_FILE"
        sudo apt-get install -f -y > /dev/null 2>&1
        
        # Actualizar caché del sistema
        echo -e "${YELLOW}Actualizando caché del sistema...${NC}"
        sudo update-desktop-database 2>/dev/null || true
        sudo gtk-update-icon-cache /usr/share/pixmaps -f 2>/dev/null || true
        
        echo
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ INSTALACIÓN COMPLETADA${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo
        echo -e "Ejecuta: ${BLUE}keyflow${NC}"
        echo
    else
        echo -e "${YELLOW}Para instalar manualmente:${NC}"
        echo -e "  ${BLUE}./compilar.sh --instalar${NC}"
        echo
        echo -e "O ejecuta:"
        echo -e "  ${BLUE}sudo dpkg -i $DEB_FILE${NC}"
        echo -e "  ${BLUE}sudo apt-get install -f${NC}"
        echo
    fi
    
    # Limpiar archivos temporales
    echo -e "${YELLOW}Limpiando archivos temporales...${NC}"
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}✓${NC} Limpieza completada"
else
    echo -e "${RED}✗ Error: No se pudo crear el paquete .deb${NC}"
    exit 1
fi
