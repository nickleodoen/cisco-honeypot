import asyncio
import asyncssh
import datetime
import logging
from alerts import send_alert

logging.basicConfig(level=logging.DEBUG)

# The SSH session (this handles the CLI interaction)
class CiscoSession(asyncssh.SSHServerSession):
    def __init__(self):
        self._input = ''
        self._chan = None

    def connection_made(self, chan):
        self._chan = chan
        chan.write("Cisco IOS Software, C800 Software (C800-UNIVERSALK9-M), Version 15.2\r\n")
        chan.write("Router> ")

    def data_received(self, data, datatype):
        self._input += data
        if '\n' in self._input:
            command = self._input.strip()
            self.log_command(command)
            self._chan.write(self.handle_command(command) + "\nRouter> ")
            self._input = ''

    def handle_command(self, cmd):
        responses = {
            "enable": "Password: ",
            "show version": "Cisco IOS Software, C800, uptime is 5 weeks...",
            "show running-config": "Building configuration...\nCurrent configuration : 2048 bytes",
        }

        if cmd == "exit":
            self._chan.write("Bye.\n")
            self._chan.exit(0)
            return ""
        
        return responses.get(cmd, f"% Invalid input detected at '^' marker.")

    def log_command(self, cmd):
        with open("honeypot.log", "a") as f:
            f.write(f"{datetime.datetime.now()}: {cmd}\n")
        send_alert(f"📟 Command run: `{cmd}`")


    def shell_requested(self):
        return True

class CiscoSSHServer(asyncssh.SSHServer):
    def __init__(self):
        self.peer_ip = "Unknown"
    
    def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
        self.peer_ip = orig_host
        return self

    def begin_auth(self, username):
        # Always require authentication
        return True

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        ip = self.peer_ip
        msg = f"🚨 SSH login: `{username}` / `{password}` from `{ip}`"
        logging.info(f"Login attempt: {username} / {password}")
        send_alert(msg)
        return True

    def session_requested(self):
        return CiscoSession()

# Start the SSH server
async def start_server():
    await asyncssh.create_server(
        CiscoSSHServer,  # <-- This was missing!
        '', 2222,
        server_host_keys=['ssh_host_key']
    )

if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(start_server())
        print("SSH honeypot running on port 2222...")
        asyncio.get_event_loop().run_forever()
    except (OSError, asyncssh.Error) as exc:
        print("SSH honeypot failed to start:", str(exc))
