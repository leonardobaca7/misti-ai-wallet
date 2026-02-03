"""
Módulo de gestión de base de datos SQLite para Misti AI Wallet
Reemplaza el almacenamiento CSV/JSON por SQLite
"""
import sqlite3
import pandas as pd
import os
from datetime import datetime
from typing import Optional, List, Dict
import hashlib


class DatabaseManager:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, db_path: str = "data/misti_wallet.db"):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Crear tablas si no existen
        self._create_tables()
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        """)
        
        # Tabla de transacciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                usuario TEXT NOT NULL,
                tipo TEXT NOT NULL,
                monto REAL NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT,
                texto_original TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (usuario) REFERENCES users(username)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, full_name: str, email: str, password: str) -> Dict:
        """Registra un nuevo usuario"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Validar contraseña
            if len(password) < 4:
                return {'success': False, 'message': 'La contraseña debe tener al menos 4 caracteres'}
            
            password_hash = self._hash_password(password)
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                INSERT INTO users (username, full_name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (username.lower().strip(), full_name.strip(), email.strip(), password_hash, created_at))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f'¡Bienvenido {full_name}! Tu cuenta ha sido creada exitosamente',
                'user': {
                    'username': username.lower().strip(),
                    'full_name': full_name.strip(),
                    'email': email.strip(),
                    'created_at': created_at
                }
            }
        except sqlite3.IntegrityError:
            return {'success': False, 'message': f'El usuario "{username}" ya está registrado'}
        except Exception as e:
            return {'success': False, 'message': f'Error al crear cuenta: {str(e)}'}
    
    def login_user(self, username: str, password: str) -> Dict:
        """Autentica un usuario"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, full_name, email, password_hash, created_at
                FROM users WHERE username = ?
            """, (username.lower().strip(),))
            
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return {'success': False, 'message': 'Usuario no encontrado'}
            
            # Verificar contraseña
            password_hash = self._hash_password(password)
            if user[3] != password_hash:
                conn.close()
                return {'success': False, 'message': '❌ Contraseña incorrecta'}
            
            # Actualizar last_login
            last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE users SET last_login = ? WHERE username = ?", 
                          (last_login, username.lower().strip()))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f'¡Bienvenido de vuelta, {user[1]}! 🎉',
                'user': {
                    'username': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'created_at': user[4],
                    'last_login': last_login
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'Error al iniciar sesión: {str(e)}'}
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Obtiene información de un usuario"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, full_name, email, created_at, last_login
                FROM users WHERE username = ?
            """, (username.lower().strip(),))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'username': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'created_at': user[3],
                    'last_login': user[4]
                }
            return None
        except Exception:
            return None
    
    # ==================== GESTIÓN DE TRANSACCIONES ====================
    
    def add_transaction(self, monto: float, categoria: str, descripcion: str,
                       texto_original: str, fecha: datetime, usuario: str, tipo: str) -> bool:
        """Agrega una nueva transacción"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            fecha_str = fecha.strftime('%Y-%m-%d')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                INSERT INTO transactions 
                (fecha, usuario, tipo, monto, categoria, descripcion, texto_original, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (fecha_str, usuario, tipo, monto, categoria, descripcion, texto_original, timestamp))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar transacción: {e}")
            return False
    
    def load_transactions(self, usuario: Optional[str] = None) -> pd.DataFrame:
        """Carga transacciones como DataFrame"""
        try:
            conn = self._get_connection()
            
            if usuario:
                query = "SELECT * FROM transactions WHERE usuario = ? ORDER BY fecha DESC, timestamp DESC"
                df = pd.read_sql_query(query, conn, params=(usuario,))
            else:
                query = "SELECT * FROM transactions ORDER BY fecha DESC, timestamp DESC"
                df = pd.read_sql_query(query, conn)
            
            conn.close()
            
            # Convertir fecha a datetime
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'])
            
            return df
        except Exception as e:
            print(f"Error al cargar transacciones: {e}")
            return pd.DataFrame(columns=[
                'id', 'fecha', 'usuario', 'tipo', 'monto', 'categoria',
                'descripcion', 'texto_original', 'timestamp'
            ])
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Elimina una transacción por ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar transacción: {e}")
            return False
    
    def clear_user_data(self, usuario: str) -> bool:
        """Elimina todas las transacciones de un usuario"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM transactions WHERE usuario = ?", (usuario,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al limpiar datos: {e}")
            return False
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict]:
        """Obtiene una transacción por ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'fecha': row[1],
                    'usuario': row[2],
                    'tipo': row[3],
                    'monto': row[4],
                    'categoria': row[5],
                    'descripcion': row[6],
                    'texto_original': row[7],
                    'timestamp': row[8]
                }
            return None
        except Exception:
            return None


if __name__ == "__main__":
    # Test del módulo
    print("✅ DatabaseManager creado exitosamente")
    db = DatabaseManager("data/test.db")
    print("✅ Base de datos inicializada")
