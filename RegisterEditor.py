import corr, struct

class RegisterEditor():
    '''
    A class for opening and editing software registers
    on a ROACH.
    '''
    def __init__(self, roach = corr.katcp_wrapper.FpgaClient('roach',7147)):
        '''takes the name of the register as an argument'''
        self.roach=roach
        self.reg='sys_scratchpad'
    def target(self, register):
        '''sets a register to be the default for write and read commands'''
        if register in self.list_registers():
            self.reg=register
        else:
            print 'Not a register'
    def write(self, value, target = None): #, offset=0): #note: Big Endian
        if target == None: target = self.reg
        self.roach.write_int(target, value)
    def read(self, target = None):#, size, offset=0):
        if target == None: target = self.reg
        print 'Signed:', self.roach.read_int(target),\
            '\nUnsigned:', self.roach.read_uint(target)
    def get_roach_name(self):
        return self.roach
    def listdev(self):
        c=self.roach
        for x in c.listdev(): print x

class BramEditor(RegisterEditor):
    '''
    A class for opening and editing block RAM on a roach
    '''
    def __init__(self, *args):
        RegisterEditor.__init__(self, *args)
        self.reg=None
    def write(self, value, target = None, offset = 0):
        '''Writes an integer value to a register.  The target register
        defaults to the target set, and the byte offset defaults to 0'''
        if target == None: target = self.reg
        if value.__class__ == str:
            packed = value
        else:
            valstring = bin(value)[2:] #converts from int to binary string, removes '0b'
            packed = ''
            mod = len(valstring) % 32 #finds how many zeroes must be prepended to fit
            if mod != 0:
                valstring = '0' * (32 - mod) + valstring #prepends zeroes
            while len(valstring) > 0:
                packed += struct.pack('>I', int(valstring[:32], 2))
                valstring = valstring[32:]
        self.roach.write(self.reg, packed, offset)
    def read(self, target = None, length=4, offset = 0):
        if target == None: target = self.reg
        output = self.roach.read(target, length, offset)
        print 'Raw: ', output, '\n', 'Unsigned int: ', struct.unpack('>I',output)
    
