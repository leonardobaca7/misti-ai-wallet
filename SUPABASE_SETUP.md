# 🔥 Configuración de Supabase para MistiWallet

## 📋 Paso 1: Crear Cuenta en Supabase (GRATIS)

1. Ve a https://supabase.com
2. Click en **"Start your project"**
3. Inicia sesión con tu GitHub (ya tienes cuenta)
4. Click en **"New Project"**

**Datos del proyecto:**
- Name: `mistiwallet`
- Database Password: **Guarda esto en un lugar seguro** (ejemplo: `TuPassword123!`)
- Region: `South America (São Paulo)` - Más cercano a Perú
- Pricing Plan: **Free** (500MB gratis, suficiente)

⏱️ Espera 2-3 minutos mientras Supabase crea tu base de datos.

---

## 📊 Paso 2: Crear las Tablas en la Base de Datos

1. En el panel de Supabase, ve a **SQL Editor** (icono de ⚡)
2. Click en **"New Query"**
3. Copia y pega este SQL completo:

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

-- ==================== SEGURIDAD (Row Level Security) ====================
-- Esto asegura que cada usuario solo vea sus propios datos
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad (los usuarios solo ven sus propios datos)
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (true);

CREATE POLICY "Users can view own transactions" ON transactions
    FOR ALL USING (username = current_setting('app.current_user', true));

CREATE POLICY "Users can view own budgets" ON budgets
    FOR ALL USING (username = current_setting('app.current_user', true));
```

4. Click en **"Run"** (o presiona Ctrl+Enter)
5. Deberías ver: ✅ **"Success. No rows returned"**

---

## 🔑 Paso 3: Obtener las Credenciales de API

1. En Supabase, ve a **Settings** ⚙️ (abajo a la izquierda)
2. Click en **API**
3. Busca estas 2 credenciales:

### **URL del Proyecto:**
```
https://tuproyecto.supabase.co
```
Copia el que dice **"URL"** (ejemplo: `https://xyzabc123.supabase.co`)

### **API Key (anon/public):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Copia el que dice **"anon" key** (es muy largo, ~200 caracteres)

---

## 🔐 Paso 4: Configurar Secrets en Streamlit Cloud

1. Ve a tu app en Streamlit Cloud: https://share.streamlit.io/
2. Click en tu app **MistiWallet**
3. Click en **"Settings"** (⚙️ abajo a la derecha)
4. Click en **"Secrets"**
5. Pega este código (reemplaza con TUS credenciales):

```toml
[supabase]
url = "https://tuproyecto.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu-key-muy-larga-aqui"
```

**⚠️ IMPORTANTE:** Reemplaza:
- `tuproyecto.supabase.co` → Tu URL real de Supabase
- `eyJ...` → Tu API key real (la "anon" key)

6. Click en **"Save"**
7. Click en **"Reboot app"**

---

## 💻 Paso 5: Configurar para Desarrollo Local (Opcional)

Si quieres probar en tu computadora antes de subir:

1. Crea un archivo `.streamlit/secrets.toml` en la carpeta de MistiWallet:

```bash
mkdir .streamlit
```

2. Crea el archivo `secrets.toml` con el mismo contenido:

```toml
[supabase]
url = "https://tuproyecto.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu-key-aqui"
```

3. Prueba la app localmente:

```bash
streamlit run app.py
```

---

## ✅ Verificar que Funciona

1. Ve a tu app en Streamlit Cloud
2. **Registra un nuevo usuario** (ejemplo: `Leonardo`, password: `1234`)
3. Agrega un gasto de prueba
4. **Recarga la página** o apágala y vuélvela a abrir
5. Inicia sesión con el mismo usuario
6. ✅ **¡Los datos deberían seguir ahí!**

---

## 🎯 Beneficios de Usar Supabase

| ❌ Antes (JSON local) | ✅ Ahora (Supabase) |
|----------------------|---------------------|
| Datos se pierden al reiniciar | **Datos permanentes** |
| Solo funciona para 1 usuario | **Multi-usuario real** |
| Sin respaldo | **Respaldo automático** |
| Lento con muchos datos | **Rápido (PostgreSQL)** |
| No hay seguridad | **Autenticación segura** |

---

## 📊 Monitorear tu Base de Datos

En Supabase puedes ver:

- **Table Editor**: Ver todos los usuarios y transacciones en tiempo real
- **Logs**: Ver errores si algo falla
- **Database**: Uso de espacio (tienes 500MB gratis)

---

## 🆘 Solución de Problemas

### Error: "Missing Supabase credentials"
→ Verifica que configuraste los secrets correctamente en Streamlit Cloud

### Error: "relation 'users' does not exist"
→ No ejecutaste el SQL del Paso 2. Ve al SQL Editor y ejecútalo

### Error: "Invalid API key"
→ Copiaste mal la API key. Debe ser la "anon" key, no la "service_role"

---

## 🎓 Con GitHub Student Pack

Si tienes GitHub Student Pack, Supabase te da:
- ✅ $100 USD en créditos
- ✅ Suficiente para 2-3 años de uso
- ✅ Sin límite de storage

**Activa aquí:** https://education.github.com/pack

---

¿Listo para probarlo? Sigue los pasos y avísame si tienes algún error. 🚀
