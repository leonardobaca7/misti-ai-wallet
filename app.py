import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import time
import importlib
import sys

# Forzar recarga de módulos para desarrollo
if 'utils.user_manager' in sys.modules:
    importlib.reload(sys.modules['utils.user_manager'])
if 'utils.nlp_processor' in sys.modules:
    importlib.reload(sys.modules['utils.nlp_processor'])
if 'utils.data_manager' in sys.modules:
    importlib.reload(sys.modules['utils.data_manager'])
if 'utils.email_manager' in sys.modules:
    importlib.reload(sys.modules['utils.email_manager'])

from utils.nlp_processor import ExpenseProcessor
from utils.data_manager import DataManager
from utils.user_manager import UserManager
from utils.email_manager import EmailManager

# Configuración de la página
# Version: 1.0.1 - Fixed empty DataFrame handling
st.set_page_config(
    page_title="Misti AI Wallet",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados - DARK MODE PROFESIONAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ========== DARK MODE - CONFIGURACIÓN GLOBAL ========== */
    
    /* Fuente global */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Fondo principal oscuro */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* Main container */
    .main .block-container {
        background-color: #0a0a0a;
        padding-top: 2rem;
    }
    
    /* Header principal estilo dark */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* ========== TARJETAS DARK MODE ========== */
    
    /* Tarjetas de métricas estilo glassmorphism oscuro */
    .metric-card {
        background: rgba(30, 30, 35, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    }
    
    /* Tarjetas de gastos oscuras */
    .expense-card {
        background: rgba(25, 25, 30, 0.6);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 3px solid #00d4ff;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .expense-card:hover {
        border: 1px solid rgba(0, 212, 255, 0.3);
        box-shadow: 0 8px 24px rgba(0, 212, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* ========== BOTONES DARK MODE ========== */
    
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        color: white;
        padding: 0.6rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00e5ff 0%, #8b6bff 100%);
    }
    
    /* Input estilo dark */
    .stTextInput>div>div>input {
        background-color: rgba(30, 30, 35, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px;
        font-size: 1rem;
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
        background-color: rgba(30, 30, 35, 0.8);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #666;
    }
    
    /* ========== TABS DARK MODE ========== */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(20, 20, 25, 0.8);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        color: #888;
        transition: all 0.3s ease;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #bbb;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    /* ========== SIDEBAR DARK MODE ========== */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151518 0%, #1a1a1f 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] label {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* ========== SELECTBOX Y OTROS INPUTS ========== */
    
    .stSelectbox>div>div {
        background-color: rgba(30, 30, 35, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #e0e0e0;
    }
    
    .stSelectbox>div>div:hover {
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    /* Date input */
    .stDateInput>div>div>input {
        background-color: rgba(30, 30, 35, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
    }
    
    /* ========== DATAFRAME DARK MODE ========== */
    
    .stDataFrame {
        background-color: rgba(20, 20, 25, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Headers de dataframe */
    .stDataFrame thead tr th {
        background-color: rgba(30, 30, 35, 0.8) !important;
        color: #00d4ff !important;
        font-weight: 600;
    }
    
    .stDataFrame tbody tr {
        background-color: rgba(20, 20, 25, 0.4);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stDataFrame tbody tr:hover {
        background-color: rgba(30, 30, 35, 0.6);
    }
    
    /* ========== ANIMACIONES ========== */
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.6); }
    }
    
    .animated {
        animation: slideIn 0.5s ease-out;
    }
    
    /* ========== TARJETAS DE EJEMPLO DARK ========== */
    
    .example-card {
        background: rgba(30, 30, 35, 0.4);
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 0.5rem;
    }
    
    .example-card:hover {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.1);
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
    }
    
    /* ========== MENSAJES Y ALERTAS ========== */
    
    .stAlert {
        background-color: rgba(30, 30, 35, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #e0e0e0;
    }
    
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.1);
        border-left: 4px solid #00ff88;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
    }
    
    .stError {
        background-color: rgba(255, 82, 82, 0.1);
        border-left: 4px solid #ff5252;
    }
    
    /* ========== BADGES Y PILLS ========== */
    
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
    }
    
    .badge-cyan { background: rgba(0, 212, 255, 0.2); color: #00d4ff; }
    .badge-purple { background: rgba(122, 90, 248, 0.2); color: #7a5af8; }
    .badge-pink { background: rgba(255, 105, 180, 0.2); color: #ff69b4; }
    .badge-green { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
    
    /* ========== UTILIDADES ========== */
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scroll personalizado */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 25, 0.4);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 212, 255, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 212, 255, 0.5);
    }
    
    /* Mejorar contraste de texto */
    p, span, div {
        color: #d0d0d0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #e8e8e8;
    }
    
    </style>
""", unsafe_allow_html=True)

# Inicializar procesador y gestor de datos
# NO usar cache para que siempre recargue los datos
def init_components():
    processor = ExpenseProcessor()
    data_manager = DataManager()
    user_manager = UserManager()
    email_manager = EmailManager()
    return processor, data_manager, user_manager, email_manager

processor, data_manager, user_manager, email_manager = init_components()

# ========== SISTEMA DE LOGIN / REGISTRO ==========
# Inicializar estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Si no está logueado, mostrar pantalla de login
if not st.session_state.logged_in:
    st.markdown('<div class="main-header">💰 Misti AI Wallet</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">🔐 Sistema Multi-Usuario</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Crear tabs para login y registro
    tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "✨ Crear Cuenta"])
    
    with tab1:
        st.markdown("### 👤 Ingresa a tu cuenta")
        st.markdown("")
        
        login_username = st.text_input(
            "Nombre de usuario:",
            placeholder="Ej: juan_perez",
            key="login_user"
        )
        
        login_password = st.text_input(
            "Contraseña:",
            type="password",
            placeholder="Ingresa tu contraseña",
            key="login_pass"
        )
        
        if st.button("🚀 Ingresar", type="primary", use_container_width=True):
            if login_username and login_password:
                result = user_manager.login_user(login_username, login_password)
                if result['success']:
                    st.session_state.logged_in = True
                    st.session_state.current_user = result['user']
                    st.success(result['message'])
                    st.balloons()
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("⚠️ Por favor completa todos los campos")
    
    with tab2:
        st.markdown("### ✨ Crea tu cuenta nueva")
        st.markdown("")
        
        new_username = st.text_input(
            "Nombre de usuario:",
            placeholder="Ej: juan_perez",
            key="reg_user",
            help="Será tu identificador único"
        )
        
        new_fullname = st.text_input(
            "Nombre completo:",
            placeholder="Ej: Juan Pérez",
            key="reg_name"
        )
        
        new_email = st.text_input(
            "Email:",
            placeholder="Ej: juan@email.com",
            key="reg_email",
            help="Para recibir recordatorios y resúmenes mensuales"
        )
        
        new_password = st.text_input(
            "Contraseña:",
            type="password",
            placeholder="Mínimo 4 caracteres",
            key="reg_pass"
        )
        
        new_password_confirm = st.text_input(
            "Confirmar contraseña:",
            type="password",
            placeholder="Repite tu contraseña",
            key="reg_pass_confirm"
        )
        
        if st.button("🎉 Crear Mi Cuenta", type="primary", use_container_width=True):
            if new_username and new_fullname and new_email and new_password and new_password_confirm:
                if new_password != new_password_confirm:
                    st.error("❌ Las contraseñas no coinciden")
                else:
                    result = user_manager.register_user(new_username, new_fullname, new_email, new_password)
                    if result['success']:
                        st.success(result['message'])
                        st.balloons()
                        # Auto-login después de registro
                        st.session_state.logged_in = True
                        st.session_state.current_user = result['user']
                        st.rerun()
                    else:
                        st.error(result['message'])
            else:
                st.warning("⚠️ Por favor completa todos los campos requeridos")
    
    st.stop()  # Detener ejecución hasta que se loguee

# ========== USUARIO LOGUEADO - APLICACIÓN PRINCIPAL ==========

# Header Dark Mode
st.markdown('<div class="main-header">💰 Misti AI Wallet</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🤖 Tu asistente inteligente de finanzas personales con IA</div>', unsafe_allow_html=True)

# Sidebar Dark Mode con Perfil de Usuario Logueado
with st.sidebar:
    # Mostrar información del usuario logueado
    current_user = st.session_state.current_user
    
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem 0 0.5rem 0;'>
            <div style='background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
                        width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 1rem;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 3rem; box-shadow: 0 8px 32px rgba(0, 212, 255, 0.4);'>
                👤
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: rgba(0, 212, 255, 0.1);
                    border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3);
                    margin-bottom: 1rem;'>
            <h3 style='color: #00d4ff; margin: 0; font-size: 1.2rem;'>¡Hola, {current_user['full_name']}!</h3>
            <p style='color: #888; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>@{current_user['username']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón de cerrar sesión
    if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    st.markdown("")
    
    # Filtros con estilo dark
    st.markdown("<div style='color: #00d4ff; font-weight: 600; font-size: 0.9rem; margin-bottom: 1rem;'>📅 FILTROS</div>", unsafe_allow_html=True)
    
    # Cargar datos del usuario actual
    df = data_manager.load_expenses(usuario=current_user['username'])
    
    # Botón de refrescar prominente
    if st.button("🔄 Actualizar Datos", type="primary", use_container_width=True):
        st.rerun()
    
    if not df.empty:
        # Filtro de fechas
        date_range = st.date_input(
            "Rango de fechas",
            value=(df['fecha'].min(), df['fecha'].max()),
            min_value=df['fecha'].min(),
            max_value=df['fecha'].max()
        )
        
        # Filtro de categorías
        categories = ['Todas'] + sorted(df['categoria'].unique().tolist())
        selected_category = st.selectbox("Categoría", categories)
    
    st.markdown("---")
    
    # Configuración de Emails/Notificaciones
    st.markdown("### 📧 Notificaciones")
    st.markdown("")
    
    with st.expander("⚙️ Configurar Email", expanded=False):
        st.markdown("**Configura tu email de Gmail para recibir resúmenes mensuales**")
        st.markdown("")
        
        gmail_user = st.text_input(
            "Tu email de Gmail:",
            value="",
            placeholder="tu_email@gmail.com",
            key="gmail_user",
            help="Email desde donde se enviarán las notificaciones"
        )
        
        gmail_password = st.text_input(
            "Contraseña de aplicación:",
            type="password",
            placeholder="xxxx xxxx xxxx xxxx",
            key="gmail_password",
            help="Genera una contraseña de aplicación en: myaccount.google.com/apppasswords"
        )
        
        st.markdown("---")
        
        if gmail_user and gmail_password and current_user.get('email'):
            if st.button("📊 Enviar Resumen del Mes Anterior", type="primary", use_container_width=True):
                with st.spinner("📤 Enviando resumen..."):
                    # Calcular estadísticas del mes anterior
                    stats = email_manager.calculate_monthly_stats(df)
                    
                    # Enviar email
                    result = email_manager.send_monthly_summary(
                        sender_email=gmail_user,
                        sender_password=gmail_password,
                        recipient_email=current_user['email'],
                        user_data=current_user,
                        stats=stats
                    )
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        st.balloons()
                    else:
                        st.error(f"❌ {result['message']}")
        else:
            st.info("💡 Completa tu email en el perfil y configura Gmail para recibir resúmenes")
    
    st.markdown("---")
    
    # Opciones adicionales con iconos mejorados
    st.markdown("### ⚙️ Opciones")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Limpiar", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_delete', False):
                data_manager.clear_all_data()
                st.success("✅ Eliminado")
                st.session_state.confirm_delete = False
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("⚠️ Confirmar")
    
    with col2:
        if st.button("📥 Exportar", type="secondary", use_container_width=True):
            if not df.empty:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ CSV",
                    data=csv,
                    file_name=f"gastos_misti_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Main content
tab1, tab2, tab3 = st.tabs(["� Nueva Transacción", "📊 Dashboard", "📋 Historial"])

# Tab 1: Nueva Transacción (Gastos e Ingresos)
with tab1:
    # Contenedor principal con animación
    st.markdown('<div class="animated">', unsafe_allow_html=True)
    
    # Header personalizado con nombre del usuario
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"### 💬 {current_user['full_name']}, cuéntame en qué gastaste o ganaste")
        st.markdown("Escribe de forma natural: gastos o ingresos")
    
    st.markdown("")
    
    # Input principal más grande y prominente
    expense_text = st.text_input(
        "Tu transacción:",
        placeholder='Ej: "Gasté 15 soles en un adobo" o "Cobré 500 soles de mi sueldo" o "Pagué 50 soles de gasolina ayer"',
        help="💡 Escribe como hablas normalmente. La IA entiende gastos E ingresos automáticamente",
        label_visibility="collapsed"
    )
    
    # Botón centrado y destacado
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        process_button = st.button("✨ Procesar con IA", type="primary", use_container_width=True)
    
    if process_button and expense_text:
        with st.spinner("🤖 Analizando con Inteligencia Artificial..."):
            result = processor.process_expense(expense_text)
            
            if result['success']:
                # Mensaje de éxito dark mode
                st.markdown("""
                    <div style='background: rgba(0, 212, 255, 0.15); 
                                padding: 1.5rem; border-radius: 16px; text-align: center;
                                border: 1px solid rgba(0, 212, 255, 0.3);
                                box-shadow: 0 10px 40px rgba(0, 212, 255, 0.3); margin: 2rem 0;'>
                        <h2 style='margin: 0; font-size: 1.8rem; color: #00d4ff;'>✅ ¡Gasto Registrado con Éxito!</h2>
                        <p style='margin: 0.5rem 0 0 0; color: #b0b0b0;'>Tu información ha sido procesada por IA</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
                
                # Métricas con diseño mejorado
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div style='background: rgba(0, 212, 255, 0.12);
                                    padding: 1.8rem; border-radius: 16px; text-align: center;
                                    border: 1px solid rgba(0, 212, 255, 0.3);
                                    box-shadow: 0 8px 32px rgba(0, 212, 255, 0.25);'>
                            <div style='font-size: 3rem; margin-bottom: 0.8rem;'>💵</div>
                            <div style='font-size: 0.8rem; color: #888; font-weight: 600; letter-spacing: 1.5px;'>MONTO</div>
                            <div style='font-size: 2.2rem; font-weight: 800; color: #00d4ff; margin-top: 0.5rem;'>S/ {result['monto']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    emoji_map = {
                        'alimentacion': '🍽️',
                        'transporte': '🚗',
                        'entretenimiento': '🎮',
                        'salud': '⚕️',
                        'educacion': '📚',
                        'servicios': '💡',
                        'compras': '🛍️',
                        'otros': '📦'
                    }
                    emoji = emoji_map.get(result['categoria'], '📦')
                    st.markdown(f"""
                        <div style='background: rgba(122, 90, 248, 0.12);
                                    padding: 1.8rem; border-radius: 16px; text-align: center;
                                    border: 1px solid rgba(122, 90, 248, 0.3);
                                    box-shadow: 0 8px 32px rgba(122, 90, 248, 0.25);'>
                            <div style='font-size: 3rem; margin-bottom: 0.8rem;'>{emoji}</div>
                            <div style='font-size: 0.8rem; color: #888; font-weight: 600; letter-spacing: 1.5px;'>CATEGORÍA</div>
                            <div style='font-size: 1.6rem; font-weight: 800; color: #7a5af8; margin-top: 0.5rem;'>{result['categoria'].title()}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    fecha_detectada = result.get('fecha', datetime.now())
                    fecha_str = fecha_detectada.strftime("%d/%m/%Y")
                    
                    # Mensaje especial si detectó una fecha distinta a hoy
                    if fecha_detectada.date() != datetime.now().date():
                        diferencia = (datetime.now().date() - fecha_detectada.date()).days
                        if diferencia == 1:
                            extra_msg = "(ayer)"
                        elif diferencia == 2:
                            extra_msg = "(anteayer)"
                        else:
                            extra_msg = f"(hace {diferencia} días)"
                    else:
                        extra_msg = "(hoy)"
                    
                    st.markdown(f"""
                        <div style='background: rgba(0, 255, 136, 0.12);
                                    padding: 1.8rem; border-radius: 16px; text-align: center;
                                    border: 1px solid rgba(0, 255, 136, 0.3);
                                    box-shadow: 0 8px 32px rgba(0, 255, 136, 0.25);'>
                            <div style='font-size: 3rem; margin-bottom: 0.8rem;'>📅</div>
                            <div style='font-size: 0.8rem; color: #888; font-weight: 600; letter-spacing: 1.5px;'>FECHA</div>
                            <div style='font-size: 1.6rem; font-weight: 800; color: #00ff88; margin-top: 0.5rem;'>{fecha_str}</div>
                            <div style='font-size: 0.9rem; color: #888; margin-top: 0.3rem;'>{extra_msg}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Descripción dark mode
                st.markdown(f"""
                    <div style='background: rgba(30, 30, 35, 0.6); padding: 1.5rem; border-radius: 14px; 
                                border-left: 4px solid #00d4ff; border: 1px solid rgba(0, 212, 255, 0.2);
                                box-shadow: 0 4px 20px rgba(0, 212, 255, 0.15);'>
                        <div style='font-size: 0.85rem; color: #00d4ff; font-weight: 600; margin-bottom: 0.5rem; letter-spacing: 1px;'>
                            📝 DESCRIPCIÓN GENERADA POR IA
                        </div>
                        <div style='font-size: 1.1rem; color: #d0d0d0; line-height: 1.6;'>
                            {result['descripcion']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Guardar el gasto/ingreso con la fecha detectada y usuario
                tipo = result.get('tipo', 'gasto')
                data_manager.add_expense(
                    monto=result['monto'],
                    categoria=result['categoria'],
                    descripcion=result['descripcion'],
                    texto_original=expense_text,
                    fecha=result.get('fecha', datetime.now()),
                    usuario=current_user['username'],
                    tipo=tipo
                )
                
                st.balloons()
                
                # Mensaje según tipo
                tipo_msg = "💰 Ingreso registrado" if tipo == 'ingreso' else "✅ Gasto guardado"
                st.success(f"{tipo_msg}. Actualizando dashboard...")
                import time
                time.sleep(1.5)
                st.rerun()
            else:
                st.markdown("""
                    <div style='background: rgba(255, 82, 82, 0.15); 
                                padding: 1.5rem; border-radius: 16px;
                                border: 1px solid rgba(255, 82, 82, 0.3);
                                box-shadow: 0 8px 32px rgba(255, 82, 82, 0.2);'>
                        <h3 style='margin: 0; color: #ff5252;'>❌ No pude procesar tu gasto</h3>
                        <p style='margin: 0.5rem 0 0 0; color: #d0d0d0;'>{}</p>
                    </div>
                """.format(result['message']), unsafe_allow_html=True)
                
                st.markdown("")
                st.info("💡 **Consejo:** Intenta incluir el monto y descripción. Ejemplo: 'Gasté 20 soles en almuerzo'")
    
    # Ejemplos con diseño mejorado
    st.markdown("---")
    st.markdown("")
    st.markdown("### 💡 Prueba estos ejemplos")
    st.markdown("Haz clic en cualquiera para probarlo")
    st.markdown("")
    
    examples = [
        ("🍜", "Me gasté 15 soles en un adobo"),
        ("⛽", "Pagué 50 soles en gasolina"),
        ("📚", "Compré libros por 80 soles"),
        ("🍕", "Cena con amigos, 120 soles"),
        ("⚕️", "Consulta médica de 150 soles"),
        ("📺", "Netflix 35 soles")
    ]
    
    cols = st.columns(3)
    for idx, (emoji, text) in enumerate(examples):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class='example-card'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{emoji}</div>
                    <div style='font-size: 0.85rem; color: #4a5568;'>{text}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Probar", key=f"example_{idx}", use_container_width=True):
                st.session_state.example_text = text
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Dashboard
with tab2:
    if df.empty:
        # Mensaje de bienvenida personalizado
        st.markdown(f"""
            <div style='text-align: center; padding: 5rem 2rem;'>
                <div style='font-size: 6rem; margin-bottom: 1.5rem;'>📊</div>
                <h2 style='color: #e8e8e8; margin-bottom: 1rem; font-size: 2.5rem;'>¡Hola {current_user['full_name']}!</h2>
                <p style='font-size: 1.2rem; color: #888; margin-bottom: 2.5rem; line-height: 1.6;'>
                    Aún no hay registros. Comienza a registrar tus gastos e ingresos<br>para ver tus estadísticas y balance financiero.
                </p>
                <div style='display: inline-block; background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
                            padding: 1.2rem 2.5rem; border-radius: 30px; color: white; font-weight: 600;
                            box-shadow: 0 10px 40px rgba(0, 212, 255, 0.4); font-size: 1.1rem;'>
                    👈 Ve a "Nueva Transacción" para empezar
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Aplicar filtros
        filtered_df = df.copy()
        
        if 'date_range' in locals() and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['fecha'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['fecha'] <= pd.Timestamp(date_range[1]))
            ]
        
        if 'selected_category' in locals() and selected_category != 'Todas':
            filtered_df = filtered_df[filtered_df['categoria'] == selected_category]
        
        # Métricas principales con diseño mejorado - Gastos vs Ingresos
        st.markdown("### 📊 Resumen Financiero")
        st.markdown("")
        
        # Separar gastos e ingresos
        gastos_df = filtered_df[filtered_df['tipo'] == 'gasto']
        ingresos_df = filtered_df[filtered_df['tipo'] == 'ingreso']
        
        total_gastos = gastos_df['monto'].sum() if not gastos_df.empty else 0
        total_ingresos = ingresos_df['monto'].sum() if not ingresos_df.empty else 0
        balance = total_ingresos - total_gastos
        balance_color = '#00ff88' if balance >= 0 else '#ff5252'
        balance_icon = '📈' if balance >= 0 else '📉'
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: rgba(255, 82, 82, 0.1);
                            padding: 1.5rem; border-radius: 16px; text-align: center;
                            border: 1px solid rgba(255, 82, 82, 0.3);
                            box-shadow: 0 8px 32px rgba(255, 82, 82, 0.2);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>💸</div>
                    <div style='font-size: 0.85rem; color: #888; font-weight: 600; letter-spacing: 1px;'>TOTAL GASTOS</div>
                    <div style='font-size: 2rem; font-weight: 700; color: #ff5252; margin-top: 0.5rem;'>S/ {total_gastos:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: rgba(0, 255, 136, 0.1);
                            padding: 1.5rem; border-radius: 16px; text-align: center;
                            border: 1px solid rgba(0, 255, 136, 0.3);
                            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>💰</div>
                    <div style='font-size: 0.85rem; color: #888; font-weight: 600; letter-spacing: 1px;'>TOTAL INGRESOS</div>
                    <div style='font-size: 2rem; font-weight: 700; color: #00ff88; margin-top: 0.5rem;'>S/ {total_ingresos:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1);
                            padding: 1.5rem; border-radius: 16px; text-align: center;
                            border: 1px solid rgba(0, 212, 255, 0.3);
                            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{balance_icon}</div>
                    <div style='font-size: 0.85rem; color: #888; font-weight: 600; letter-spacing: 1px;'>BALANCE</div>
                    <div style='font-size: 2rem; font-weight: 700; color: {balance_color}; margin-top: 0.5rem;'>S/ {balance:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            num_transacciones = len(filtered_df)
            st.markdown(f"""
                <div style='background: rgba(122, 90, 248, 0.1);
                            padding: 1.5rem; border-radius: 16px; text-align: center;
                            border: 1px solid rgba(122, 90, 248, 0.3);
                            box-shadow: 0 8px 32px rgba(122, 90, 248, 0.2);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📝</div>
                    <div style='font-size: 0.85rem; color: #888; font-weight: 600; letter-spacing: 1px;'>TRANSACCIONES</div>
                    <div style='font-size: 2rem; font-weight: 700; color: #7a5af8; margin-top: 0.5rem;'>{num_transacciones}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("")
        
        # Gráficos separados por tipo (gastos e ingresos)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💸 Gastos por Categoría")
            # Filtrar solo gastos
            gastos_category = gastos_df.groupby('categoria')['monto'].sum().reset_index()
            gastos_category = gastos_category.sort_values('monto', ascending=False)
            
            # Colores neón para cada barra (gastos)
            colors = ['#ff5252', '#ff6b6b', '#ff8787', '#ffa0a0', '#ffb8b8', '#ffd0d0', '#ffe8e8', '#fff0f0']
            
            if not gastos_category.empty:
                fig_category = go.Figure(data=[
                    go.Bar(
                        x=gastos_category['categoria'],
                        y=gastos_category['monto'],
                        marker=dict(
                            color=colors[:len(gastos_category)],
                            line=dict(width=0)
                        ),
                        text=gastos_category['monto'].apply(lambda x: f'S/ {x:.0f}'),
                        textposition='outside',
                        textfont=dict(color='#e0e0e0', size=12)
                    )
                ])
                
                fig_category.update_layout(
                    showlegend=False,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", color='#e0e0e0'),
                    xaxis=dict(
                        showgrid=False,
                        title='',
                        tickfont=dict(color='#b0b0b0')
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.05)',
                        title='Monto (S/)',
                        tickfont=dict(color='#b0b0b0'),
                        title_font=dict(color='#888')
                    ),
                    margin=dict(t=30, b=20)
                )
                st.plotly_chart(fig_category, use_container_width=True)
            else:
                st.info("No hay gastos para mostrar en el período seleccionado")
        
        with col2:
            st.markdown("### 💰 Ingresos por Categoría")
            # Filtrar solo ingresos
            ingresos_category = ingresos_df.groupby('categoria')['monto'].sum().reset_index()
            ingresos_category = ingresos_category.sort_values('monto', ascending=False)
            
            colors_pie = ['#00ff88', '#00e676', '#00d4aa', '#00c28a', '#00b070', '#009e56', '#008c3c', '#007a22']
            
            if not ingresos_category.empty:
                fig_pie = go.Figure(data=[
                    go.Pie(
                        labels=ingresos_category['categoria'],
                        values=ingresos_category['monto'],
                        hole=0.5,
                        marker=dict(
                            colors=colors_pie[:len(ingresos_category)],
                            line=dict(color='#0a0a0a', width=3)
                        ),
                        textfont=dict(color='#ffffff', size=13, family='Inter'),
                        textposition='inside',
                        textinfo='percent+label'
                    )
                ])
                
                fig_pie.update_layout(
                    height=400,
                    font=dict(family="Inter, sans-serif", color='#e0e0e0'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    legend=dict(
                        font=dict(color='#b0b0b0'),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    margin=dict(t=30, b=20)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No hay ingresos para mostrar en el período seleccionado")
        
        st.markdown("")
        
        # Evolución temporal con gastos e ingresos separados
        st.markdown("### 📈 Evolución de Gastos e Ingresos en el Tiempo")
        
        # Preparar datos temporales
        gastos_temporal = gastos_df.groupby('fecha')['monto'].sum().reset_index()
        gastos_temporal = gastos_temporal.sort_values('fecha')
        gastos_temporal.columns = ['fecha', 'gastos']
        
        ingresos_temporal = ingresos_df.groupby('fecha')['monto'].sum().reset_index()
        ingresos_temporal = ingresos_temporal.sort_values('fecha')
        ingresos_temporal.columns = ['fecha', 'ingresos']
        
        # Combinar ambos datasets
        temporal_data = pd.merge(gastos_temporal, ingresos_temporal, on='fecha', how='outer').fillna(0)
        temporal_data = temporal_data.sort_values('fecha')
        
        fig_time = go.Figure()
        
        # Área de gastos
        fig_time.add_trace(go.Scatter(
            x=temporal_data['fecha'],
            y=temporal_data['gastos'],
            fill='tozeroy',
            fillcolor='rgba(255, 82, 82, 0.2)',
            line=dict(color='#ff5252', width=3),
            mode='lines+markers',
            marker=dict(
                size=8,
                color='#ff5252',
                line=dict(color='#0a0a0a', width=2)
            ),
            name='Gastos'
        ))
        
        # Área de ingresos
        fig_time.add_trace(go.Scatter(
            x=temporal_data['fecha'],
            y=temporal_data['ingresos'],
            fill='tozeroy',
            fillcolor='rgba(0, 255, 136, 0.2)',
            line=dict(color='#00ff88', width=3),
            mode='lines+markers',
            marker=dict(
                size=8,
                color='#00ff88',
                line=dict(color='#0a0a0a', width=2)
            ),
            name='Ingresos'
        ))
        
        fig_time.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color='#e0e0e0'),
            xaxis=dict(
                showgrid=False,
                title='Fecha',
                tickfont=dict(color='#b0b0b0'),
                title_font=dict(color='#888')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                title='Monto (S/)',
                tickfont=dict(color='#b0b0b0'),
                title_font=dict(color='#888')
            ),
            showlegend=False,
            margin=dict(t=30, b=20),
            hovermode='x unified'
        )
        st.plotly_chart(fig_time, use_container_width=True)
        
        st.markdown("")
        
        # Top 5 gastos con mejor diseño
        st.markdown("### 🔝 Top 5 Mayores Gastos")
        st.markdown("")
        
        top_gastos = filtered_df.nlargest(5, 'monto')[['fecha', 'descripcion', 'categoria', 'monto']]
        
        for idx, row in top_gastos.iterrows():
            emoji_map = {
                'alimentacion': '🍽️',
                'transporte': '🚗',
                'entretenimiento': '🎮',
                'salud': '⚕️',
                'educacion': '📚',
                'servicios': '💡',
                'compras': '🛍️',
                'otros': '📦'
            }
            emoji = emoji_map.get(row['categoria'], '📦')
            
            st.markdown(f"""
                <div style='background: rgba(30, 30, 35, 0.5); padding: 1.3rem; border-radius: 14px; 
                            margin-bottom: 1rem; border: 1px solid rgba(0, 212, 255, 0.15);
                            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                            transition: all 0.3s ease;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='flex: 1; display: flex; align-items: center; gap: 1rem;'>
                            <span style='font-size: 2rem;'>{emoji}</span>
                            <div>
                                <div style='font-size: 1.1rem; font-weight: 600; color: #e8e8e8;'>{row['descripcion']}</div>
                                <div style='font-size: 0.85rem; color: #888; margin-top: 0.2rem;'>
                                    <span class='badge badge-purple'>{row['categoria'].title()}</span>
                                </div>
                            </div>
                        </div>
                        <div style='text-align: right; padding-left: 1rem;'>
                            <div style='font-size: 0.85rem; color: #888;'>{row['fecha'].strftime("%d/%m/%Y")}</div>
                            <div style='font-size: 1.8rem; font-weight: 800; color: #00d4ff; margin-top: 0.3rem;'>S/ {row['monto']:.2f}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Tab 3: Historial
with tab3:
    st.markdown("### 📋 Historial Completo de Transacciones")
    st.markdown("")
    
    if df.empty:
        st.markdown("""
            <div style='text-align: center; padding: 4rem 2rem;'>
                <div style='font-size: 5rem; margin-bottom: 1.5rem;'>📋</div>
                <h3 style='color: #b0b0b0; font-size: 1.8rem;'>No hay transacciones registradas aún</h3>
                <p style='color: #666; font-size: 1.1rem;'>Comienza a registrar tus gastos e ingresos para ver tu historial aquí</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Aplicar filtros
        filtered_df = df.copy()
        
        if 'date_range' in locals() and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['fecha'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['fecha'] <= pd.Timestamp(date_range[1]))
            ]
        
        if 'selected_category' in locals() and selected_category != 'Todas':
            filtered_df = filtered_df[filtered_df['categoria'] == selected_category]
        
        # Ordenar por fecha (más reciente primero)
        filtered_df = filtered_df.sort_values('fecha', ascending=False)
        
        # Mostrar tabla con mejor formato y tipo de transacción
        display_df = filtered_df[['fecha', 'tipo', 'descripcion', 'categoria', 'monto']].copy()
        display_df['fecha'] = display_df['fecha'].dt.strftime('%d/%m/%Y')
        
        # Agregar emoji según tipo
        display_df['tipo'] = display_df['tipo'].apply(lambda x: '💰 Ingreso' if x == 'ingreso' else '💸 Gasto')
        
        # Formatear monto con color
        display_df['monto'] = display_df['monto'].apply(lambda x: f'S/ {x:.2f}')
        display_df.columns = ['📅 Fecha', '🏷️ Tipo', '📝 Descripción', '📂 Categoría', '💵 Monto']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Opción de eliminar transacciones con mejor diseño
        st.markdown("---")
        st.markdown("### 🗑️ Gestionar Transacciones")
        st.markdown("")
        
        expense_ids = filtered_df.index.tolist()
        if expense_ids:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                selected_expense = st.selectbox(
                    "Selecciona una transacción para eliminar:",
                    options=expense_ids,
                    format_func=lambda x: f"📅 {filtered_df.loc[x, 'fecha'].strftime('%d/%m/%Y')} | {'💰' if filtered_df.loc[x, 'tipo'] == 'ingreso' else '💸'} {filtered_df.loc[x, 'descripcion']} | 💵 S/ {filtered_df.loc[x, 'monto']:.2f}",
                    label_visibility="visible"
                )
            
            with col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Eliminar", type="secondary", use_container_width=True):
                    data_manager.delete_expense(selected_expense)
                    st.success("✅ Eliminado")
                    st.rerun()

# Footer dark mode
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2.5rem 1rem; 
                background: rgba(20, 20, 25, 0.6);
                border-radius: 20px; margin-top: 2rem; 
                border: 1px solid rgba(0, 212, 255, 0.2);
                box-shadow: 0 10px 40px rgba(0, 212, 255, 0.15);'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>💰</div>
        <h2 style='background: linear-gradient(135deg, #00d4ff 0%, #7a5af8 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   margin: 0.5rem 0; font-weight: 800; font-size: 2rem;'>Misti AI Wallet</h2>
        <p style='color: #b0b0b0; margin: 0.8rem 0; font-size: 1.1rem; font-weight: 500;'>
            🤖 Tu asistente inteligente de finanzas personales
        </p>
        <div style='margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.1);'>
            <p style='color: #888; font-size: 0.9rem;'>
                Desarrollado con ❤️ usando <span style='color: #00d4ff; font-weight: 600;'>Streamlit</span>, 
                <span style='color: #7a5af8; font-weight: 600;'>Python</span> y 
                <span style='color: #00ff88; font-weight: 600;'>AI</span>
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
