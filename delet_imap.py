import getpass
import imaplib, email
pop3_server = 'imap.gmail.com'
pop3_port = '993'

def fetchMail(username, password):
    mailbox = imaplib.IMAP4_SSL(pop3_server, pop3_port)
    mailbox.login(username, password)
    mailbox.select('Inbox')
    result, data = mailbox.search(None, '(FROM "parnamihardik@gmail.com")')
    print(data[0])
    data = data[0].split()
    for id in data:
        mailbox.store(id, '+X-GM-LABELS', '\\Trash')
    mailbox.expunge()
    mailbox.close()
    mailbox.logout()

def getUnseen(username, password):
    mailbox = imaplib.IMAP4_SSL(pop3_server, pop3_port)
    mailbox.login(username, password)
    mailbox.select('Inbox')
    result, data = mailbox.search(None, '(UNSEEN)')
    if result == "OK":
        for uid in data[0].split():
            result, data = mailbox.fetch(uid, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            print(msg)
            print(30*'*')
            result, data = mailbox.store(uid, '-FLAGS', '\\SEEN')

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
# fetchMail(username, password)
getUnseen(username, password)