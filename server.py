import socket
import pickle
import datetime
import hashlib

class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"

class Blockchain:

    diff = 10
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                print(int(block.hash(), 16))
                print(self.target)
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1


host= '127.0.0.1'
port= 5001

s=socket.socket()
s.bind((host, port))

s.listen(2)
c, addr= s.accept()
print("connection from:" + str(addr))
while True:
    data=c.recv(4096).decode()
    if not data:
        break
    print("From client:" + str(data))
   # d="sup"
    blockchain = Blockchain()
    for n in range(10):
        blockchain.mine(Block("heyTanya")) # + str(n+1)
        if n==0:
            yellow = blockchain.head
        while blockchain.head != None:
            print(blockchain.head)
            blockchain.head = blockchain.head.next
    blockchain.head = yellow
    datastr= pickle.dumps(blockchain)
    print("Sending to client... ")
    c.send(datastr)
c.close()














