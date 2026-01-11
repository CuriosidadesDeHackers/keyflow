"""
KeePass Database Manager
Maneja todas las operaciones con archivos .kdbx
"""
import os
from uuid import UUID

from typing import Optional, List, Dict
from pykeepass import PyKeePass, create_database
from pykeepass.exceptions import CredentialsError


class KeePassManager:
    """Gestor de base de datos KeePass"""
    
    def __init__(self):
        self.kp: Optional[PyKeePass] = None
        self.db_path: Optional[str] = None
    
    def create_database(self, filepath: str, password: str) -> bool:
        """
        Crea una nueva base de datos KeePass
        
        Args:
            filepath: Ruta donde crear el archivo .kdbx
            password: Contraseña maestra
            
        Returns:
            True si se creó correctamente, False en caso contrario
        """
        try:
            self.kp = create_database(filepath, password=password)
            self.db_path = filepath
            return True
        except Exception as e:
            print(f"Error al crear la base de datos: {e}")
            return False
    
    def open_database(self, filepath: str, password: str) -> bool:
        """
        Abre una base de datos KeePass existente
        
        Args:
            filepath: Ruta al archivo .kdbx
            password: Contraseña maestra
            
        Returns:
            True si se abrió correctamente, False en caso contrario
        """
        try:
            if not os.path.exists(filepath):
                return False
            
            self.kp = PyKeePass(filepath, password=password)
            self.db_path = filepath
            return True
        except CredentialsError:
            print("Contraseña incorrecta")
            return False
        except Exception as e:
            print(f"Error al abrir la base de datos: {e}")
            return False
    
    def close_database(self):
        """Cierra la base de datos actual"""
        self.kp = None
        self.db_path = None
    
    def add_entry(self, title: str, username: str, password: str, url: str = "", notes: str = "") -> bool:
        """
        Añade una nueva entrada a la base de datos
        
        Args:
            title: Título de la entrada
            username: Nombre de usuario
            password: Contraseña
            url: URL (opcional)
            notes: Notas (opcional)
            
        Returns:
            True si se añadió correctamente, False en caso contrario
        """
        if not self.kp:
            return False
        
        try:
            group = self.kp.root_group
            self.kp.add_entry(
                destination_group=group,
                title=title,
                username=username,
                password=password,
                url=url,
                notes=notes
            )
            self.kp.save()
            return True
        except Exception as e:
            print(f"Error al añadir entrada: {e}")
            return False
    
    def get_all_entries(self) -> List[Dict[str, str]]:
        """
        Obtiene todas las entradas de la base de datos
        
        Returns:
            Lista de diccionarios con la información de las entradas
        """
        if not self.kp:
            return []
        
        entries = []
        for entry in self.kp.entries:
            entries.append({
                'uuid': str(entry.uuid),
                'title': entry.title or "",
                'username': entry.username or "",
                'password': entry.password or "",
                'url': entry.url or "",
                'notes': entry.notes or ""
            })
        
        return entries
    
    def update_entry(self, uuid: str, title: str, username: str, password: str, 
                     url: str = "", notes: str = "") -> bool:
        """
        Actualiza una entrada existente
        
        Args:
            uuid: UUID de la entrada a actualizar
            title: Nuevo título
            username: Nuevo nombre de usuario
            password: Nueva contraseña
            url: Nueva URL (opcional)
            notes: Nuevas notas (opcional)
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        if not self.kp:
            return False
        
        try:
            entry = self.kp.find_entries(uuid=UUID(uuid), first=True)
            if not entry:
                return False
            
            entry.title = title
            entry.username = username
            entry.password = password
            entry.url = url
            entry.notes = notes
            
            self.kp.save()
            return True
        except Exception as e:
            print(f"Error al actualizar entrada: {e}")
            return False
    
    def delete_entry(self, uuid: str) -> bool:
        """
        Elimina una entrada de la base de datos
        
        Args:
            uuid: UUID de la entrada a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not self.kp:
            return False
        
        try:
            entry = self.kp.find_entries(uuid=UUID(uuid), first=True)
            if not entry:
                return False
            
            self.kp.delete_entry(entry)
            self.kp.save()
            return True
        except Exception as e:
            print(f"Error al eliminar entrada: {e}")
            return False
    
    def search_entries(self, query: str) -> List[Dict[str, str]]:
        """
        Busca entradas por título, username o URL
        
        Args:
            query: Texto a buscar
            
        Returns:
            Lista de entradas que coinciden con la búsqueda
        """
        if not self.kp or not query:
            return self.get_all_entries()
        
        query_lower = query.lower()
        all_entries = self.get_all_entries()
        
        return [
            entry for entry in all_entries
            if query_lower in entry['title'].lower() 
            or query_lower in entry['username'].lower()
            or query_lower in entry['url'].lower()
        ]
    
    def is_database_open(self) -> bool:
        """Verifica si hay una base de datos abierta"""
        return self.kp is not None
