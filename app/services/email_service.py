from flask_mail import Message
from app import mail
from flask import current_app, render_template
from threading import Thread


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")


def send_email(subject, recipients, text_body, html_body=None):
    """Send email"""
    msg = Message(subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # Send asynchronously
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_contact_confirmation(contacto):
    """Send confirmation email to user who submitted contact form"""
    send_email(
        subject=f'Confirmación de contacto - {contacto.oferta.titulo}',
        recipients=[contacto.email],
        text_body=f'''Hola {contacto.nombre},

Hemos recibido tu consulta sobre: {contacto.oferta.titulo}

El propietario se pondrá en contacto contigo pronto.

Gracias por usar EquaHome.
''',
        html_body=f'''
        <p>Hola <strong>{contacto.nombre}</strong>,</p>
        <p>Hemos recibido tu consulta sobre: <strong>{contacto.oferta.titulo}</strong></p>
        <p>El propietario se pondrá en contacto contigo pronto.</p>
        <p>Gracias por usar EquaHome.</p>
        '''
    )


def send_admin_notification(contacto):
    """Send notification to admin about new contact"""
    send_email(
        subject=f'Nuevo contacto recibido - {contacto.oferta.titulo}',
        recipients=[current_app.config['ADMIN_EMAIL']],
        text_body=f'''Nuevo contacto recibido:

Propiedad: {contacto.oferta.titulo}
De: {contacto.nombre} ({contacto.email})
Teléfono: {contacto.telefono}
Mensaje: {contacto.mensaje}

Fecha: {contacto.fecha_contacto}
''',
        html_body=f'''
        <h2>Nuevo contacto recibido</h2>
        <p><strong>Propiedad:</strong> {contacto.oferta.titulo}</p>
        <p><strong>De:</strong> {contacto.nombre} ({contacto.email})</p>
        <p><strong>Teléfono:</strong> {contacto.telefono}</p>
        <p><strong>Mensaje:</strong> {contacto.mensaje}</p>
        <p><strong>Fecha:</strong> {contacto.fecha_contacto}</p>
        '''
    )


def send_queja_response(queja):
    """Send response to user complaint"""
    send_email(
        subject=f'Respuesta a tu queja - {queja.titulo}',
        recipients=[queja.usuario.email],
        text_body=f'''Hola {queja.usuario.nombre},

Hemos revisado tu queja: {queja.titulo}

Respuesta del administrador:
{queja.respuesta_admin}

Gracias por ayudarnos a mejorar.

EquaHome
''',
        html_body=f'''
        <p>Hola <strong>{queja.usuario.nombre}</strong>,</p>
        <p>Hemos revisado tu queja: <strong>{queja.titulo}</strong></p>
        <h3>Respuesta del administrador:</h3>
        <p>{queja.respuesta_admin}</p>
        <p>Gracias por ayudarnos a mejorar.</p>
        <p><em>EquaHome</em></p>
        '''
    )
