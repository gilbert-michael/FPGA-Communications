import socket, Queue, multiprocessing, time, struct
        
class Catcher(multiprocessing.Process):
    '''A generator of udp receiving threads that save output as raw strings'''
    def __init__(self, sock, threadnum, queue, maxsize = 10**8, bsize = 875*8):
        self.sock = sock
        self.threadnum = threadnum
        self.bsize = bsize
        self.then = time.time()
        self.q = queue
        multiprocessing.Process.__init__(self)
    def run(self):
        global til
        while time.time() < til:
            self.q.put(self.sock.recv(self.bsize))
        print'Receive Success %d' %self.threadnum
        self.sock.close()

class Test(object):
    ''' Tests the performance of the catcher class.
        After the class is constructed, start using the start method. '''
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('192.168.2.1',6000))
        print 'Socket Initialized\n'
    def start(self, threads = 6, bsize = 7000, recv_for = 1):
        '''
        Starts a given number of processes (default 6), and receives packets
        with a size given in bytes (default 7000 bytes)
        for a given amount of time.)
        '''
        global til
        til = time.time() + recv_for
        q = multiprocessing.Queue()
        l =[]
        packet_num = 0
        for x in range(threads):
            print 'Start thread %d' %(x+1)
            Catcher(self.sock, x+1, q).start()
        while True:
            try:
                l.append(q.get(timeout = .5))
                #packet_num += 1
            except(Queue.Empty):
                data = ''.join(l)
                #with open('dataudp','wb') as f:
                    #f.write(data)
                break
        #print '%d packets worth of data and %d packets written at %f Gbps'\
        #      %(len(data)/bsize, packet_num, len(data)*8./recv_for/10**9)
        header_list = []
        e = 0
        p = zip(*[iter(data[:bsize])]*4)
        for i in p: #finds the header in a packet of all zeroes
            j = ''.join(i)
            if j != '\x00\x00\x00\x00':
                break
            e += 1
        o = zip(data[4*e::bsize],data[4*e+1::bsize],
            data[4*e+2::bsize],data[4*e+3::bsize])
        for i in o: #puts the headers into a list
            k = struct.unpack('>I',''.join(i))[0]
            header_list.append(k)
        print header_list[:10]
        header_list.sort()
        dropcount = -(struct.unpack('>I',j)[0])
        a = 0
        for i in header_list: #finds gaps in the packet numbers
            b = a
            a = i
            if (a - b) != 1:
                dropcount += a - b - 1
        print dropcount
        return([recv_for, len(data), dropcount == 0])

if __name__ == '__main__':
    g = Test()
    print g.start(recv_for = 1)
