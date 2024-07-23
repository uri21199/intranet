import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def enviar_correo(categoria, subcategoria, tipo_problema, descripcion_problema, id_equipo, empleado):
    # Configuración del servidor SMTP
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_user = "lbustos_@outlook.com"
    smtp_password = "34Bostero!"

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = formataddr((str(Header('Soporte Sistemas', 'utf-8')), smtp_user))
    mensaje['To'] = "sistemas@worldmedicalcare.com"
    mensaje['Subject'] = Header("Nuevo reporte a sistemas", 'utf-8')

    cuerpo = f"""
    Categoria: {categoria}
    Subcategoria: {subcategoria}
    Tipo de problema: {tipo_problema}
    Descripcion del problema: {descripcion_problema}
    ID del equipo: {id_equipo}
    Reportado por: {empleado}
    """
    mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
    print(cuerpo)

    # Enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, "sistemas@worldmedicalcare.com", mensaje.as_string())
        server.quit()
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
