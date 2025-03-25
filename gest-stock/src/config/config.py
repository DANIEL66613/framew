import os


# Chaves do Twilio
TWILIO_SID = os.getenv("TWILIO_SID", "seu_twilio_sid_aqui")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "seu_auth_token_aqui")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "seu_numero_twilio_aqui")

# Chave secreta
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")