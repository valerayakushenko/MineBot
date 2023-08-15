import socket

def check_server_online(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((ip, int(port)))
        return True
    except socket.error:
        return False
    finally:
        sock.close()
        

