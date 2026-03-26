from api.net import Net
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import argparse
from sys import stdout
from api.security.fingerprint import FingerPrint

# global
found_ports = []
lock = Lock()
fingerprint = FingerPrint()

@Net.tcp_socket
def scan(sock , ip:str , port:int , timeout:float) -> None:
    sock.settimeout(timeout)

    if sock.connect_ex(( ip , port )) == 0:
        with lock:
            found_ports.append(port)


def arguments():
    parser = argparse.ArgumentParser(

        description="a simple Portscanner"
    )

    parser.add_argument("-H" , "--host" , default="127.0.0.1" , type=str , help="specify thet target IP")
    parser.add_argument("-r" , "--range" , default=1024 , type=int , help="set a specific range")
    parser.add_argument("-t" , "--timeout" , default=1.0 , type=float , help="set a specific timeout")
    parser.add_argument('-th' , "--threads" , default=25 , type=float , help="set a specific thread count")

    return parser.parse_args()



def main() -> None:
    args = arguments()


    with ThreadPoolExecutor(max_workers=args.threads) as thread:
        for port in range(1 , args.range + 1):
            thread.submit(scan , args.host , port , args.timeout)

            with lock:
                stdout.write(f"\r> port scanned : {port} ( {(port / args.range) * 100:.2f}%)")
                stdout.flush()

    print()


    for port in found_ports:
        fingerprint.payload_driven(args.host , port)

    print("> By Port Number ( BASED ON PORT NUMBER )")
    
    for port in found_ports:
        print(f"{port} :: {fingerprint.by_portnum(port)}")



main() 