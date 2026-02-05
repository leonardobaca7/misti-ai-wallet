# 🚀 RAILWAY DEPLOYMENT - Guía Rápida

## 📋 PASO 1: Crear Tablas en Supabase (5 minutos)

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard/projects
2. Abre tu proyecto: **wytaduckicscvulotqhb**
3. Click en **SQL Editor** (icono ⚡ en el menú izquierdo)
4. Click en **"New Query"**
5. **Copia y pega este SQL completo:**

```sql
-- ==================== TABLA DE USUARIOS ====================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP DEFAULT NOW()
);

-- ==================== TABLA DE TRANSACCIONES ====================
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

-- ==================== TABLA DE PRESUPUESTOS ====================
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

-- ==================== ÍNDICES PARA PERFORMANCE ====================
CREATE INDEX IF NOT EXISTS idx_transactions_username ON transactions(username);
CREATE INDEX IF NOT EXISTS idx_transactions_fecha ON transactions(fecha DESC);
CREATE INDEX IF NOT EXISTS idx_budgets_username ON budgets(username);
```

6. Click en **"Run"** (o Ctrl+Enter)
7. Deberías ver: ✅ **"Success. No rows returned"**

---

## 🚂 PASO 2: Crear Cuenta en Railway (2 minutos)

1. Ve a https://railway.app/
2. Click en **"Login"**
3. **Inicia sesión con tu cuenta de GitHub** (leonardobaca7)
4. Click en **"New Project"**
5. Selecciona **"Deploy from GitHub repo"**
6. Busca y selecciona: **MistiWallet**
7. Railway detectará automáticamente que es Python

---

## ⚙️ PASO 3: Configurar Variables de Entorno en Railway (3 minutos)

Después de crear el proyecto en Railway:

1. En tu proyecto, ve a la pestaña **"Variables"**
2. Click en **"+ New Variable"**
3. Agrega estas 2 variables:

**Variable 1:**
```
Name: SUPABASE_URL
Value: https://wytaduckicscvulotqhb.supabase.co
```

**Variable 2:**
```
Name: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5dGFkdWNraWNzY3Z1bG90cWhiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyNDY5NDAsImV4cCI6MjA4NTgyMjk0MH0.wgcfKJIYg_e3AzLB1bJ94PkAhyL9ugBGk08_cLDPdP4
```

4. Railway reiniciará automáticamente tu app

---

## 🎯 PASO 4: Verificar que Funciona

1. Railway te dará una URL como: `https://mistiwallet-production.up.railway.app`
2. Abre la URL
3. **Crea un usuario nuevo** (ejemplo: `Leonardo`, password: `1234`)
4. Agrega un gasto de prueba
5. **Recarga la página**
6. ✅ **Los datos deberían persistir** (no se pierden)

---

## 🔥 Beneficios de Railway vs Streamlit Cloud

| Feature | Streamlit Cloud | Railway |
|---------|----------------|---------|
| **Siempre activo** | ❌ Se duerme | ✅ 24/7 |
| **Datos persisten** | ❌ Se pierden | ✅ Supabase |
| **Velocidad** | Lento | ⚡ Rápido |
| **Dominio custom** | ❌ | ✅ |
| **Student Pack** | ❌ | ✅ $5/mes gratis |
| **SSL/HTTPS** | ✅ | ✅ |

---

## 🆘 Solución de Problemas

### Error: "Module 'supabase' not found"
→ Asegúrate que `supabase>=2.0.0` esté en requirements.txt (ya lo agregamos)

### Error: "Missing SUPABASE_URL"
→ Verifica que agregaste las variables de entorno en Railway

### La app no carga
→ Ve a "Deployments" en Railway y revisa los logs de error

---

## 💰 GitHub Student Pack (IMPORTANTE)

Railway te da **$5 USD/mes gratis** con Student Pack:

1. Ve a https://railway.app/account/billing
2. Click en **"Redeem GitHub Student Pack"**
3. Conecta tu cuenta de GitHub
4. ✅ Obtienes $5/mes recurrentes (suficiente para MistiWallet)

---

¿Listo? Sigue los pasos y avísame si tienes errores. 🚀
