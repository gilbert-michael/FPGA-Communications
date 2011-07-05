import socket, Queue, threading, multiprocessing, time, struct, cPickle as pickle

class catcher(multiprocessing.Process):
    '''A generator of udp receiving threads.  Pickles to save output'''
    def __init__(self, sock, threadnum, queue, r, maxsize = 10**8, bsize = 875*8):
        self.sock = sock
        self.threadnum = threadnum
        self.bsize = bsize
        self.maxsize = maxsize
        self.then = time.time()
        rec_size = r
        q = queue
        multiprocessing.Process.__init__(self)
        print 'init Thread %d success.' %threadnum
    def run(self):
        #Grabs packets from the pipe, if one is available
        print 'Begin run'
        l = []
        while rec_size.value < self.maxsize:
            data, source = self.sock.recvfrom(self.bsize)
            l.append(data)
            rec_size.value += self.bsize
        print 'Receive Success.  Begin write.'
        with open('data' + str(self.threadnum),'wb') as f:
            pickle.dump(l,f)
        self.sock.close()
        print time.time()-then, '\n',rec_size.value,'\n'
        
class CatchNoPickle(catcher):
    '''A generator of udp receiving threads that save output as raw strings'''
    def __init__(self,*args,**kwargs):
        catcher.__init__(self,*args,**kwargs)
    def run(self):
        #Grabs packets from the pipe, if one is available
        #l = []
        global rec_size
        while rec_size < self.maxsize:
            data, source = self.sock.recvfrom(self.bsize)
            q.put(data)
            #l.append(data)
            rec_size += self.bsize
        print'Receive Success.  Begin write.'
        #output = ''.join(l)
        #with open('data' + str(self.threadnum),'wb') as f:
            #f.write(output)
        #q.put(output)
        self.sock.close()
        print time.time()-self.then, 'seconds'
        
if __name__ == '__main__':
    q = multiprocessing.Queue()
    adj = 0
    rec_size = 0 #multiprocessing.Value('i',0)
    l =[]
    bsize = 7000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('192.168.2.1',6000))
    print 'Socket Initialized\n'
    for x in range(7):
        print 'Start thread %d \n' %(x+1)
        CatchNoPickle(sock, x+1, q, rec_size).start()
    while True:
        try:
            l.append(q.get(timeout = 2))
        except(Queue.Empty):
            with open('dataudp','wb') as f:
                f.write(''.join(l))
            break
    print len(''.join(l))/bsize, 'packets written.'
    a = struct.unpack('>%dI'%(len(''.join(l))/4),''.join(l))
    p=[]
    for i in a:
        if i != 0:
            p.append(i)
    print len(p)-len(set(p)), 'duplicates.'
    print(sorted(p))[-100:]
