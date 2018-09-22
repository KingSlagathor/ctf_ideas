import random
import socket
import threading
from math import sqrt as sq


class ThreadedServer(object):

    Intro_Message = "The Fibonacci sequence is a series of numbers where a number is found by adding up the two numbers" \
                    " before it.\n Starting with 0 and 1, the sequence goes 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 etc.\n" \
                    "The 4th prime number is 7 and the number at position 7 of the Fibonacci sequence is 13.\n" \
                    "If the server sends the number 4 the answer to respond with would be 13.\n" \
                    "Send \"1\" to receive 3 static test cases to test your code and \"2\" to receive random tests.\n" \
                    "Earn the flag by passing the random tests.\n".encode('ascii')
    Test_Passed = "Test Passed\nTry for the flag next time!\n".encode('ascii')
    Test_Failed =  "Test Failed\n".encode('ascii')
    Flag_Attempt_Failed = "Attempt at flag failed\n".encode('ascii')
    Flag_Attempt_Passed = "Success!\nFlag:PrimePythonPractice\n".encode('ascii')

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def fp(self, n): # returns value from func p's position in fib seq
        return f(p(n))

    def srpf(self, client, address, n):
        x = str(n)
        client.send(x.encode('ascii') + "\n")
        r = client.recv(2048)
        rr = r.decode('ascii')
        if int(rr) == self.fp(n):
            return True
        else:
            return False

    def test_fp(self, client, address):
        x = [3, 5, 7]
        if all(self.srpf(client, address, i) for i in x):
            client.send(self.Test_Passed)
        else:
            client.send(self.Test_Failed)

    def attempt_fp(self, client, address):
        x = [random.randint(1,100) for _ in range(20)]
        if all(self.srpf(client, address, i) for i in x):
            client.send(self.Flag_Attempt_Passed)
        else:
            client.send(self.Flag_Attempt_Failed)

    def listen_to_client(self, client, address):

        size = 2048
        while True:
            try:
                client.send(self.Intro_Message)
                data = client.recv(size).rstrip()
                if data == "1".encode('ascii'):
                    self.test_fp(client, address)
                    break
                elif data == "2".encode('ascii'):
                    self.attempt_fp(client, address)
                    break
                else:
                    raise Exception('Client Disconnected')
            except:
                client.close()
                return False


def f(n):  # returns nth number in fibonacci sequence
    return pow(2 << n, n+1, (4 << 2*n) - (2 << n)-1) % (2 << n) #returns Fibonacci number in given position so for example F(7) would return 13


def p(n):  # returns nths prime number
    primes = [2]
    attempt = 3
    while len(primes) < n:
        if all(attempt % prime != 0 for prime in primes):
            primes.append(attempt)
        attempt += 2
    return primes[-1]


if __name__ == '__main__':

    port_num = 2020
    ThreadedServer('',port_num).listen()
