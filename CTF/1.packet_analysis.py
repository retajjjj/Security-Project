from pathlib import Path
from scapy.all import rdpcap, TCP, Raw
from base64 import b64decode

#load all pkts
PCAP_PATH = Path(__file__).resolve().parent.parent / "CTF_DATA" / "CTF1" / "traffic.pcapng"
packets = rdpcap(str(PCAP_PATH))

#collect the tcp payloads (in bytes) whose dest port = 4444
payloads = []
for pkt in packets:
    if TCP in pkt and Raw in pkt and pkt[TCP].dport == 4444:
        payloads.append(pkt[Raw].load)

#concat the bytes 
combined = b"".join(payloads).decode() 
print(f"Message reassembled: {combined}")

#strip msg of MSG and EOF
stripped = combined.removeprefix("MSG:").removesuffix(":EOF")

#decode
flag = b64decode(stripped).decode()

print(f"Flag: {flag}")

