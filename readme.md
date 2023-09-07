# Website Monitoring Project

The project offers an end-to-end monitoring solution for web applications hosted on Linode and containerized using Docker. If any issue or anomaly is detected, the system will automatically restart the Docker container or the entire server, depending on the severity. If the application is not accessible at all, a notification email is sent to the designated email address.

## Features:
1. **Website Monitoring**: Periodically checks the status of a specified website.
2. **Automatic Recovery**: Restarts Docker containers or the entire server upon detected issues.
3. **Notification System**: Sends an email alert when the application is inaccessible.
4. **Scheduled Monitoring**: Uses the `schedule` library to continuously monitor the website at regular intervals.

## Implementation Steps:

### 1. **Environment Variables Configuration**:
Set up necessary environment variables for the application:
- `EMAIL_ADDRESS`: Your email address used to send notifications.
- `EMAIL_PASSWORD`: Email account password.
- `LINODE_TOKEN`: Your Linode API token.
- `LINODE_PWD`: Password for Linode.

### 2. **Monitoring & Recovery**:
The `monitor_website()` function performs the following tasks:
- Sends a request to the web application.
- If the application returns HTTP 200 (OK), it logs that the application is running successfully.
- If the application is down but the server is running, the Docker container is restarted.
- If the application isn't accessible at all, a notification email is sent, and both the server and Docker container are restarted.

### 3. **Notification System**:
The `send_notification(message)` function:
- Connects to the SMTP server (`smtp.outlook.com` in this case) using the provided email credentials.
- Sends an email alert with the specified message.

### 4. **Automatic Recovery**:
Two recovery functions are provided:
- `restart_container()`: Connects to the server via SSH using `paramiko` and restarts the Docker container.
- `restart_server_and_container()`: Uses the `linode_api4` library to restart the Linode server. Once the server is up, it restarts the Docker container.

### 5. **Scheduled Monitoring**:
The monitoring function is scheduled to run every 5 minutes using the `schedule` library. The program runs indefinitely, periodically checking the status of the website.

## Libraries & Tools Used:
- **Requests**: For sending HTTP requests. [Documentation](https://pypi.org/project/requests/).
- **Paramiko**: For SSH connections. [Documentation](https://pypi.org/project/paramiko/).
- **smtplib**: Built-in Python module for sending emails.
- **linode_api4**: To interact with Linode servers. [Documentation](https://pypi.org/project/linode-api4/).
- **schedule**: To run scheduled tasks. [Documentation](https://schedule.readthedocs.io/).

## Setup & Usage:

1. Install necessary libraries:
  ```bash
      pip install requests paramiko linode_api4 schedule
  ```
3. Set up environment variables as mentioned above.
4. Run the Python script to start monitoring.

