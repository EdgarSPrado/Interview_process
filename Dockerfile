# Imagen base
FROM python:3.11-slim

# Carpeta de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip install --upgrade pip

# Instalar dependencias Python
RUN pip install -r requirements.txt

# Copiar proyecto Django
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar Django con gunicorn
CMD ["gunicorn", "new_proyect.wsgi:application", "--bind", "0.0.0.0:8080"]
