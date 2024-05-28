import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send(email, nombre, fecha, hora, corte):
    
    #credenciales
    user = st.secrets["smtp_user"]
    password = st.secrets["smtp_pass"]
    
    sender_email = "JCA Barber Shop"
    #Config del server
    msg = MIMEMultipart()
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Param del mensaje
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Reserva cita"
    
    # Cuerpo del mensaje
    message = f"""
    Hola {nombre},
    Su reserva ha sido realizada con éxito.
    Fecha {fecha}
    Hora {hora}
    Tipo de corte {corte}
    
    Gracias por confiar en nosotros.
    ¡Un saludo!   
    """
    
    msg.attach(MIMEText(message, 'plain'))
    
    # Conexion al servidor
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
     
    except smtplib.SMTPException as e:
        st.exception("Error al enviar el email")
        