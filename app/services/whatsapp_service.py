import urllib.parse
from flask import current_app

class WhatsAppService:
    @staticmethod
    def generar_enlace_oferta(oferta, telefono_base=None):
        """
        Genera un enlace de WhatsApp con un mensaje predefinido para una oferta de propiedad.
        """
        # Formatear el teléfono
        telefono = telefono_base or oferta.propietario.telefono
        if not telefono:
            return None
            
        # Limpiar el teléfono (quitar espacios, +, etc)
        telefono = str(telefono).replace(' ', '').replace('+', '').replace('-', '')
        
        # Construir el mensaje
        mensaje = f"¡Hola! Estoy interesado en la propiedad: '{oferta.titulo}' "
        if oferta.tipo_operacion == 'alquiler':
            mensaje += f"(Alquiler - {oferta.precio} FCFA/mes)."
        elif oferta.tipo_operacion == 'booking':
            mensaje += f"(Reserva/Booking)."
        else:
            mensaje += f"(Venta - {oferta.precio} FCFA)."
            
        mensaje += f" Ubicada en {oferta.ciudad}, {oferta.barrio}."
        mensaje += f" ¿Podría darme más información?"
        
        # Codificar el mensaje
        mensaje_codificado = urllib.parse.quote(mensaje)
        
        # Retornar el enlace a wa.me
        return f"https://wa.me/{telefono}?text={mensaje_codificado}"
        
    @staticmethod
    def generar_enlace_soporte():
        """
        Genera un enlace de WhatsApp para soporte general de la plataforma.
        """
        telefono_soporte = current_app.config.get('WHATSAPP_SOPORTE', '')
        if not telefono_soporte:
            return None
            
        telefono_soporte = str(telefono_soporte).replace(' ', '').replace('+', '').replace('-', '')
        mensaje = "Hola equipo de soporte de EquaHome, necesito ayuda con mi cuenta."
        mensaje_codificado = urllib.parse.quote(mensaje)
        
        return f"https://wa.me/{telefono_soporte}?text={mensaje_codificado}"
