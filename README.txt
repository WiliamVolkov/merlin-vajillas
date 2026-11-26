MERLIN VAJILLAS - APLICACIÓN WEB

REQUISITOS
- Python 3.11+
- PostgreSQL para producción (SQLite funciona en local)

EJECUCIÓN LOCAL
1. Crear entorno virtual:
   python -m venv .venv
2. Activarlo:
   Windows: .venv\Scripts\activate
   macOS/Linux: source .venv/bin/activate
3. Instalar:
   pip install -r requirements.txt
4. Copiar .env.example a .env y configurar variables.
5. Ejecutar:
   python run.py

ADMINISTRACIÓN
La primera ejecución crea el usuario administrador usando ADMIN_EMAIL y ADMIN_PASSWORD.
Si no configurás esas variables, los valores iniciales son:
admin@merlinvajillas.com
Cambiar123!

CAMBIAR LA CONTRASEÑA INICIAL INMEDIATAMENTE.
No dejar credenciales predeterminadas en producción.

RENDER
- Crear un Web Service conectado al repositorio.
- Build command: pip install -r requirements.txt
- Start command: gunicorn run:app
- Agregar una PostgreSQL de Render y copiar su Internal Database URL a DATABASE_URL.
- Configurar SECRET_KEY, ADMIN_EMAIL y ADMIN_PASSWORD como variables de entorno.
- Health check path: /health

IMPORTANTE
Esta es una primera versión funcional. La aprobación de solicitudes no bloquea stock por fechas todavía:
antes de confirmar un alquiler, el administrador debe revisar manualmente disponibilidad y cantidades.
Las imágenes se cargan mediante URL externa en esta versión.
La integración de WhatsApp está prevista en variables de entorno, pero requiere configurar y desarrollar el envío con la API oficial de Meta.
Antes de operar comercialmente, probar todos los flujos y reforzar controles de inventario, almacenamiento de imágenes, copias de seguridad y políticas de privacidad.
