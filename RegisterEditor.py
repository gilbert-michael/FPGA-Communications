import corr

class RegisterEditor():
    '''
    A class for opening and editing software registers
    on a ROACH.
    '''
    def __init__(self,roach):
        '''takes the name of the register as an argument'''
        self.reg=reg_name
	self.roach=roach
    def target_reg(self, register)
        self.reg_name=register
    def set_reg(self, value): #, offset=0): #note: Big Endian
        self.roach.write_int(self.reg_name, value)
    def get_reg(self):#, size, offset=0):
        print 'Signed:', self.roach.read_int('status_signed'),\
               '\nUnsigned:', self.roach.read_uint('status_unsigned')
    def get_target_reg(self)
        return self.reg_name

def RegSetter():
    ''' 
    Takes manual input to set registers
    '''
    regedit=RegisterEditor(corr.katcp_wrapper.FpgaClient('roach',7147)
    registers=regedit.roach.listdev()
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
                return pass
            else:
                regedit.target_reg(registers[j]])
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
            elif value == 'q': return pass
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
