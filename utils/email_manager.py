"""
Sistema de notificaciones por email para Misti AI Wallet
Envía resúmenes mensuales automáticos a los usuarios
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


class EmailManager:
    """Gestor de notificaciones por email"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Inicializa el gestor de emails
        
        Args:
            smtp_server: Servidor SMTP (por defecto Gmail)
            smtp_port: Puerto SMTP (587 para TLS)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def _create_monthly_summary_html(self, user_data: Dict, stats: Dict) -> str:
        """
        Crea el HTML para el resumen mensual
        
        Args:
            user_data: Información del usuario
            stats: Estadísticas del mes
            
        Returns:
            HTML formateado del email
        """
        month_name = stats['month_name']
        year = stats['year']
        
        # Colores neón para el email
        cyan = '#00d4ff'
        green = '#00ff88'
        red = '#ff5252'
        purple = '#7a5af8'
        
        balance_color = green if stats['balance'] >= 0 else red
        balance_icon = '📈' if stats['balance'] >= 0 else '📉'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                    color: #e0e0e0;
                    padding: 20px;
                    margin: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: rgba(20, 20, 20, 0.9);
                    border-radius: 20px;
                    border: 1px solid rgba(0, 212, 255, 0.3);
                    overflow: hidden;
                    box-shadow: 0 20px 60px rgba(0, 212, 255, 0.2);
                }}
                .header {{
                    background: linear-gradient(135deg, {cyan} 0%, {purple} 100%);
                    padding: 30px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2rem;
                    font-weight: 700;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 1.1rem;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 30px;
                }}
                .greeting {{
                    font-size: 1.2rem;
                    margin-bottom: 20px;
                    color: {cyan};
                }}
                .metrics {{
                    display: flex;
                    gap: 15px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    flex: 1;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .metric-card.green {{
                    background: rgba(0, 255, 136, 0.1);
                    border-color: rgba(0, 255, 136, 0.3);
                }}
                .metric-card.red {{
                    background: rgba(255, 82, 82, 0.1);
                    border-color: rgba(255, 82, 82, 0.3);
                }}
                .metric-card.cyan {{
                    background: rgba(0, 212, 255, 0.1);
                    border-color: rgba(0, 212, 255, 0.3);
                }}
                .metric-card .icon {{
                    font-size: 2rem;
                    margin-bottom: 10px;
                }}
                .metric-card .label {{
                    font-size: 0.85rem;
                    color: #888;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    font-weight: 600;
                    margin-bottom: 5px;
                }}
                .metric-card .value {{
                    font-size: 1.8rem;
                    font-weight: 700;
                }}
                .metric-card.green .value {{ color: {green}; }}
                .metric-card.red .value {{ color: {red}; }}
                .metric-card.cyan .value {{ color: {balance_color}; }}
                .categories {{
                    margin: 30px 0;
                }}
                .categories h3 {{
                    color: {purple};
                    margin-bottom: 15px;
                }}
                .category-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 12px;
                    margin: 8px 0;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                    border-left: 3px solid {cyan};
                }}
                .category-name {{
                    font-weight: 600;
                }}
                .category-amount {{
                    color: {cyan};
                    font-weight: 700;
                }}
                .footer {{
                    margin-top: 30px;
                    padding: 20px;
                    text-align: center;
                    background: rgba(0, 0, 0, 0.3);
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    color: #888;
                    font-size: 0.9rem;
                }}
                .cta-button {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 15px 30px;
                    background: linear-gradient(135deg, {cyan} 0%, {purple} 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-weight: 700;
                    box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Misti AI Wallet</h1>
                    <p>Resumen Mensual - {month_name} {year}</p>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        ¡Hola {user_data['full_name']}! 👋
                    </div>
                    
                    <p>Aquí está tu resumen financiero de <strong>{month_name} {year}</strong>:</p>
                    
                    <div class="metrics">
                        <div class="metric-card green">
                            <div class="icon">💰</div>
                            <div class="label">Ingresos</div>
                            <div class="value">S/ {stats['total_ingresos']:,.2f}</div>
                        </div>
                        
                        <div class="metric-card red">
                            <div class="icon">💸</div>
                            <div class="label">Gastos</div>
                            <div class="value">S/ {stats['total_gastos']:,.2f}</div>
                        </div>
                    </div>
                    
                    <div class="metric-card cyan" style="margin: 20px 0;">
                        <div class="icon">{balance_icon}</div>
                        <div class="label">Balance Final</div>
                        <div class="value">S/ {stats['balance']:,.2f}</div>
                    </div>
                    
                    <div class="categories">
                        <h3>📊 Top Categorías de Gastos</h3>
        """
        
        # Agregar categorías
        for cat in stats['top_categories'][:5]:
            html += f"""
                        <div class="category-item">
                            <span class="category-name">{cat['emoji']} {cat['categoria'].title()}</span>
                            <span class="category-amount">S/ {cat['monto']:,.2f}</span>
                        </div>
            """
        
        html += f"""
                    </div>
                    
                    <p style="margin-top: 30px; color: #b0b0b0; text-align: center;">
                        📝 Registraste <strong>{stats['num_transacciones']}</strong> transacciones este mes
                    </p>
                    
                    <div style="text-align: center;">
                        <a href="#" class="cta-button">Ver Detalles Completos →</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Este es un mensaje automático de Misti AI Wallet</p>
                    <p>💡 Gestiona tus finanzas de forma inteligente</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_monthly_summary(self, 
                            sender_email: str, 
                            sender_password: str,
                            recipient_email: str,
                            user_data: Dict,
                            stats: Dict) -> Dict:
        """
        Envía un resumen mensual por email
        
        Args:
            sender_email: Email del remitente (cuenta de Gmail)
            sender_password: Contraseña de aplicación de Gmail
            recipient_email: Email del destinatario
            user_data: Información del usuario
            stats: Estadísticas del mes
            
        Returns:
            Dict con resultado del envío
        """
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = f"📊 Resumen de {stats['month_name']} - Misti AI Wallet"
            message["From"] = sender_email
            message["To"] = recipient_email
            
            # Crear HTML
            html = self._create_monthly_summary_html(user_data, stats)
            html_part = MIMEText(html, "html")
            message.attach(html_part)
            
            # Enviar email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
            
            return {
                'success': True,
                'message': f'Resumen enviado exitosamente a {recipient_email}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al enviar email: {str(e)}'
            }
    
    def calculate_monthly_stats(self, 
                                df: pd.DataFrame, 
                                month: Optional[int] = None,
                                year: Optional[int] = None) -> Dict:
        """
        Calcula estadísticas mensuales de un DataFrame
        
        Args:
            df: DataFrame con transacciones
            month: Mes a analizar (None = mes anterior)
            year: Año a analizar (None = año actual)
            
        Returns:
            Dict con estadísticas del mes
        """
        # Si no se especifica mes, usar el mes anterior
        if month is None or year is None:
            now = datetime.now()
            if now.month == 1:
                month = 12
                year = now.year - 1
            else:
                month = now.month - 1
                year = now.year
        
        # Nombres de meses
        month_names = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        # Filtrar por mes y año
        df['fecha'] = pd.to_datetime(df['fecha'])
        month_df = df[(df['fecha'].dt.month == month) & (df['fecha'].dt.year == year)]
        
        # Separar gastos e ingresos
        gastos_df = month_df[month_df['tipo'] == 'gasto']
        ingresos_df = month_df[month_df['tipo'] == 'ingreso']
        
        # Calcular totales
        total_gastos = gastos_df['monto'].sum() if not gastos_df.empty else 0
        total_ingresos = ingresos_df['monto'].sum() if not ingresos_df.empty else 0
        balance = total_ingresos - total_gastos
        
        # Top categorías de gastos
        category_emoji = {
            'alimentacion': '🍽️',
            'transporte': '🚗',
            'entretenimiento': '🎮',
            'salud': '⚕️',
            'educacion': '📚',
            'servicios': '💡',
            'compras': '🛍️',
            'otros': '📦'
        }
        
        top_categories = []
        if not gastos_df.empty:
            cat_summary = gastos_df.groupby('categoria')['monto'].sum().sort_values(ascending=False)
            for cat, monto in cat_summary.items():
                top_categories.append({
                    'categoria': cat,
                    'monto': monto,
                    'emoji': category_emoji.get(cat, '📦')
                })
        
        return {
            'month': month,
            'year': year,
            'month_name': month_names[month - 1],
            'total_gastos': total_gastos,
            'total_ingresos': total_ingresos,
            'balance': balance,
            'num_transacciones': len(month_df),
            'top_categories': top_categories
        }
    
    def send_monthly_summaries_to_all_users(self,
                                           sender_email: str,
                                           sender_password: str,
                                           users: List[Dict],
                                           data_manager) -> List[Dict]:
        """
        Envía resúmenes mensuales a todos los usuarios con email
        
        Args:
            sender_email: Email del remitente
            sender_password: Contraseña de aplicación
            users: Lista de usuarios
            data_manager: Instancia de DataManager para cargar datos
            
        Returns:
            Lista con resultados del envío
        """
        results = []
        
        for user in users:
            # Solo enviar a usuarios con email registrado
            if user.get('email') and '@' in user['email']:
                # Cargar transacciones del usuario
                df = data_manager.load_expenses(usuario=user['username'])
                
                if not df.empty:
                    # Calcular estadísticas
                    stats = self.calculate_monthly_stats(df)
                    
                    # Enviar email
                    result = self.send_monthly_summary(
                        sender_email=sender_email,
                        sender_password=sender_password,
                        recipient_email=user['email'],
                        user_data=user,
                        stats=stats
                    )
                    
                    results.append({
                        'user': user['username'],
                        'email': user['email'],
                        'result': result
                    })
        
        return results


if __name__ == "__main__":
    # Test del módulo
    print("📧 Email Manager para Misti AI Wallet")
    print("Módulo de notificaciones por email")
