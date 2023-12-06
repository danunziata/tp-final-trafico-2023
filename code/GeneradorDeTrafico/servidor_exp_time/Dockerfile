# Utiliza la imagen base Alpine
FROM alpine:latest

# Instala las dependencias del sistema
RUN apk add python3
RUN apk add py3-pip

# Configura el directorio de trabajo
WORKDIR /home/servidor

# Copia los archivos de la aplicación
COPY . /home/servidor

# Instalar uvircon y fastapi
RUN pip install uvicorn
RUN pip install "fastapi[all]"

# Expone el puerto en el que la aplicación se ejecuta (por defecto, FastAPI usa el puerto 8000)
EXPOSE 8000

# Comando para ejecutar Uvicorn con la aplicación FastAPI
CMD ["sh","-c","uvicorn servidor:app --host 0.0.0.0 --port 8000 & exec sh"]