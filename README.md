# Password Manager con Flet

Aplicación de gestión de contraseñas tipo KeePass construida con Flet.

## Características

- ✅ Crear y abrir bases de datos .kdbx (KeePass)
- ✅ Añadir, editar y borrar contraseñas
- ✅ Búsqueda de contraseñas
- ✅ Interfaz moderna con Flet
- ✅ Protección con contraseña maestra

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Opción 1: Usando el script
```bash
./run.sh
```

### Opción 2: Manualmente
```bash
./venv/bin/python app/main.py
```

O si prefieres activar el entorno virtual primero:
```bash
source venv/bin/activate
python app/main.py
```

## Estructura del Proyecto

```
video/
├── app/
│   ├── main.py              # Aplicación principal
│   ├── core/
│   │   └── keepass.py       # Gestor de base de datos KeePass
│   └── views/
│       ├── auth_view.py     # Vista de autenticación
│       └── vault_view.py    # Vista de contraseñas
└── requirements.txt
```

## Primer Uso

1. Ejecuta la aplicación
2. Selecciona "Crear nueva base de datos"
3. Elige una ubicación y nombre para el archivo .kdbx
4. Establece una contraseña maestra
5. Comienza a añadir tus contraseñas

## Seguridad

- Las contraseñas se almacenan en formato KeePass (.kdbx) encriptado
- Compatible con otras aplicaciones KeePass
- La contraseña maestra nunca se almacena en texto plano
