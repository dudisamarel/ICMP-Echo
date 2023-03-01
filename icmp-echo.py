from socket import *
from struct import *
from random import randint
from time import sleep
import argparse

ICMP_ECHO_REQUEST = 8
ICMP_HEADER_FORMAT = "!BBHHH"


def calculate_checksum(source_string):
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0
    loByte = 0
    hiByte = 0

    while count < countTo:
        loByte = source_string[count]
        hiByte = source_string[count + 1]
        sum = sum + ((hiByte) * 256 + (loByte))
        count += 2

    if countTo < len(source_string):
        loByte = source_string[len(source_string) - 1]
        sum += (loByte)

    sum &= 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff

    return htons(answer)


class IcmpService:
    def __init__(self, dest):
        self.seq = 0
        self.code = 0
        self.checksum = 0
        self.seq = 0
        self.s = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.dest_addr = gethostbyname(dest)

    def create_packet(self, payload):
        id = randint(0, 0xFFFF)
        data = bytes(payload, encoding="ascii")
        checksum = 0
        header = pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST,
                      self.code, checksum, id, self.seq)
        checksum = calculate_checksum(header + data)
        return pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST,  self.code, checksum, id, self.seq) + data

    def send_packet(self, payload):
        self.s.sendto(self.create_packet(payload), (self.dest_addr, 0))
        self.seq += 1


def main(args):
    dest = args.destination
    payload = args.payload
    icmp_service = IcmpService(dest)
    n = 10
    for i in range(0, len(payload), n):
        icmp_service.send_packet(payload[i:i+n])
        sleep(5)
    while True:
        icmp_service.send_packet(" ")
        sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("payload")
    args = parser.parse_args()
    main(args)
