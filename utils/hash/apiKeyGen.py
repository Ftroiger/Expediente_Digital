import uuid

# Función para generar una apiKey única
def generarApiKey():
    return str(uuid.uuid4())