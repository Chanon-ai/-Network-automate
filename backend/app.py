import os
import time
import paramiko
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="/app/frontend")

USERNAME = os.getenv("CISCO_USERNAME", "admin")
PASSWORD = os.getenv("CISCO_PASSWORD", "cisco")
SSH_PORT = int(os.getenv("SSH_PORT", "22"))


@app.get("/")
def index():
    return send_from_directory("/app/frontend", "index.html")


@app.post("/api/execute")
def execute_command():
    data = request.get_json(silent=True) or {}

    router_ip = str(data.get("ip", "")).strip()
    command = str(data.get("command", "")).strip()

    if not router_ip or not command:
        return jsonify({
            "success": False,
            "error": "IP address and command are required."
        }), 400

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=router_ip,
            port=SSH_PORT,
            username=USERNAME,
            password=PASSWORD,
            look_for_keys=False,
            allow_agent=False,
            timeout=8
        )

        channel = ssh.invoke_shell()
        time.sleep(1)

        # Clear initial output
        if channel.recv_ready():
            channel.recv(65535)

        # Send command
        channel.send(command + "\n")
        time.sleep(2)

        output = ""

        while channel.recv_ready():
            output += channel.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )
            time.sleep(0.2)

        return jsonify({
            "success": True,
            "output": output
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"{type(e).__name__}: {e}"
        }), 502

    finally:
        ssh.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
