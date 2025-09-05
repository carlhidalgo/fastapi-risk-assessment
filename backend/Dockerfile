# Usar la imagen oficial de Python 3.12 slim (más liviana)
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el archivo de requirements primero (para aprovechar el cache de Docker)
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias sin cache para reducir el tamaño de la imagen
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar todo el código de la aplicación
COPY . /app

# Exponer el puerto 80 (donde correrá FastAPI)
EXPOSE 80

# Comando para ejecutar la aplicación usando uvicorn
# Usa la forma exec para permitir que FastAPI maneje señales correctamente
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
