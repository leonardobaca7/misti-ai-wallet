# 💰 Misti AI Wallet

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

**Tu asistente inteligente de finanzas personales con IA** 🤖✨

Gestiona tus gastos e ingresos usando lenguaje natural. Dark mode profesional, multi-usuario y notificaciones por email.

</div>

---

## 🎯 Características Principales

### 🗣️ Lenguaje Natural
Escribe como hablas y la IA entiende automáticamente:

```
"Gasté 50 soles en almuerzo ayer"        → ✅ Detecta: 50 | Ayer | Alimentación
"Pagué 120 en taxi hace 3 días"          → ✅ Detecta: 120 | Hace 3 días | Transporte  
"Cobré 3000 de mi sueldo el lunes"       → ✅ Detecta: 3000 | Lunes | Ingreso
"Compré ropa por 200 anteayer"           → ✅ Detecta: 200 | Anteayer | Compras
```

### 🤖 Inteligencia Artificial
- **Detección de montos**: Reconoce cantidades en texto natural
- **Fechas inteligentes**: `ayer`, `anteayer`, `hace X días`, `el lunes`, `DD/MM`
- **Categorización automática**: 8 categorías predefinidas (alimentación, transporte, etc.)
- **Clasificación de tipo**: Distingue automáticamente gastos de ingresos

### 👥 Sistema Multi-Usuario
- ✅ Registro con contraseñas encriptadas (SHA-256)
- ✅ Login seguro con validación
- ✅ Datos completamente separados por usuario
- ✅ Sesiones persistentes

### 📧 Notificaciones por Email
- 📊 Resúmenes mensuales automáticos vía Gmail
- 💰 Total de ingresos y gastos del mes
- 📈 Balance (ingresos - gastos) con indicador
- 🏆 Top 5 categorías de gastos
- 🎨 Diseño HTML dark mode profesional

### 📊 Dashboard Interactivo
- **Métricas**: Total gastos, total ingresos, balance, transacciones
- **Gráficos**: Barras por categoría, pie chart, evolución temporal
- **Filtros**: Por fecha, categoría y tipo de transacción
- **Exportar**: Descarga datos en CSV

### 🎨 Diseño Dark Mode
- Colores neón profesionales (#00d4ff, #7a5af8, #00ff88, #ff69b4)
- Glassmorphism effects
- Fuente Inter de Google Fonts
- Interfaz moderna y responsive

---

## 🚀 Instalación Rápida

### 1. Clonar Repositorio
```bash
git clone https://github.com/leonardobaca7/misti-ai-wallet.git
cd misti-ai-wallet
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar Aplicación
```bash
streamlit run app.py
```

La app se abrirá en `http://localhost:8501` 🎉

---

## 📦 Tecnologías

- **Streamlit**: Framework web interactivo
- **Pandas**: Manipulación de datos
- **Plotly**: Visualizaciones interactivas
- **SQLite**: Base de datos persistente (incluido con Python)
- **Python 3.13**: Lenguaje base
- **SHA-256**: Encriptación de contraseñas
- **Gmail SMTP**: Notificaciones por email

---

## 💻 Uso

### 1️⃣ Crear Cuenta
1. Abre la app
2. Ve a **"✨ Crear Cuenta"**
3. Completa: usuario, nombre, email, contraseña
4. ¡Listo! Auto-login

### 2️⃣ Registrar Transacciones

**Gastos:**
- "Gasté 50 en comida ayer"
- "Pagué 120 de taxi hace 2 días"
- "Compré ropa por 200 el lunes"

**Ingresos:**
- "Cobré 3000 de mi sueldo"
- "Gané 500 por freelance ayer"
- "Me pagaron 1000 de la venta"

### 3️⃣ Ver Dashboard
- **Tab "📊 Dashboard"**: Gráficos y métricas en tiempo real
- **Tab "📋 Historial"**: Tabla completa filtrable
- **Exportar**: Botón para descargar CSV

### 4️⃣ Configurar Emails (Opcional)

**Obtener contraseña de Gmail:**
1. Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Genera contraseña para "Misti Wallet"
3. Copia la contraseña de 16 caracteres

**En la app:**
1. Sidebar → **"📧 Notificaciones"**
2. Ingresa email y contraseña de aplicación
3. Click **"Enviar Resumen del Mes Anterior"**
4. ¡Revisa tu inbox! 📬

---

## 📁 Estructura del Proyecto

```
misti-ai-wallet/
├── app.py                      # App principal Streamlit
├── requirements.txt            # Dependencias
├── .gitignore                  # Archivos ignorados
├── README.md                   # Documentación
├── LICENSE                     # Licencia MIT
│
├── data/                       # Datos (no versionados)
│   ├── .gitkeep
│   └── misti_wallet.db        # Base de datos SQLite
│
└── utils/                      # Módulos del sistema
    ├── __init__.py
    ├── nlp_processor.py       # IA - Procesamiento lenguaje
    ├── database_manager.py    # Gestión base de datos SQLite
    └── email_manager.py       # Notificaciones Gmail
```

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con SHA-256 (nunca en texto plano)
- ✅ Datos separados por usuario en SQLite con claves foráneas
- ✅ Contraseñas de Gmail no se almacenan en archivos
- ✅ Base de datos en `.gitignore` (no se sube a GitHub)
- ✅ Sesiones seguras con Streamlit

**IMPORTANTE:**
- `data/misti_wallet.db` está en `.gitignore`
- Usa contraseñas de aplicación de Gmail, NO tu contraseña principal
- Los datos persisten en archivo SQLite local

---

## 📊 Categorías Automáticas

| Categoría | Palabras clave |
|-----------|---------------|
| 🍽️ Alimentación | comida, almuerzo, cena, restaurante, desayuno |
| 🚗 Transporte | taxi, uber, gasolina, pasaje, combustible |
| 🎮 Entretenimiento | cine, juego, concierto, netflix, diversión |
| ⚕️ Salud | medicina, doctor, farmacia, hospital, clínica |
| 📚 Educación | curso, libro, matrícula, universidad, colegio |
| 💡 Servicios | luz, agua, internet, alquiler, teléfono |
| 🛍️ Compras | ropa, zapatos, tienda, mall, compras |
| 📦 Otros | Todo lo demás |

---

## 📅 Fechas Reconocidas

- **Ayer**: `"ayer gasté 50"`
- **Anteayer**: `"anteayer pagué 120"`
- **Hace X días**: `"hace 3 días compré 200"`
- **Hace X semanas**: `"hace 2 semanas gasté 150"`
- **Día de semana**: `"el lunes gasté 80"`, `"el martes pagué 90"`
- **Semana pasada**: `"la semana pasada gasté 300"`
- **Formato DD/MM**: `"el 25/12 gasté 400"`

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -m 'Agregar funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 🐛 Problemas Comunes

### "❌ Contraseña incorrecta"
- Verifica mayúsculas/minúsculas
- Las contraseñas son case-sensitive

### "❌ Error al enviar email"
- Verifica contraseña de aplicación de Gmail
- Verifica conexión a internet
- Asegúrate de que el email esté registrado

### "No aparecen mis datos"
- Click en "🔄 Actualizar Datos"
- Verifica que estés logueado con el usuario correcto

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

Desarrollado con ❤️ usando Python, Streamlit y mucho café ☕

**Leonardo Baca**
- GitHub: [@leonardobaca7](https://github.com/leonardobaca7)
- Proyecto: [Misti AI Wallet](https://github.com/leonardobaca7/misti-ai-wallet)

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

Made with 💰 by [Leonardo Baca](https://github.com/leonardobaca7)

</div>
