# SMTPTesting

Herramienta web para probar conexiones SMTP de forma interactiva y registrar resultados.

---

## 🚀 ¿Qué hace esta app?

Permite:

- Ingresar los datos de conexión SMTP (host, puerto, usuario, seguridad).
- Validar si la autenticación se realiza correctamente.
- Ver el resultado en pantalla.
- Guardar el historial de pruebas en un archivo `smtp_log.txt` (sin contraseña).

---

## 🧱 Estructura del proyecto

```
/smtptesting
├── app.py               # Código principal de la app Flask
├── requirements.txt     # Dependencias (Flask)
├── Dockerfile           # Imagen base del contenedor
├── docker-compose.yml   # Configuración del entorno Docker
└── smtp_log.txt         # Log de intentos SMTP (creado en ejecución)
```

---

## ▶️ Cómo iniciar el entorno de trabajo

### Paso 1: Abre Docker Desktop  
Asegúrate de que esté corriendo.

### Paso 2: Abre una terminal y navega al proyecto

```bash
cd /Users/henrysilvacastillo/Webs/smtptesting
```

### Paso 3: Levanta el contenedor

```bash
docker-compose up
```

Esto ejecuta Flask en modo desarrollo, con recarga automática y acceso vía:

👉 http://localhost:8080

---

## 🛑 Cómo detener

Presiona `Ctrl + C` y luego:

```bash
docker-compose down
```

---

## 🔄 Para reconstruir (si cambias el Dockerfile o dependencias)

```bash
docker-compose up --build
```

---

## 📁 Archivos de log

El archivo `smtp_log.txt` guarda los intentos de conexión (sin contraseñas). Se sobrescribe con cada ejecución.

---

## 🔒 Seguridad

- El formulario no guarda contraseñas.
- Se recomienda configurar autenticación básica si se va a exponer públicamente.

---
