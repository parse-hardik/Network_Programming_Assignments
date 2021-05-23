import getpass
import poplib
pop3_server = 'pop.googlemail.com'
pop3_port = '995'

def fetchMail(username, password):
    mailbox = poplib.POP3_SSL(pop3_server, pop3_port)
    mailbox.user(username)
    mailbox.pass_(password)
    # print(len(mailbox.list()[1]))
    number_of_messages = len(mailbox.list()[1])
    # Loop in the all emails.
    count=0
    for i in range(number_of_messages):
        # Get one email.
        count+=1
        for msg in mailbox.retr(i+1)[1]:
            # body = msg.decode()['Body']
            if msg.decode().find('Timetable'):
                print(msg)
        if count==10:
            break

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
fetchMail(username, password)