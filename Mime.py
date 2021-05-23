from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['To'] = "hardik@gmail.com"
msg['From'] = "hardik2@example.com"
msg['Subject'] = "Query in compre"
part = MIMEText('text', 'plain')
message = "Kab chalu hoga exam?"
part.set_payload(message)
msg.attach(part)
print(msg.as_string())
