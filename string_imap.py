import getpass
import imaplib, email
pop3_server = 'imap.gmail.com'
pop3_port = '993'

def fetchMail(username, password):
    mailbox = imaplib.IMAP4_SSL(pop3_server, pop3_port)
    mailbox.login(username, password)
    mailbox.select('Inbox')
    result, data = mailbox.search(None, 'ALL')
    # print(data[0])
    for num in reversed(data[0].split()):
        result, data = mailbox.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        if 'Network Programming' in msg.as_string():
            print('Date: ', msg['Date'])
            print('From: ', msg['From'])
            print('To: ', msg['To'])
            print('Subject: ', msg['Subject'])
            print( email.message_from_bytes(data[0][1]))
            print(' ')
    # print(len(mailbox.list()[1]))
    mailbox.close()
    mailbox.logout()

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
fetchMail(username, password)