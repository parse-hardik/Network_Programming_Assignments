import getpass
import poplib
pop3_server = 'pop.googlemail.com'
pop3_port = '995'

def fetchMail(username, password):
    mailbox = poplib.POP3_SSL(pop3_server, pop3_port)
    mailbox.user(username)
    mailbox.pass_(password)
    print(len(mailbox.list()[1]))

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
fetchMail(username, password)