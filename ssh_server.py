import asyncio
import websockets
import paramiko
import json

async def ssh_handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=data['host'],
                port=int(data['port']),
                username=data['username'],
                password=data['password']
            )

            stdin, stdout, stderr = ssh.exec_command(data['command'])
            output = stdout.read().decode() + stderr.read().decode()
            await websocket.send(output)
            ssh.close()
        except Exception as e:
            await websocket.send(f"Error: {str(e)}")

async def main():
    async with websockets.serve(ssh_handler, "0.0.0.0", 8765):
        print("SSH WebSocket Server is running on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
