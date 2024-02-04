# Robot for ordering





## Setup as a Background Service

### 🚀 Setup and test Workforce Agent Core
Replace <link token> below with a link token created from the Control Room Workers -page. Note that Workforce Agent is always linked to a specific workspace in Control Room to avoid accidental runs between development and production Workers.



```
mkdir ~/.robocorp
curl https://downloads.robocorp.com/workforce-agent-core/releases/latest/linux64/robocorp-workforce-agent-core -o ~/.robocorp/robocorp-workforce-agent-core
chmod +x ~/.robocorp/robocorp-workforce-agent-core
~/.robocorp/robocorp-workforce-agent-core -v
~/.robocorp/robocorp-workforce-agent-core link <link token>
~/.robocorp/robocorp-workforce-agent-core start --service
```


## Setup service

1. Create the service config file


```
touch /etc/systemd/system/RobocorpAgentCore.service
sudo chmod 664 /etc/systemd/system/RobocorpAgentCore.service
```


2.  Add the following content to the config file

Edit the file /etc/systemd/system/RobocorpAgentCore.service with your favorite text editor.

```
[Unit]
Description=Robocorp Agent

[Service]
User=<user>
ExecStart=/home/centos/.robocorp/robocorp-workforce-agent-core start --service
Restart=always
PrivateDevices=true
ProtectControlGroups=true
ProtectKernelTunables=true
ProtectSystem=full
RestrictSUIDSGID=true
PrivateTmp=yes

[Install]
WantedBy=default.target
```
- Replace <user> with actual user
- The ExecStart needs to have the absolute path

3. Setup and start the service:
```
sudo systemctl daemon-reload
sudo systemctl start RobocorpAgentCore.service
sudo systemctl status RobocorpAgentCore.service
```
### Having the service start at boot

If you want the service to be running after startup you have to run:

```
sudo systemctl enable RobocorpAgentCore.service
```


### Maintain the service
The typical maintenance task is to update the Agent Core executable.

For that, you need to:

- Stop the service
- Download the latest Agent Core
- Restart the service


```
sudo systemctl stop RobocorpAgentCore.service
curl https://downloads.robocorp.com/workforce-agent-core/releases/latest/linux64/robocorp-workforce-agent-core -o ~/.robocorp/robocorp-workforce-agent-core
sudo systemctl start RobocorpAgentCore.service
sudo systemctl status RobocorpAgentCore.service
```

