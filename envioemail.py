import smtplib
from email.message import EmailMessage


def enviar(email_destino,codigo):
    email_origen="grupo4uninorte@outlook.com"
    password="GevoraHotel"
    email= EmailMessage()
    email["From"] = email_origen
    email["To"] = email_destino
    email["Subject"] = "codigo de activacion"
    email.set_content("Sr, usuario su código de activación es :\n\n"+codigo+ "\n\n Recuerde copiarlo y pegarlo para activar su cuenta. \n\nMuchas Gracias")
    
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(email_origen, password)
    smtp.sendmail(email_origen, email_destino, email.as_string())
    smtp.quit()
        
    

