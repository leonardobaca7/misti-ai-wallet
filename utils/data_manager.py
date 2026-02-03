"""
Módulo de gestión de datos para almacenar y recuperar gastos
"""
import pandas as pd
import os
from datetime import datetime
from typing import Optional


class DataManager:
    """
    Clase para gestionar el almacenamiento de gastos en archivo CSV
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa el gestor de datos
        
        Args:
            data_dir: Directorio donde se almacenarán los datos
        """
        self.data_dir = data_dir
        self.csv_file = os.path.join(data_dir, "gastos.csv")
        
        # Crear directorio si no existe
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Crear archivo CSV si no existe
        if not os.path.exists(self.csv_file):
            self._create_empty_csv()
    
    def _create_empty_csv(self):
        """
        Crea un archivo CSV vacío con las columnas necesarias
        """
        df = pd.DataFrame(columns=[
            'id',
            'fecha',
            'usuario',
            'tipo',  # 'gasto' o 'ingreso'
            'monto',
            'categoria',
            'descripcion',
            'texto_original',
            'timestamp'
        ])
        df.to_csv(self.csv_file, index=False)
    
    def add_expense(
        self,
        monto: float,
        categoria: str,
        descripcion: str,
        texto_original: str,
        fecha: Optional[datetime] = None,
        usuario: str = "default",
        tipo: str = "gasto"
    ) -> int:
        """
        Agrega un nuevo gasto o ingreso al archivo CSV
        
        Args:
            monto: Monto del gasto/ingreso
            categoria: Categoría del gasto/ingreso
            descripcion: Descripción del gasto/ingreso
            texto_original: Texto original ingresado por el usuario
            fecha: Fecha del gasto/ingreso (por defecto la fecha actual)
            usuario: Nombre de usuario dueño del registro
            tipo: 'gasto' o 'ingreso'
            
        Returns:
            ID del registro agregado
        """
        if fecha is None:
            fecha = datetime.now()
        
        # Leer datos existentes
        df = self.load_expenses()
        
        # Generar nuevo ID
        if df.empty:
            new_id = 1
        else:
            new_id = df['id'].max() + 1
        
        # Crear nueva fila
        new_expense = pd.DataFrame([{
            'id': new_id,
            'fecha': fecha.strftime('%Y-%m-%d'),
            'usuario': usuario,
            'tipo': tipo,
            'monto': monto,
            'categoria': categoria,
            'descripcion': descripcion,
            'texto_original': texto_original,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])
        
        # Agregar al DataFrame
        df = pd.concat([df, new_expense], ignore_index=True)
        
        # Guardar
        df.to_csv(self.csv_file, index=False)
        
        return new_id
    
    def load_expenses(self, usuario: Optional[str] = None) -> pd.DataFrame:
        """
        Carga todos los gastos/ingresos del archivo CSV, opcionalmente filtrados por usuario
        
        Args:
            usuario: Nombre de usuario para filtrar (opcional)
        
        Returns:
            DataFrame con todos los gastos/ingresos
        """
        if not os.path.exists(self.csv_file):
            self._create_empty_csv()
            return pd.DataFrame(columns=[
                'id', 'fecha', 'usuario', 'tipo', 'monto', 'categoria',
                'descripcion', 'texto_original', 'timestamp'
            ])
        
        df = pd.read_csv(self.csv_file)
        
        if df.empty:
            return df
        
        # Asegurar que existe la columna usuario (para compatibilidad con datos antiguos)
        if 'usuario' not in df.columns:
            df['usuario'] = 'default'
        
        # Asegurar que existe la columna tipo (para compatibilidad con datos antiguos)
        if 'tipo' not in df.columns:
            df['tipo'] = 'gasto'
        
        # Filtrar por usuario si se especifica
        if usuario:
            df = df[df['usuario'] == usuario]
        
        # Convertir fecha a datetime solo si hay datos
        if not df.empty:
            df['fecha'] = pd.to_datetime(df['fecha'])
            # Asegurar que id sea entero
            df['id'] = df['id'].astype(int)
        
        return df
    
    def get_expense_by_id(self, expense_id: int) -> Optional[pd.Series]:
        """
        Obtiene un gasto específico por su ID
        
        Args:
            expense_id: ID del gasto
            
        Returns:
            Serie de pandas con los datos del gasto o None si no existe
        """
        df = self.load_expenses()
        
        if df.empty:
            return None
        
        expense = df[df['id'] == expense_id]
        
        if expense.empty:
            return None
        
        return expense.iloc[0]
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Elimina un gasto por su ID
        
        Args:
            expense_id: ID del gasto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        df = self.load_expenses()
        
        if df.empty:
            return False
        
        initial_len = len(df)
        df = df[df['id'] != expense_id]
        
        if len(df) == initial_len:
            return False
        
        df.to_csv(self.csv_file, index=False)
        return True
    
    def update_expense(
        self,
        expense_id: int,
        monto: Optional[float] = None,
        categoria: Optional[str] = None,
        descripcion: Optional[str] = None,
        fecha: Optional[datetime] = None
    ) -> bool:
        """
        Actualiza un gasto existente
        
        Args:
            expense_id: ID del gasto a actualizar
            monto: Nuevo monto (opcional)
            categoria: Nueva categoría (opcional)
            descripcion: Nueva descripción (opcional)
            fecha: Nueva fecha (opcional)
            
        Returns:
            True si se actualizó correctamente, False si no existe
        """
        df = self.load_expenses()
        
        if df.empty or expense_id not in df['id'].values:
            return False
        
        # Actualizar campos
        if monto is not None:
            df.loc[df['id'] == expense_id, 'monto'] = monto
        
        if categoria is not None:
            df.loc[df['id'] == expense_id, 'categoria'] = categoria
        
        if descripcion is not None:
            df.loc[df['id'] == expense_id, 'descripcion'] = descripcion
        
        if fecha is not None:
            df.loc[df['id'] == expense_id, 'fecha'] = fecha.strftime('%Y-%m-%d')
        
        # Actualizar timestamp
        df.loc[df['id'] == expense_id, 'timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar
        df.to_csv(self.csv_file, index=False)
        return True
    
    def get_expenses_by_category(self, categoria: str) -> pd.DataFrame:
        """
        Obtiene todos los gastos de una categoría específica
        
        Args:
            categoria: Nombre de la categoría
            
        Returns:
            DataFrame con los gastos de la categoría
        """
        df = self.load_expenses()
        
        if df.empty:
            return df
        
        return df[df['categoria'] == categoria]
    
    def get_expenses_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Obtiene gastos en un rango de fechas
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            DataFrame con los gastos en el rango
        """
        df = self.load_expenses()
        
        if df.empty:
            return df
        
        mask = (df['fecha'] >= pd.Timestamp(start_date)) & (df['fecha'] <= pd.Timestamp(end_date))
        return df[mask]
    
    def get_total_by_category(self) -> pd.DataFrame:
        """
        Calcula el total gastado por categoría
        
        Returns:
            DataFrame con el total por categoría
        """
        df = self.load_expenses()
        
        if df.empty:
            return pd.DataFrame(columns=['categoria', 'total'])
        
        return df.groupby('categoria')['monto'].sum().reset_index(name='total')
    
    def get_statistics(self) -> dict:
        """
        Calcula estadísticas generales de los gastos
        
        Returns:
            Diccionario con estadísticas
        """
        df = self.load_expenses()
        
        if df.empty:
            return {
                'total_gastos': 0,
                'promedio': 0,
                'mediana': 0,
                'minimo': 0,
                'maximo': 0,
                'num_gastos': 0
            }
        
        return {
            'total_gastos': df['monto'].sum(),
            'promedio': df['monto'].mean(),
            'mediana': df['monto'].median(),
            'minimo': df['monto'].min(),
            'maximo': df['monto'].max(),
            'num_gastos': len(df)
        }
    
    def clear_all_data(self):
        """
        Elimina todos los gastos (crea un CSV vacío)
        """
        self._create_empty_csv()
    
    def export_to_csv(self, filepath: str) -> bool:
        """
        Exporta los gastos a un archivo CSV específico
        
        Args:
            filepath: Ruta del archivo de destino
            
        Returns:
            True si se exportó correctamente
        """
        try:
            df = self.load_expenses()
            df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False
    
    def import_from_csv(self, filepath: str) -> bool:
        """
        Importa gastos desde un archivo CSV
        
        Args:
            filepath: Ruta del archivo a importar
            
        Returns:
            True si se importó correctamente
        """
        try:
            new_df = pd.read_csv(filepath)
            
            # Validar columnas requeridas
            required_cols = ['monto', 'categoria', 'descripcion']
            if not all(col in new_df.columns for col in required_cols):
                return False
            
            # Agregar cada gasto
            for _, row in new_df.iterrows():
                fecha = pd.to_datetime(row.get('fecha', datetime.now()))
                texto_original = row.get('texto_original', row['descripcion'])
                
                self.add_expense(
                    monto=row['monto'],
                    categoria=row['categoria'],
                    descripcion=row['descripcion'],
                    texto_original=texto_original,
                    fecha=fecha
                )
            
            return True
        except Exception as e:
            print(f"Error al importar: {e}")
            return False
