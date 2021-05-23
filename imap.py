import getpass
import imaplib, email
pop3_server = 'imap.gmail.com'
pop3_port = '993'

def fetchMail(username, password):
    mailbox = imaplib.IMAP4_SSL(pop3_server, pop3_port)
    mailbox.login(username, password)
    mailbox.select('Inbox')
    result, data = mailbox.uid('search', 'FROM', 'psaxena')
    print(data[0])
    for num in data[0].split():
        result, data = mailbox.uid('fetch', num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        print('Date: ', msg['Date'])
        print('From: ', msg['From'])
        print('To: ', msg['To'])
        print('Subject: ', msg['Subject'])
        print(' ')
    # print(len(mailbox.list()[1]))
    mailbox.close()
    mailbox.logout()

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
fetchMail(username, password)