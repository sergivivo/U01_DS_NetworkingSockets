# Python modules
import socket, pickle, time
import random as rnd
from datetime import datetime, timedelta

# Self made modules
from message import Message

host, port = "localhost", 12345

HELP_PROB = 0.3                      # probability of helping
CHK_MIN_TIME, CHK_MAX_TIME = 4., 15. # time interval to check for new messages
MSG_DEF = 'Sho te banco...'          # message to be sent

if __name__ == '__main__':
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((host, port))

    try:
        while True:
            # Sleep a random amount of time
            print("Sleep time")
            time.sleep(rnd.uniform(CHK_MIN_TIME, CHK_MAX_TIME))

            # Receive binary data
            print("Checking messages...")
            data = sock.recv(4096)

            if data:
                # Unpickle the object
                # We can retreive information because we have the Message class imported from the module
                msg = pickle.loads(data)

                print("]<-- Received message '%s'" % msg.msg)

                now = datetime.now()
                # Help under certain probability
                if rnd.uniform(0.,1.) > HELP_PROB:
                    print("]  x Not helping this time")
                # Compare datetimes to check if message has expired timestamp
                elif now > msg.expTime:
                    print("]  x Message expired at {}. Ignoring it...". format(msg.expTime))
                else:
                    print("]--> Sending support")
                    msg = Message(None, MSG_DEF) # sending confirmation for help
                    data = pickle.dumps(msg)
                    sock.send(data)
            else:
                print("No new messages.")

            print()

    except KeyboardInterrupt:
        pass

    sock.close()

