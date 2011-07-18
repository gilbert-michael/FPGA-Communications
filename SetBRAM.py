from corr import katcp_wrapper as kw
import struct, time

class SetDataCodes(object):
    '''Sets the bram "bram_data_codes" to have addresses with a leading one
        to indicate end of frame at specified intervals, and the addresses
        immediately after to have trailing ones to send the mcnt at the beginning
        of each packet.
        IMPORTANT: Run this each time each time bram_len is changed'''
    def __init__(self, roach = kw.FpgaClient('roach', 7147)):
        self.fpga = roach
        self.spacing = 2
    def set_header(self, addr = 0):
        self.fpga.write('bram_data_codes',
                        struct.pack('>I', 0x7fffffff), addr*4)
    def set_eof(self, addr = 0):
        self.fpga.write('bram_data_codes',
                        struct.pack('>I', 2<<30), addr*4)
    def set_bram_len(self, size):
        self.fpga.write_int('bram_len', size)
    def set_bram(self, spacing, addr = 0, offset = 0):
        #self.clear_bram()
        if offset == 0:
            while addr + offset <= 2**15:
                self.fpga.write('bram_data_codes',
                struct.pack('>I', 0xffffffff), addr*4)
                addr += spacing
        else:
            while addr + offset <= 2**15:
                self.set_header(addr + offset)
                self.set_eof(addr)
                addr += spacing
    def clear_bram(self, target = 'bram_data_codes'):
        '''Finds all non-zero addresses in the bram, and sets them to 0'''
        loc = self.fpga.read(target,2<<16)
        i=0
        for x in loc:
            y = struct.unpack('>B',x)[0]
            if y != 0:
                self.fpga.write('bram_data_codes',struct.pack('>I',0),i-(i % 4))
            i += 1
        #    self.fpga.write('bram_data_codes', struct.pack('>I',0), addr*4)
        #    self.fpga.write('bram_data_codes', struct.pack('>I',0), (addr+1)*4)
        #    addr += self.spacing
        
class SetSpead(object):
    def __init__(self, roach = kw.FpgaClient('roach', 7147)):
        self.fpga = roach
        self.sdc = SetDataCodes(roach)
        
    def run(self, addr = 0):
        PACKET_HEADER = '\x83\x04\x40\x28\x00\x00\x00\x05'
        HEAP_LEN_ID = '\x80\x00\x02' # top bit is 1, bottom is 2
        HEAP_CNT_ID = '\x80\x00\x01' # top bit is 1, bottom is 1
        PAYLOAD_LEN_ID = '\x80\x00\x04'
        PAYLOAD_OFF_ID = '\x80\x00\x03'
        ITEM_ID = '\x00\x14\x08' # can be any number above 4096
        
        heap_length = '\x00\x00\x02\x00\x00' # = 2**17
        payload_length = '\x00\x00\x00\x10\x00'# = 4096
        counter = '\x00\x00\x00\x00\x00' # to be replaced on the fpga
        for i in xrange(0, 31*4096, 4096):
            spead = PACKET_HEADER\
                + HEAP_LEN_ID + heap_length\
                + HEAP_CNT_ID + counter\
                + PAYLOAD_LEN_ID + payload_length\
                + PAYLOAD_OFF_ID + '\x00' + struct.pack('>I',i)\
                + ITEM_ID + '\x00\x00\x00\x00\x00'
            assert len(spead) == 48
            x = [''.join(i) for i in zip(*[iter(spead)]*4)]
            lsb = ''.join(x[1::2])
            msb = ''.join(x[::2])
            self.fpga.write('bram_data_lsb', lsb, addr*4)
            self.fpga.write('bram_data_msb', msb, addr*4)
            self.sdc.set_header(4*(addr + 2))
            addr += 67
            self.sdc.set_eof(4*(addr - 1))
        return addr

if __name__ == '__main__':
    sdc = SetDataCodes()
    time.sleep(1)
    spead = SetSpead()
    time.sleep(1)
    sdc.clear_bram()
    sdc.clear_bram('bram_data_lsb')
    sdc.clear_bram('bram_data_msb')
    x = spead.run()
    sdc.set_bram_len(x)
