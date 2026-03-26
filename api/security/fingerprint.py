import socket

class FingerPrint:

    """
    Simple Security Measure to detect and monitor requests and connections.
    Supports HTTP, FTP, and SSH detection via payload-driven scanning.
    """

    COMMON_IDENTIFIERS = {
        "HTTP": "HTTP/1.1",
        "FTP": "220",
        "SSH": "SSH"
    }



    def look_for(self, text: str) -> str:
        """Identify service from response text."""
        if not text:
            return "NO RESPONSE"
        for name, signature in self.COMMON_IDENTIFIERS.items():
            if signature in text:
                return name
        return "UNKNOWN"



    def send_payload(self, ip: str, port: int, payload: str, reply_size: int = 4096) -> str:
        """Send payload to a target IP:port and return service identification."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                if sock.connect_ex((ip, port)) == 0:
                    print(f"│ sending to > \033[1;34m{ip}:{port}\033[0m => [\033[1;33m{repr(payload)}\033[0m]")
                    sock.sendall(payload.encode())
                    data = sock.recv(reply_size).decode(errors="ignore")
                    return self.look_for(data)
                else:
                    print(f"* (engine[failed]) > target [{ip}:{port}] unreachable, payload: [{repr(payload)}]")
                    return "UNREACHABLE"
        except Exception as e:
            print(f"* (engine[error]) > {e}")
            return "ERROR"



    def by_portnum(self , port_num , proto:str="tcp"):
        try:
                return socket.getservbyport(port_num , proto)

        except OSError:
                return "UNKNOWN"



    def payload_driven(self, ip: str, port: int):
        """Send multiple protocol payloads and summarize results."""
        
        PAYLOADS = [
            "USER anonymous\r\n",
            f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n",
            "hello world!"
        ]
        
        summary = {}

        print("┌" + "─" * 25 + " REQUESTS " + "─" * 25 + "┐")
        
        for payload in PAYLOADS:
            service = self.send_payload(ip, port, payload)
            summary[payload] = service
        
        print("└" + "─" * (50 + len(" REQUESTS ")) + "┘\n")

        print("┌" + "─" * 25 + " SUMMARY " + "─" * 25 + "┐")
        
        for payload, service in summary.items():
            print(f"│ SERVICE : {service:<10} :: payload : [{repr(payload)}]")
        
        print("└" + "─" * (50 + len(" SUMMARY ")) + "┘")