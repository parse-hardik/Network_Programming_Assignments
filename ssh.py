import getpass, paramiko
hostname = 'localhost'
port = 22
ssh_client = paramiko.SSHClient()
print('here')
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.load_system_host_keys()
username = input("Enter username: ")
password = getpass.getpass(prompt="Enter password: ")
cmd = 'ls | wc -l'
ssh_client.connect(hostname, port, username, password)
stdin, stdout, stderr = ssh_client.exec_command(cmd)
print(stdout.read())