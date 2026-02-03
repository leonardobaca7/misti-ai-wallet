"""
Módulo de procesamiento de lenguaje natural para extraer información de gastos
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any


class ExpenseProcessor:
    """
    Clase para procesar texto en lenguaje natural y extraer información de gastos
    """
    
    def __init__(self):
        """
        Inicializa el procesador con categorías y palabras clave
        """
        self.categories = {
            'alimentacion': [
                'adobo', 'almuerzo', 'cena', 'desayuno', 'comida', 'restaurante',
                'menu', 'pollo', 'ceviche', 'pizza', 'hamburguesa', 'sushi',
                'cafe', 'té', 'bebida', 'bocadillo', 'snack', 'mercado',
                'supermercado', 'verduras', 'frutas', 'carne', 'pescado',
                'arroz', 'pan', 'leche', 'huevos', 'comestibles', 'groceries'
            ],
            'transporte': [
                'gasolina', 'combustible', 'taxi', 'uber', 'bus', 'combi',
                'metro', 'pasaje', 'transporte', 'peaje', 'estacionamiento',
                'parking', 'carro', 'auto', 'moto', 'bicicleta', 'scooter',
                'lavado', 'mantenimiento', 'mecanico', 'repuestos'
            ],
            'entretenimiento': [
                'cine', 'pelicula', 'teatro', 'concierto', 'fiesta', 'bar',
                'discoteca', 'club', 'juego', 'videojuego', 'streaming',
                'netflix', 'spotify', 'amazon prime', 'disney', 'hbo',
                'youtube', 'suscripcion', 'membresía', 'hobby', 'deporte',
                'gimnasio', 'gym', 'entrenamiento', 'yoga'
            ],
            'salud': [
                'medicina', 'farmacia', 'doctor', 'medico', 'consulta',
                'hospital', 'clinica', 'dentista', 'odontologo', 'terapia',
                'psicologo', 'psiquiatra', 'analisis', 'examen', 'laboratorio',
                'radiografia', 'seguro', 'vitaminas', 'tratamiento',
                'pastillas', 'jarabe', 'inyeccion'
            ],
            'educacion': [
                'libro', 'libros', 'curso', 'clase', 'universidad', 'colegio',
                'escuela', 'academia', 'tutor', 'profesor', 'matricula',
                'pension', 'material', 'utiles', 'cuaderno', 'lapiz',
                'mochila', 'laptop', 'tablet', 'software', 'licencia',
                'certificacion', 'seminario', 'workshop', 'capacitacion'
            ],
            'servicios': [
                'luz', 'agua', 'gas', 'internet', 'telefono', 'celular',
                'cable', 'electricidad', 'recibo', 'factura', 'servicio',
                'alquiler', 'renta', 'arrendamiento', 'mantenimiento',
                'reparacion', 'limpieza', 'lavanderia', 'tintoreria',
                'peluqueria', 'salon', 'barberia', 'corte', 'spa'
            ],
            'compras': [
                'ropa', 'zapatos', 'zapatillas', 'camisa', 'pantalon',
                'vestido', 'falda', 'abrigo', 'chompa', 'sweater',
                'tienda', 'mall', 'centro comercial', 'online', 'amazon',
                'mercado libre', 'compra', 'regalo', 'electronico',
                'computadora', 'celular', 'audifonos', 'mouse', 'teclado',
                'monitor', 'mueble', 'decoracion', 'electrodomestico'
            ]
        }
        
        # Patrones para detectar montos
        self.amount_patterns = [
            r'(\d+(?:\.\d{1,2})?)\s*(?:soles?|s/|pen)',
            r's/\s*(\d+(?:\.\d{1,2})?)',
            r'(\d+(?:\.\d{1,2})?)\s*(?:sol|soles)',
            r'(\d+(?:\.\d{1,2})?)',  # Solo números como último recurso
        ]
        
        # Palabras que indican un gasto
        self.expense_indicators = [
            'gasté', 'gaste', 'pague', 'pagué', 'compré', 'compre',
            'me gaste', 'me gasté', 'costo', 'costó', 'salió',
            'pago', 'pagó', 'invertí', 'inverti', 'di'
        ]
        
        # Palabras que indican un ingreso
        self.income_indicators = [
            'gané', 'gane', 'cobré', 'cobre', 'recibí', 'recibi',
            'me pagaron', 'ingreso', 'ganancia', 'salario', 'sueldo',
            'pago', 'honorarios', 'bono', 'propina', 'venta', 'vendí',
            'vendi', 'ingresó', 'ingreso', 'me dieron', 'transferencia'
        ]
    
    def process_expense(self, text: str) -> Dict[str, Any]:
        """
        Procesa un texto en lenguaje natural y extrae la información del gasto
        
        Args:
            text: Texto en lenguaje natural describiendo el gasto
            
        Returns:
            Diccionario con la información extraída:
            - success: bool indicando si el procesamiento fue exitoso
            - monto: float con el monto del gasto
            - categoria: str con la categoría detectada
            - descripcion: str con la descripción del gasto
            - fecha: datetime con la fecha del gasto
            - message: str con un mensaje de error si hubo algún problema
        """
        text_lower = text.lower().strip()
        
        # Extraer el monto
        monto = self._extract_amount(text_lower)
        if monto is None:
            return {
                'success': False,
                'message': 'No se pudo detectar un monto en el texto. Por favor incluye el precio.'
            }
        
        # Detectar la fecha
        fecha = self._extract_date(text_lower)
        
        # Detectar si es gasto o ingreso
        tipo = self._detect_type(text_lower)
        
        # Detectar la categoría
        categoria = self._detect_category(text_lower)
        
        # Generar descripción
        descripcion = self._generate_description(text, monto)
        
        return {
            'success': True,
            'monto': monto,
            'categoria': categoria,
            'descripcion': descripcion,
            'fecha': fecha,
            'tipo': tipo,
            'message': 'Gasto procesado exitosamente'
        }
    
    def _extract_amount(self, text: str) -> float:
        """
        Extrae el monto del texto
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            Monto como float o None si no se encuentra
        """
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    # Tomar el primer match válido
                    amount = float(matches[0])
                    if amount > 0:
                        return amount
                except (ValueError, IndexError):
                    continue
        return None
    
    def _extract_date(self, text: str) -> datetime:
        """
        Extrae la fecha del texto, detectando fechas relativas
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            Fecha como datetime (por defecto hoy si no se detecta)
        """
        hoy = datetime.now()
        
        # Detectar "ayer"
        if 'ayer' in text:
            return hoy - timedelta(days=1)
        
        # Detectar "anteayer" o "antier"
        if 'anteayer' in text or 'antier' in text:
            return hoy - timedelta(days=2)
        
        # Detectar "hace X días"
        match = re.search(r'hace\s+(\d+)\s+d[ií]as?', text)
        if match:
            dias = int(match.group(1))
            return hoy - timedelta(days=dias)
        
        # Detectar "hace X semanas"
        match = re.search(r'hace\s+(\d+)\s+semanas?', text)
        if match:
            semanas = int(match.group(1))
            return hoy - timedelta(weeks=semanas)
        
        # Detectar "la semana pasada"
        if 'semana pasada' in text:
            return hoy - timedelta(weeks=1)
        
        # Detectar "el lunes", "el martes", etc. (asume la semana actual o pasada)
        dias_semana = {
            'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2,
            'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5, 'domingo': 6
        }
        for dia_nombre, dia_num in dias_semana.items():
            if dia_nombre in text:
                dias_hasta_dia = (hoy.weekday() - dia_num) % 7
                if dias_hasta_dia == 0:
                    dias_hasta_dia = 7  # Si es hoy, asumir semana pasada
                return hoy - timedelta(days=dias_hasta_dia)
        
        # Detectar fechas específicas como "15/01", "15 de enero", etc.
        # Formato DD/MM o DD-MM
        match = re.search(r'(\d{1,2})[/-](\d{1,2})', text)
        if match:
            dia = int(match.group(1))
            mes = int(match.group(2))
            try:
                fecha = datetime(hoy.year, mes, dia)
                # Si la fecha es futura, asumir año pasado
                if fecha > hoy:
                    fecha = datetime(hoy.year - 1, mes, dia)
                return fecha
            except ValueError:
                pass
        
        # Si no se detecta ninguna fecha especial, retornar hoy
        return hoy
    
    def _detect_type(self, text: str) -> str:
        """
        Detecta si el texto describe un gasto o un ingreso
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            'gasto' o 'ingreso'
        """
        # Contar indicadores de ingreso
        income_score = sum(1 for indicator in self.income_indicators if indicator in text)
        
        # Contar indicadores de gasto
        expense_score = sum(1 for indicator in self.expense_indicators if indicator in text)
        
        # Si hay más indicadores de ingreso, es un ingreso
        if income_score > expense_score:
            return 'ingreso'
        
        # Por defecto, asumir que es un gasto
        return 'gasto'
    
    def _detect_category(self, text: str) -> str:
        """
        Detecta la categoría del gasto basándose en palabras clave
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            Nombre de la categoría detectada o 'otros' si no se detecta ninguna
        """
        # Contar coincidencias por categoría
        category_scores = {}
        
        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Dar más peso a palabras más largas (más específicas)
                    score += len(keyword)
            category_scores[category] = score
        
        # Retornar la categoría con mayor puntuación
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        
        return 'otros'
    
    def _generate_description(self, text: str, monto: float) -> str:
        """
        Genera una descripción limpia del gasto
        
        Args:
            text: Texto original
            monto: Monto extraído
            
        Returns:
            Descripción del gasto
        """
        # Limpiar el texto
        description = text.strip()
        
        # Remover referencias al monto para evitar redundancia
        monto_str = str(monto)
        description = re.sub(rf'\b{monto_str}\b', '', description, flags=re.IGNORECASE)
        description = re.sub(r's/\s*\d+(?:\.\d{1,2})?', '', description, flags=re.IGNORECASE)
        description = re.sub(r'\d+(?:\.\d{1,2})?\s*(?:soles?|s/|pen)', '', description, flags=re.IGNORECASE)
        
        # Remover palabras indicadoras comunes
        for indicator in self.expense_indicators:
            description = description.replace(indicator, '')
        
        # Limpiar espacios extras y palabras comunes al inicio
        description = re.sub(r'\s+', ' ', description).strip()
        description = description.lstrip('en de ')
        
        # Capitalizar primera letra
        if description:
            description = description[0].upper() + description[1:]
        else:
            description = "Gasto sin descripción específica"
        
        return description
    
    def get_categories(self) -> list:
        """
        Retorna la lista de categorías disponibles
        
        Returns:
            Lista de nombres de categorías
        """
        return list(self.categories.keys()) + ['otros']
    
    def add_category_keyword(self, category: str, keyword: str):
        """
        Agrega una palabra clave a una categoría existente
        
        Args:
            category: Nombre de la categoría
            keyword: Palabra clave a agregar
        """
        if category in self.categories:
            if keyword.lower() not in self.categories[category]:
                self.categories[category].append(keyword.lower())
        else:
            raise ValueError(f"La categoría '{category}' no existe")
