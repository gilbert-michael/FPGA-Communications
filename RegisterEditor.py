import corr
import struct

class RegisterEditor():
    '''
    A class for opening and editing software registers
    on a ROACH.
    '''
    def __init__(self,roach):
        '''takes the name of the register as an argument'''
        self.roach=roach
        self.reg='sys_scratchpad'
    def target(self, register):
        '''sets a register to be the default for write and read commands'''
        self.reg=register
    def write(self, value, target=self.reg): #, offset=0): #note: Big Endian
        self.roach.write_int(target, value)
    def read(self, target=self.reg):#, size, offset=0):
        print 'Signed:', self.roach.read_int(target),\
            '\nUnsigned:', self.roach.read_uint(target)
    def get_roach_name(self):
        return self.roach
    def list_registers(self):
        c=self.roach
        print c.listdev()

class BramEditor(RegisterEditor):
        def __init__(self, roach):
            RegisterEditor.__init__(self, roach)
        def write(self, value, target = self.reg, offset = 0):
            '''Writes an integer value to a register.  The target register
            defaults to the target set, and the byte offset defaults to 0'''
            valstring = bin(value)[2:]
            packed = ''
            while len(valstring) > 32:
                packed += struct.pack('>I', int(valstring[:32], 2))
                valstring = valstring[32:]
            valstring += '0' * (32 - len(valstring))
            packed += struct.pack('>I', int(valstring[:32], 2))
            self.roach.write(self.reg, offset, packed)
        def read(self, target = self.reg, offset = 0):
            #TEMPORARY
            output = self.roach.read(target, 4, offset)
            print struct.unpack('>I',output)

if __name__ == '__main__':
    roach=corr.katcp_wrapper.FpgaClient(roach, '7147')
    re=RegisterEditor(roach)
    be=BramEditor(roach)

"""def RegSetter():
    ''' 
    Takes manual input to set registers
    '''
    regedit=RegisterEditor(corr.katcp_wrapper.FpgaClient('roach',7147))
    temp=corr.katcp_wrapper.FpgaClient('roach',7147)#regedit.get_roach_name()
    registers=temp.listdev()
    print 'Available registers'
    i=0
    for reg in registers:
        print i,' ',reg
        i += 1
    while True:
        print 'Which register to modify (q to quit)? /n'
        try:
            j=input('Register number: ')
            if j == 'q':
                return
            else:
                regedit.target_reg(registers[j])
        except(IndexError):
            print 'Index out of range, try again'
            continue
        except(TypeError):
            print 'Please enter an integer'
            continue
        else:
            break
    print 'Current Register Value:' + regedit.get_reg() + ''
    while True:
        try:
            value=input('New Value for register' + registers[j] + '(x to undo, q to quit): ')
            if value == 'x': break
            elif value == 'q': r/eturn
            regedit.set_reg(value)
        except(TypeError):
            print 'Please use proper data format'
            continue
        except(SyntaxError):
            print 'Syntax Error: Try Again'
            continue
        else:
            break
    RegSetter()
RegSetter()
"""
