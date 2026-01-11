# Keyflow Password Manager

<div align="center">

![Keyflow Logo](assets/logo.png)

**Un gestor de contraseñas seguro, moderno y de código abierto compatible con archivos .kdbx**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![KeePass](https://img.shields.io/badge/Format-KDBX-orange.svg)](https://keepass.info/)

</div>

---

## 📖 Descripción

Keyflow es un gestor de contraseñas moderno desarrollado con Python y PySide6 que te permite almacenar y gestionar tus credenciales de forma segura utilizando el formato estándar `.kdbx` de KeePass.

### ✨ Características Principales

- 🔐 **Cifrado Robusto**: Compatible con archivos `.kdbx` (KeePass Database)
- 🎨 **Interfaz Moderna**: Tema oscuro con diseño limpio e intuitivo
- ⚡ **Optimizado**: Tiempos de carga reducidos mediante KDF optimizado
- 🔑 **Generador de Contraseñas**: Crea contraseñas seguras automáticamente
- 🕒 **Timer de Portapapeles**: Limpieza automática del portapapeles (12 segundos)
- 💾 **Última Bóveda**: Acceso rápido a tu bóveda más reciente
- 🌐 **Menús en Español**: Interfaz completamente localizada
- 📋 **Copiar con Seguridad**: Copia usuario, contraseña y URL con un clic

---

## 🖼️ Capturas de Pantalla
 
 ### Pantalla de Inicio
 ![Pantalla de Inicio](assets/home.png)
 
 ### Vista de la Bóveda
 ![Dashboard](assets/dashboard.png)

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
sudo apt-get install -f
```

### Opción 2: Construir desde fuente

Para construir tu propio paquete `.deb`:

```bash
# Clonar el repositorio
git clone https://github.com/Maalfer/keyflow.git
cd keyflow

# Ejecutar el script de construcción
./build-deb.sh

# Instalar el paquete generado
sudo dpkg -i keyflow_1.0.0_all.deb
sudo apt-get install -f
```

### Ejecutar la aplicación

Después de la instalación, puedes ejecutar Keyflow de dos formas:

1. **Desde el menú de aplicaciones**: Busca "Keyflow Password Manager" en el menú de tu sistema
2. **Desde la terminal**:
   ```bash
   keyflow
   ```

### Desinstalar

Para desinstalar Keyflow completamente:

```bash
sudo apt remove keyflow
```

---

## 📚 Uso

### Crear una Nueva Bóveda

1. Ejecuta `python main.py`
2. Haz clic en **"Crear Nueva Base de Datos"**
3. Elige la ubicación y nombre del archivo `.kdbx`
4. Establece una contraseña maestra segura
5. ¡Listo! Ahora puedes agregar tus credenciales

### Abrir una Bóveda Existente

1. Si es tu primera vez: Haz clic en **"Abrir Base de Datos Existente"**
2. Si ya abriste una antes: Simplemente ingresa la contraseña en el campo destacado
3. Presiona **Enter** o clic en **"Abrir Bóveda"**

### Gestionar Entradas

- **Agregar**: Botón **"+ Agregar Entrada"** o `Ctrl+N`
- **Editar**: Doble clic en una entrada
- **Eliminar**: Selecciona una entrada y presiona `Delete`
- **Copiar**: Clic derecho → Copiar Usuario/Contraseña/URL

### Generar Contraseñas

Al crear o editar una entrada, haz clic en el botón **"Generar"** junto al campo de contraseña para crear una contraseña segura de 20 caracteres.

---

## 🛡️ Seguridad

- **Cifrado**: AES-256 para almacenamiento de datos
- **KDF Optimizado**: Argon2 con iteraciones ajustables (por defecto: 2 para rendimiento)
- **Limpieza de Portapapeles**: Automática después de 12 segundos
- **Sin Almacenamiento en Claro**: Las contraseñas nunca se guardan sin cifrar

> ⚠️ **Nota**: La configuración KDF está optimizada para uso personal. Para entornos de máxima seguridad, considera aumentar las iteraciones.

---

## 🏗️ Estructura del Proyecto

```
keyflow/
├── assets/              # Recursos (logo, imágenes)
├── src/
│   ├── database.py      # Lógica de base de datos (pykeepass)
│   └── ui/
│       ├── main_window.py    # Ventana principal
│       ├── start_screen.py   # Pantalla de inicio
│       ├── entry_dialog.py   # Diálogo de entrada
│       ├── login_window.py   # Ventana de login
│       └── styles.py         # Estilos CSS/QSS
├── tests/               # Tests unitarios
├── main.py             # Punto de entrada
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Maalfer**

- GitHub: [@Maalfer](https://github.com/Maalfer)
- LinkedIn: [maalfer1](https://www.linkedin.com/in/maalfer1/)
- Proyecto: [Keyflow](https://github.com/Maalfer/keyflow)

---

<div align="center">

**⭐ Si te gusta Keyflow, dale una estrella en GitHub! ⭐**

[![Star History Chart](https://api.star-history.com/svg?repos=Maalfer/keyflow&type=Date)](https://star-history.com/#Maalfer/keyflow&Date)

</div>
