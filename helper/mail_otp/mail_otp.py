import imaplib
import email
import logging
from email.header import decode_header
import re
from dotenv import load_dotenv
import os

load_dotenv()

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_IMAP_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_IMAP_PASSWORD")

logger = logging.getLogger(__name__)

def get_latest_otp_email(subject_to_search:str):
    print(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")
    mail._encoding = "utf-8"

    status, data = mail.search("UTF-8", f'(SUBJECT "{subject_to_search}")')

    if status != "OK":
        logger.warning("search failed")
        mail.logout()
        exit()

    email_ids = data[0].split()

    if not email_ids:
        logger.warning("cannot find any email with the specified subject")
        mail.logout()
        exit()

    latest_email_id = email_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    if status != "OK":
        logger.warning("fetch email failed")
        mail.logout()
        exit()

    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    logger.debug("Subject: %s", subject)

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="ignore")
                break  
    else:
        charset = msg.get_content_charset() or "utf-8"
        body = msg.get_payload(decode=True).decode(charset, errors="ignore")

    logger.debug("Body:\n%s", body)

    mail.logout()

    # TODO: 根據實際 OTP 格式調整正則表達式，目前只是假設 OTP 是 6 位數字
    otp_pass = re.findall(r'<div style=".*">(\d{6})</div>',body)
    return otp_pass[0] if otp_pass else None