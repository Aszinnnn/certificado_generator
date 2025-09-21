import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_certificate_email(config, to_email, name, certificate_path):
    try:
        print("🔄 Tentando método alternativo de autenticação...")
        
        # Configurações
        email = config['email']
        password = config['password']
        
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = config['subject']
        
        # Corpo do email
        message_body = config['message'].format(nome=name)
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Anexar certificado
        with open(certificate_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="html")
            attach.add_header('Content-Disposition', 'attachment', 
                             filename=f"Certificado_{name}.html")
            msg.attach(attach)
        
        # Tentar diferentes métodos de conexão
        try:
            # Método 1: TLS (587)
            print("🔧 Tentando porta 587 com TLS...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            server.quit()
            print("✅ Email enviado com sucesso via TLS!")
            
        except Exception as e:
            print(f"❌ Erro com TLS: {e}")
            
            # Método 2: SSL (465)
            print("🔧 Tentando porta 465 com SSL...")
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(email, password)
            server.send_message(msg)
            server.quit()
            print("✅ Email enviado com sucesso via SSL!")
        
        # Mover certificado para enviados
        sent_dir = "output/sent"
        os.makedirs(sent_dir, exist_ok=True)
        os.rename(certificate_path, os.path.join(sent_dir, os.path.basename(certificate_path)))
        
        return True
        
    except Exception as e:
        raise Exception(f"Falha ao enviar e-mail: {str(e)}")