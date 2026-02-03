"""
Módulo de gestión de usuarios para el sistema multi-usuario
"""
import json
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict, List


class UserManager:
    """
    Clase para gestionar usuarios y autenticación
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa el gestor de usuarios
        
        Args:
            data_dir: Directorio donde se almacenarán los datos
        """
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        
        # Crear directorio si no existe
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Crear archivo de usuarios si no existe
        if not os.path.exists(self.users_file):
            self._create_users_file()
    
    def _create_users_file(self):
        """
        Crea un archivo JSON vacío para usuarios
        """
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump({"users": []}, f, indent=4)
    
    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, full_name: str, email: str = "", password: str = "") -> Dict[str, any]:
        """
        Registra un nuevo usuario
        
        Args:
            username: Nombre de usuario único
            full_name: Nombre completo del usuario
            email: Email del usuario (opcional)
            password: Contraseña del usuario
            
        Returns:
            Diccionario con resultado de la operación
        """
        # Validar que el username no esté vacío
        if not username or not username.strip():
            return {
                'success': False,
                'message': 'El nombre de usuario no puede estar vacío'
            }
        
        # Validar contraseña
        if not password or len(password) < 4:
            return {
                'success': False,
                'message': 'La contraseña debe tener al menos 4 caracteres'
            }
        
        username = username.strip().lower()
        
        # Verificar si el usuario ya existe
        if self.user_exists(username):
            return {
                'success': False,
                'message': f'El usuario "{username}" ya está registrado'
            }
        
        # Cargar usuarios existentes
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Crear nuevo usuario
        new_user = {
            'username': username,
            'full_name': full_name.strip(),
            'email': email.strip() if email else "",
            'password_hash': self._hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': None
        }
        
        # Agregar usuario
        data['users'].append(new_user)
        
        # Guardar
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # No devolver el hash de la contraseña
        user_info = {k: v for k, v in new_user.items() if k != 'password_hash'}
        return {
            'success': True,
            'message': f'¡Bienvenido {full_name}! Tu cuenta ha sido creada exitosamente',
            'user': user_info
        }
    
    def user_exists(self, username: str) -> bool:
        """
        Verifica si un usuario existe
        
        Args:
            username: Nombre de usuario a verificar
            
        Returns:
            True si el usuario existe, False en caso contrario
        """
        username = username.strip().lower()
        
        if not os.path.exists(self.users_file):
            return False
        
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return any(user['username'] == username for user in data['users'])
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Obtiene la información de un usuario
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Diccionario con información del usuario o None si no existe
        """
        username = username.strip().lower()
        
        if not os.path.exists(self.users_file):
            return None
        
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for user in data['users']:
            if user['username'] == username:
                return user
        
        return None
    
    def login_user(self, username: str, password: str = "") -> Dict[str, any]:
        """
        Inicia sesión de un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            Diccionario con resultado de la operación
        """
        username = username.strip().lower()
        
        # Verificar si el usuario existe
        user = self.get_user(username)
        
        if not user:
            return {
                'success': False,
                'message': f'El usuario "{username}" no está registrado. Por favor crea una cuenta primero.'
            }
        
        # Si el usuario tiene contraseña, validarla
        if 'password_hash' in user:
            if not password:
                return {
                    'success': False,
                    'message': '❌ Debes ingresar tu contraseña'
                }
            
            password_hash = self._hash_password(password)
            if user['password_hash'] != password_hash:
                return {
                    'success': False,
                    'message': '❌ Contraseña incorrecta'
                }
        
        # Actualizar última fecha de login
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for u in data['users']:
            if u['username'] == username:
                u['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # No devolver el hash de la contraseña
        user_info = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return {
            'success': True,
            'message': f'¡Bienvenido de nuevo {user["full_name"]}!',
            'user': user_info
        }
    
    def get_all_users(self) -> List[Dict]:
        """
        Obtiene la lista de todos los usuarios registrados
        
        Returns:
            Lista de diccionarios con información de usuarios
        """
        if not os.path.exists(self.users_file):
            return []
        
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data['users']
    
    def delete_user(self, username: str) -> Dict[str, any]:
        """
        Elimina un usuario del sistema
        
        Args:
            username: Nombre de usuario a eliminar
            
        Returns:
            Diccionario con resultado de la operación
        """
        username = username.strip().lower()
        
        if not self.user_exists(username):
            return {
                'success': False,
                'message': f'El usuario "{username}" no existe'
            }
        
        # Cargar usuarios
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filtrar usuario
        data['users'] = [u for u in data['users'] if u['username'] != username]
        
        # Guardar
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        return {
            'success': True,
            'message': f'Usuario "{username}" eliminado exitosamente'
        }
