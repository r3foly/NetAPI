import socket


class Net:

    @staticmethod
    def tcp_socket(func):
        def wrapper(*args , **kwargs):
            with socket.socket( socket.AF_INET , socket.SOCK_STREAM) as sock:
                return func(sock , *args , **kwargs)

        return wrapper



    @staticmethod
    def udp_socket(func):
        def wrapper(*args , **kwargs):
            with socket.socket( socket.AF_INET , socket.SOCK_DGRAM) as sock:
                return func(sock , *args , **kwargs)

        return wrapper



"""

    A Simple Wireless Point To Point ( PTP ) echo server

"""

class Tcp_echoServer:
    

    def handle_client(self , conn ,reply_size:int=4096):
        # a message to notify the client
        conn.sendall(b"CRTL-C to disconnect\n")


        try:
            while True:
                chunk = conn.recv(reply_size).decode(errors='ignore') # libs shouldnt crash user-made programs , could result into truncated output

                if not chunk:
                        conn.sendall(b"message didnt arrive...\n")
                        break

                else:
                    print(f"* (log) > received : {chunk}")
                    conn.sendall(f"{chunk}".encode())

        except Exception as exp:
            print(f"* (server[startup]) >\033[1;31m failed due to {exp}\033[0m")
            raise



    def start(self , ip:str="0.0.0.0" , port:int=2800):
        with socket.socket( socket.AF_INET , socket.SOCK_STREAM) as sock:

            sock.bind(( ip ,  port))
            sock.listen()
            print(f"* (server[tcp]) > listening on {ip}:{port}")


            conn , addr = sock.accept()
            print(f"* (connection attempt) > {addr[0]} is now connected")
            self.handle_client(conn)

