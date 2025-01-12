FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY app.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto que usará la aplicación
EXPOSE 8501

# Variables de entorno para Streamlit
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
