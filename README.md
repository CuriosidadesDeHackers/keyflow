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

## 🖼️ Captura de Pantalla

![Pantalla de Inicio](assets/home.png)

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Maalfer/keyflow.git
cd keyflow
```

2. **Crear entorno virtual** (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python main.py
```

---

## 🐳 Docker

También puedes ejecutar Keyflow usando Docker (requiere X11 forwarding para GUI):

```bash
# Construir la imagen
docker build -t keyflow .

# Ejecutar (Linux)
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix keyflow
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
├── Dockerfile          # Imagen Docker
└── README.md           # Este archivo
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una sugerencia:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👤 Autor

**Maalfer**

- GitHub: [@Maalfer](https://github.com/Maalfer)
- LinkedIn: [maalfer1](https://www.linkedin.com/in/maalfer1/)
- Proyecto: [Keyflow](https://github.com/Maalfer/keyflow)

---

## 🙏 Agradecimientos

- [KeePass](https://keepass.info/) por el formato `.kdbx`
- [pykeepass](https://github.com/libkeepass/pykeepass) por la biblioteca Python
- [PySide6](https://www.qt.io/qt-for-python) por el framework GUI

---

<div align="center">

**⭐ Si te gusta Keyflow, dale una estrella en GitHub! ⭐**

</div>
