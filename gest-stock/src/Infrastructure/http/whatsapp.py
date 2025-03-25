from twilio.rest import Client
from src.config.config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

class WhatsAppService:
    @staticmethod
    def enviar_mensagem(phone_number, activation_code):
        """Envia o código de ativação para o número do WhatsApp usando Twilio"""
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Seu código de ativação é: {activation_code}",
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{phone_number}"
        )

        return message.sid