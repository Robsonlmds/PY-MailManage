import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser
import logging

class Config:
    EMAIL_HOST_IMAP = 'imap.gmail.com'  # Servidor IMAP
    EMAIL_HOST_SMTP = 'smtp.gmail.com'  # Servidor SMTP
    EMAIL_USER = 'robsonlucas@gmail.com'  # POR EMAIL PESSOAL !!!!!!!!!!!!!
    EMAIL_PASS = '*****************'  # POR SENHA PESSOAL !!!!!!!!!!!!!
    DESTINATARIO = 'destinatario@gmail.com' # DESTINATARIO FIXO!!!!!!!!  


# LOGGING
logging.basicConfig(level=logging.INFO)


#FUNÇÃO ENVIAR E-MAIL
def enviar_email(destinatario, assunto, corpo):
    """email TEST."""
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP(Config.EMAIL_HOST_SMTP, 587) as server:
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
            server.sendmail(Config.EMAIL_USER, destinatario, msg.as_string())
        logging.info('Email enviado!!')
    except Exception as e:
        logging.error(f'Erro ao enviar email {e}')


#FUNÇÃO RESPONDER E-MAIL
def responder_email(remetente, assunto_original):
    """Respondendo e-mial"""
    corpo = f'Obrigado pelo seu email sobre "{assunto_original}".'
    enviar_email(remetente, f'Re: {assunto_original}', corpo)


#FUNCÃO DE LOCALIZAR E-MAIL
def ver_emails():
    """Verifica e lista os emails não lidos na caixa de entrada."""
    try:
        mail = imaplib.IMAP4_SSL(Config.EMAIL_HOST_IMAP)
        mail.login(Config.EMAIL_USER, Config.EMAIL_PASS)
        mail.select('inbox')

        result, data = mail.search(None, 'UNSEEN')
        ids = data[0].split()

        if not ids:
            logging.info('Não há novos emails.')
            return

        for email_id in ids:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
            subject = msg['subject']
            sender = msg['from']
            logging.info(f'Novo email de: {sender}\nAssunto: {subject}')
            
            # RESPONDER EMAIL
            responder_email(sender, subject)

        mail.close()
        mail.logout()
    except Exception as e:
        logging.error(f'Erro ao verificar emails: {e}')

if __name__ == '__main__':
    logging.info('Iniciando o serviço de email...')
    ver_emails()  #  -> VERIFICAR E-MIAL AO INICIAR
