import struct

class SetDataCodes():
    '''Sets the bram "bram_data_codes" to have addresses with a leading one
        to indicate end of frame at specified intervals, and the addresses
        immediately after to have trailing ones to send the mcnt at the beginning
        of each packet.
        IMPORTANT: Run this each time each time bram_len is changed'''
    def __init__(self, roach):
        self.fpga = roach
        self.spacing = 2
    def get_bram_len(self):
        return self.fpga.read_int('bram_len')
    '''def _set_eof(self, spacing):
        addr = 0
        while addr < self.get_bram_len():
            self.fpga.write('bram_data_codes', struct.pack('>I',2<<30), addr*4)
            addr += spacing'''
    def _set_header(self, spacing):
        addr = 0
        while addr <= self.get_bram_len():
            self.fpga.write('bram_data_codes',
                            struct.pack('>I', 0xffffffff), addr*4))
            addr += spacing
    def set_bram(self, spacing):
        #self.clear_bram()
        self._set_header(spacing)
        self.spacing = spacing
    def clear_bram(self):
        '''Finds all non-zero addresses in the bram, and sets them to 0'''
        loc = self.fpga.read('bram_data_codes',2<<16)
        i=0
        for x in loc:
            y = struct.unpack('>B',x)[0]
            if y != 0:
                self.fpga.write('bram_data_codes',struct.pack('>I',0),i-(i % 4))
            i += 1
        #addr = 0
        #while addr*4 < self.get_bram_len:
        #    self.fpga.write('bram_data_codes', struct.pack('>I',0), addr*4)
        #    self.fpga.write('bram_data_codes', struct.pack('>I',0), (addr+1)*4)
        #    addr += self.spacing

if __name__ == '__main__':
    import configure_roach
    roach = configure_roach.ROACH()
    sdc = SetDataCodes(roach.fpga)
    sdc.clear_bram()
    sdc.set_bram(875)
