import os
import imaplib
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email import policy
from email.parser import BytesParser
from dotenv import load_dotenv

# CARREGAR DOTNEV
load_dotenv()

class Config:
    EMAIL_HOST_IMAP = os.getenv('EMAIL_HOST_IMAP', 'imap.gmail.com')
    EMAIL_HOST_SMTP = os.getenv('EMAIL_HOST_SMTP', 'smtp.gmail.com')
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    DESTINATARIO = os.getenv('DESTINATARIO', 'emailDestinatario@gmail.com')

# CONFIGURAR LOGGING
logging.basicConfig(filename='logs/email_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ENVIAR EMAIL
def enviar_email(destinatario, assunto, corpo, anexo=None):
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    if anexo:
        with open(anexo, 'rb') as f:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(f.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename={os.path.basename(anexo)}')
            msg.attach(parte)

    try:
        with smtplib.SMTP(Config.EMAIL_HOST_SMTP, 587) as server:
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
            server.sendmail(Config.EMAIL_USER, destinatario, msg.as_string())
        logging.info('Email enviado com sucesso!')
    except Exception as e:
        logging.error(f'Erro ao enviar email: {e}')

# VEREFICAR EMAIL
def ver_emails(filtro='UNSEEN'):
    try:
        mail = imaplib.IMAP4_SSL(Config.EMAIL_HOST_IMAP)
        mail.login(Config.EMAIL_USER, Config.EMAIL_PASS)
        mail.select('inbox')

        result, data = mail.search(None, filtro)
        ids = data[0].split()

        if not ids:
            logging.info('Não há novos emails.')
            return

        for email_id in ids:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
            
            # Verificações para evitar erros
            subject = msg['subject'] if msg['subject'] else 'Sem assunto'
            sender = msg['from'] if msg['from'] else 'Desconhecido'

            logging.info(f'Novo email de: {sender}\nAssunto: {subject}')

        mail.close()
        mail.logout()
    except Exception as e:
        logging.error(f'Erro ao verificar emails: {e}')


if __name__ == '__main__':
    logging.info('Iniciando o serviço de email...')
    ver_emails()  # VERRIFICAR O EMAL, QUANDO INICIAR
    # TESTE DE EMAIL
    enviar_email(Config.DESTINATARIO, 'Teste', 'Este é um e-mail de teste com anexo.', 'C:/Users/profslpa/AppData/Local/Programs/')
