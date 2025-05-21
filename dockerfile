# ------------- Fase de construcción -------------
FROM python:3.11-slim as builder

WORKDIR /build

# Instala dependencias de compilación
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ------------- Fase de producción -------------
FROM python:3.11-slim

# Crea usuario y su directorio home
RUN useradd -m appuser  # -m crea el directorio /home/appuser
WORKDIR /home/appuser/app  # WORKDIR en el home del usuario

# Copia dependencias desde la fase builder
COPY --chown=appuser:appuser --from=builder /root/.local /home/appuser/.local

# Copia el código de la app
COPY --chown=appuser:appuser . .

# Configura variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/appuser/app \
    PATH="/home/appuser/.local/bin:${PATH}"

# Usuario no-root
USER appuser

# Puerto y comando
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]