# Python modules
import socketserver, pickle              # pickle for serialization of objects
import threading                         # synchronization of threads
import random as rnd
from datetime import datetime, timedelta # access to clock and operations with time
import time                              # sleep

# Self made modules
from message import Message



# The server based on threads for each connection
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class Worker(socketserver.StreamRequestHandler):

    # Constants
    N_HELPERS = 3
    N_NEEDED = 2
    MSG_DEF = 'Ashuda!'

    # Time intervals
    EXP_MIN_TIME, EXP_MAX_TIME = 5., 10.
    WORK_MIN_TIME, WORK_MAX_TIME = 3., 5.

    ITERATION_STATS = 3 # Iterations needed to display stats

    # Shared memory
    helpers = 0
    helping = 0

    msg = None
    data = None
    timeout = 15.

    # Statistics
    requests = 0
    helpful  = 0

    # Concurrency
    lock    = threading.Lock()     # Mutual exclusion
    barrier = threading.Barrier(3) # Will help us synchronize handle threads

    def handle(self):
        print("Connected: %s on %s" % (self.client_address,threading.current_thread().name))

        self._barrierHandle() # sync all threads

        while True:
            # Sending the help request
            print("|--> Requesting support to %s" % (self.client_address,))
            with Worker.lock:
                self.request.sendall(Worker.data) # send it as a byte stream

            # Waiting for answers
            self.request.settimeout(Worker.timeout)
            try:
                data = self.request.recv(4096)
                msg = pickle.loads(data)
                print("|<-- Received support from %s: '%s'" % (self.client_address, msg.msg))

                self._helpReceiveHandle()

            # Timeout reached
            except TimeoutError:
                print("|  x Denied support from %s" % (self.client_address,))

            self._barrierHandle()


    def _barrierHandle(self):
        # Count threads
        with Worker.lock:
            Worker.helpers += 1
            if Worker.helpers == Worker.N_HELPERS:
                # Show stats after a number of iterations
                if Worker.requests > 0 and Worker.requests % Worker.ITERATION_STATS == 0:
                    Worker.showStats()

                # Last thread will generate a new message
                Worker._helpRequestHandle()
                Worker.helpers = 0
                Worker.helping = 0

        # Synchronize threads
        Worker.barrier.wait()

    @classmethod
    def _helpRequestHandle(cls):
        # Random time waiting till next help message
        print()
        print("Working on my own...")
        time.sleep(rnd.uniform(cls.WORK_MIN_TIME, cls.WORK_MAX_TIME))

        # Create a new message setting an expiration date
        print("Uh, I need help")
        exp_time = timedelta(seconds=rnd.uniform(cls.EXP_MIN_TIME, cls.EXP_MAX_TIME))
        cls.timeout = exp_time.total_seconds()

        exp_dt = datetime.now() + exp_time
        cls.msg = Message(exp_dt, cls.MSG_DEF)

        # Create the data string of the object using pickle
        cls.data = pickle.dumps(cls.msg)

        # Counter for statistics
        Worker.requests += 1


    def _helpReceiveHandle(self):
        with Worker.lock:
            Worker.helping += 1
            print("  {}/{} support needed".format(Worker.helping, Worker.N_NEEDED))

            # Last thread will notify succesful helping
            if Worker.helping == Worker.N_NEEDED:
                print("Successfully helped!")
                Worker.helpful += 1

    @classmethod
    def showStats(cls):
        print()
        print("================ STATS =================")
        print("  Help requests : %d" % cls.requests)
        print("   Times helped : %d" % cls.helpful)
        print("     Help ratio : %.1f%%" % (cls.helpful * 100. / cls.requests))
        print("========================================")


if __name__ == '__main__':
    server = ThreadedTCPServer(('', 12345), Worker)

    try:
        print('The server is running...')
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()

