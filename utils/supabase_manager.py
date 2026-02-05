"""
🔥 Supabase Manager - Persistencia en la Nube
Base de datos PostgreSQL que NUNCA pierde datos
"""
import os
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import hashlib
from supabase import create_client, Client


class SupabaseManager:
    """
    Gestor de base de datos con Supabase (PostgreSQL en la nube)
    ✅ Datos persistentes
    ✅ No se pierden con reinicio de Streamlit
    ✅ Gratis hasta 500MB
    """
    
    def __init__(self):
        """Inicializa conexión a Supabase"""
        # Obtener credenciales desde secrets de Streamlit O variables de entorno (Railway)
        supabase_url = None
        supabase_key = None
        
        # Primero intentar leer desde Streamlit secrets
        try:
            import streamlit as st
            supabase_url = st.secrets["supabase"]["url"]
            supabase_key = st.secrets["supabase"]["key"]
        except:
            # Si falla, leer desde variables de entorno (Railway/producción)
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("❌ Faltan credenciales de Supabase. Configura secrets.toml o variables de entorno")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        print("✅ Conectado a Supabase")
    
    def _hash_password(self, password: str) -> str:
        """Hashea contraseña con SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ==================== USUARIOS ====================
    
    def register_user(self, username: str, full_name: str, email: str = "", password: str = "") -> Tuple[bool, str]:
        """
        Registra nuevo usuario en Supabase
        
        Returns:
            (success, message)
        """
        try:
            # Verificar si usuario existe
            existing = self.client.table('users').select('username').eq('username', username).execute()
            
            if existing.data:
                return False, f"❌ El usuario '{username}' ya existe"
            
            # Hash de contraseña
            password_hash = self._hash_password(password) if password else ""
            
            # Insertar usuario
            user_data = {
                'username': username,
                'full_name': full_name,
                'email': email or None,  # Convertir string vacío a NULL
                'password_hash': password_hash
            }
            
            response = self.client.table('users').insert(user_data).execute()
            
            # Verificar si la inserción fue exitosa
            if not response.data:
                return False, f"❌ No se pudo crear el usuario. Verifica RLS en Supabase"
            
            return True, f"✅ Usuario '{username}' registrado exitosamente"
            
        except Exception as e:
            import traceback
            error_full = traceback.format_exc()
            error_msg = str(e)
            print(f"🔍 ERROR COMPLETO: {error_full}")
            
            if "401" in error_msg or "Invalid API key" in error_msg or "new row violates row-level security" in error_msg.lower():
                return False, f"❌ Error RLS: Ve a Supabase → Table Editor → users → Click el candado y desactiva RLS"
            return False, f"❌ Error: {error_msg}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Autentica usuario
        
        Returns:
            (success, user_data)
        """
        try:
            password_hash = self._hash_password(password)
            
            # Buscar usuario
            result = self.client.table('users').select('*').eq('username', username).eq('password_hash', password_hash).execute()
            
            if not result.data:
                return False, None
            
            user = result.data[0]
            
            # Actualizar último login
            self.client.table('users').update({'last_login': datetime.now().isoformat()}).eq('username', username).execute()
            
            return True, user
            
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return False, None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Obtiene datos de un usuario"""
        try:
            result = self.client.table('users').select('*').eq('username', username).execute()
            return result.data[0] if result.data else None
        except:
            return None
    
    # ==================== TRANSACCIONES ====================
    
    def add_transaction(self, username: str, transaction_data: Dict) -> Tuple[bool, str]:
        """
        Agrega transacción para un usuario
        
        Args:
            username: Usuario dueño de la transacción
            transaction_data: Dict con keys: tipo, categoria, monto, descripcion, fecha
        """
        try:
            # Agregar username y timestamp
            transaction_data['username'] = username
            transaction_data['created_at'] = datetime.now().isoformat()
            
            # Insertar en Supabase
            self.client.table('transactions').insert(transaction_data).execute()
            
            return True, "✅ Transacción guardada"
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def get_user_transactions(self, username: str, limit: int = 100) -> List[Dict]:
        """
        Obtiene transacciones de un usuario
        
        Returns:
            Lista de transacciones ordenadas por fecha (más recientes primero)
        """
        try:
            result = self.client.table('transactions')\
                .select('*')\
                .eq('username', username)\
                .order('fecha', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Error obteniendo transacciones: {e}")
            return []
    
    def delete_transaction(self, transaction_id: int, username: str) -> Tuple[bool, str]:
        """
        Elimina una transacción
        
        Args:
            transaction_id: ID de la transacción
            username: Usuario (para verificar permisos)
        """
        try:
            # Verificar que la transacción pertenezca al usuario
            result = self.client.table('transactions')\
                .delete()\
                .eq('id', transaction_id)\
                .eq('username', username)\
                .execute()
            
            if result.data:
                return True, "✅ Transacción eliminada"
            else:
                return False, "❌ Transacción no encontrada"
                
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def update_transaction(self, transaction_id: int, username: str, updated_data: Dict) -> Tuple[bool, str]:
        """
        Actualiza una transacción existente
        """
        try:
            # Agregar timestamp de actualización
            updated_data['updated_at'] = datetime.now().isoformat()
            
            result = self.client.table('transactions')\
                .update(updated_data)\
                .eq('id', transaction_id)\
                .eq('username', username)\
                .execute()
            
            if result.data:
                return True, "✅ Transacción actualizada"
            else:
                return False, "❌ Transacción no encontrada"
                
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    # ==================== PRESUPUESTOS ====================
    
    def set_budget(self, username: str, categoria: str, monto: float, mes: int, anio: int) -> Tuple[bool, str]:
        """
        Establece presupuesto para una categoría
        """
        try:
            budget_data = {
                'username': username,
                'categoria': categoria,
                'monto': monto,
                'mes': mes,
                'anio': anio,
                'created_at': datetime.now().isoformat()
            }
            
            # Verificar si ya existe
            existing = self.client.table('budgets')\
                .select('*')\
                .eq('username', username)\
                .eq('categoria', categoria)\
                .eq('mes', mes)\
                .eq('anio', anio)\
                .execute()
            
            if existing.data:
                # Actualizar
                self.client.table('budgets')\
                    .update({'monto': monto})\
                    .eq('id', existing.data[0]['id'])\
                    .execute()
            else:
                # Insertar
                self.client.table('budgets').insert(budget_data).execute()
            
            return True, f"✅ Presupuesto de {categoria} establecido"
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def get_budgets(self, username: str, mes: int, anio: int) -> List[Dict]:
        """Obtiene presupuestos de un usuario para un mes específico"""
        try:
            result = self.client.table('budgets')\
                .select('*')\
                .eq('username', username)\
                .eq('mes', mes)\
                .eq('anio', anio)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Error obteniendo presupuestos: {e}")
            return []
    
    # ==================== ESTADÍSTICAS ====================
    
    def get_user_stats(self, username: str) -> Dict:
        """
        Obtiene estadísticas generales del usuario
        """
        try:
            transactions = self.get_user_transactions(username, limit=1000)
            
            total_ingresos = sum(t['monto'] for t in transactions if t['tipo'] == 'Ingreso')
            total_gastos = sum(t['monto'] for t in transactions if t['tipo'] == 'Gasto')
            balance = total_ingresos - total_gastos
            
            return {
                'total_transactions': len(transactions),
                'total_ingresos': total_ingresos,
                'total_gastos': total_gastos,
                'balance': balance,
                'last_transaction': transactions[0]['fecha'] if transactions else None
            }
            
        except Exception as e:
            print(f"❌ Error calculando stats: {e}")
            return {
                'total_transactions': 0,
                'total_ingresos': 0,
                'total_gastos': 0,
                'balance': 0,
                'last_transaction': None
            }


# ==================== SQL SETUP ====================
# Ejecuta esto en el SQL Editor de Supabase para crear las tablas:

SQL_SETUP = """
-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP DEFAULT NOW()
);

-- Tabla de transacciones
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Ingreso', 'Gasto')),
    categoria VARCHAR(50) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Tabla de presupuestos
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    categoria VARCHAR(50) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    mes INT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(username, categoria, mes, anio)
);

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_transactions_username ON transactions(username);
CREATE INDEX IF NOT EXISTS idx_transactions_fecha ON transactions(fecha DESC);
CREATE INDEX IF NOT EXISTS idx_budgets_username ON budgets(username);

-- Habilitar Row Level Security (RLS) - opcional pero recomendado
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;
"""
