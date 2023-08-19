import os
import paramiko
import requests
import smtplib
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
LINODE_PWD = os.environ.get('LINODE_PWD')


def send_notification(message):
    print('Sending an email alert....')
    with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='172.105.102.225', username='root', password=LINODE_PWD,
                key_filename='/home/vboxuser/.ssh/id_rsa.pub')
    stdin, stdout, stderr = ssh.exec_command('docker start 6cb5aab2b894')
    print(stdin)
    print(stdout.readlines())
    print("application restarted")


def restart_server_and_container():
    # restarts linode server
    print("Rebooting the server ...")
    my_client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = my_client.load(linode_api4.Instance, 47557273)
    nginx_server.reboot()
    while True:
        nginx_server = my_client.load(linode_api4.Instance, 47557273)
        if nginx_server.status == 'running':
            time.sleep(5)
            # restart the application
            restart_container()
            break


def monitor_website():
    try:
        response = requests.get('http://172.105.102.225:8080/')
        if response.status_code == 200:
            print("Application is running successfully")
        else:
            print("applications is down")
            msg = "Subject: SITE DOWN!!\n Fix the issue!"
            # send_notification(msg)
            restart_container()

    except Exception as ex:
        print(f'Connection error {ex}')
        msg = "App isn't accessible at all"
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_website)

while True:
    schedule.run_pending()