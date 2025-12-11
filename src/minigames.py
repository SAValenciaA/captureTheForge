import socketserver
import subprocess
import os
import threading

PATH = "src/minigames"
BASE_PORT = 4000

def spawn_server(port, script):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self_inner):
            proc = subprocess.Popen(
                ["python3", script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            def send_output():
                for line in proc.stdout:
                    try: self_inner.request.sendall(line.encode())
                    except: break

            threading.Thread(target=send_output, daemon=True).start()

            while True:
                data = self_inner.request.recv(1024)
                if not data:
                    break
                proc.stdin.write(data.decode())
                proc.stdin.flush()

    print(f"[+] Launching {script} on port {port}")
    socketserver.TCPServer(("0.0.0.0", port), Handler).serve_forever()

scripts = [f for f in os.listdir(PATH) if f.endswith(".py")]

for i, script in enumerate(scripts):
    port = BASE_PORT + i
    t = threading.Thread(target=spawn_server, args=(port, f"{PATH}/{script}"), daemon=True)
    t.start()

input("Press ENTER to stop servers...\n")

