import time
import socket
import threading
import traceback

from Logger import logger

from toolbox import unpack

IP = 'localhost'
IP = '192.168.31.38'
port = 63365
buffer_size = 1024
coding = 'utf-8'


class TCPClient(object):
    ''' TCP client object,
    it connects to the TCP server, sends and receives messages.
    '''

    def __init__(self, IP=IP, port=port, buffer_size=buffer_size):
        ''' Initialize and setup client '''
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # Connet to IP:port
        client.connect((IP, port))
        name = client.getsockname()

        # Setup client and name
        self.buffer_size = buffer_size
        self.serverIP = IP
        self.client = client
        self.name = name
        logger.info(f'TCP Client is initialized as {name} to {IP}')

        self.session = None

        # Keep listening
        self.keep_listen()

    def close(self):
        ''' Close the session '''
        # Close the client
        self.client.close()
        self.is_connected = False

        # Stop the data stack
        if self.session is not None:
            self.session.ds.stop()

        logger.info(f'Client closed: {self.serverIP}')

    def keep_listen(self):
        ''' Keep listening to the server.
        - Received the message;
        - Send reply;
        - It will be closed if it receives empty message or error occurs.
        '''
        logger.info(f'Start listening to {self.serverIP}')

        t0 = time.time()
        num = 0

        while True:
            try:
                # ----------------------------------------------------------------
                # Wait until new message is received
                income = b''
                while len(income) < 16000:
                    income += self.client.recv(min(self.buffer_size,
                                               16000 - len(income)))

                if income == b'':
                    logger.debug('Received empty message')
                    break

                logger.debug(
                    f'Received message: {len(income)}: {income[:20]}')

                try:
                    arr = unpack(income, 4000)
                    x = arr[37]
                    y = arr[38]
                    logger.debug(f'Parse array: {x} | {y}, {len(arr)}')
                    if x == 0:
                        t0 = time.time()
                        num = 0
                    num += 1
                    logger.debug('Package rate: {} milliseconds ({})'.format(
                        (time.time()-t0)/num * 1000, num))
                    pass
                except:
                    traceback.print_exc()
                    pass

            except KeyboardInterrupt:
                logger.error(f'Keyboard Interruption is detected')
                break

            except ConnectionResetError as err:
                logger.warning(
                    f'Connection reset occurs. It can be normal when server closes the connection.')
                break

            except Exception as err:
                detail = traceback.format_exc()
                print(f'E: {detail}')
                logger.error(f'Unexpected error: {err}')
                logger.debug(f'Unexpected error detail: {detail}')
                self.send(b'Something is wrong')
                break

        self.close()
        logger.info(f'Stopped listening to {self.serverIP}')

    def send(self, message):
        ''' Send [message] to server
        Args:
        - @message: The message to be sent
        '''
        self.client.sendall(message)
        logger.debug(f'Sent "{message}" to {self.serverIP}')


def keep_try():
    while True:
        try:
            client = TCPClient()
        except:
            traceback.print_exc()
        time.sleep(5)


if __name__ == '__main__':
    thread = threading.Thread(target=keep_try)
    thread.setDaemon(True)
    thread.start()

    while 'q' == input('Press q to Escape'):
        break

    print('Done')
