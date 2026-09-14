# Cisco Router SSH Web Project

A small Docker Compose project with:
- Frontend: HTML/CSS/JavaScript
- Backend: Flask + Paramiko
- SSH to a Cisco IOS router
- Two inputs: router IP and IOS command
- Execute button and command output

## Default credentials

The backend uses:
- username: `admin`
- password: `cisco`

You can override them with environment variables.

## Start

From this project directory:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
docker compose logs -f backend
```

Open in Ubuntu browser:

```text
http://localhost:5000
```

Default test:
- IP: `192.168.31.132`
- Command: `show ip interface brief`

## Stop

```bash
docker compose down
```

## Important

The Docker container must be able to reach the router's IP on TCP port 22. The Ubuntu VM/network must also be able to reach `192.168.31.132`.

For commands that require an interactive IOS mode (for example entering configuration mode or `enable` with a separate enable password), this starter project should be extended to use Paramiko `invoke_shell()` and prompt handling.
