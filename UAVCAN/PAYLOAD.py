class UAVCAN_PAYLOAD:
    def __init__(self, transfer_start = 0b1, transfer_end = 0b1, toggle = 0b0, transfer_ID = 0b00000):
        self.transfer_start = transfer_start
        self.transfer_end   = transfer_end
        self.toggle         = toggle
        self.transfer_ID    = transfer_ID

    def get_tail(self):
        return '{:02X}'.format((self.transfer_start << 7) + (self.transfer_end << 6) + (self.toggle << 5) + self.transfer_ID)

    # def tail(transfer_start, transfer_end, toggle, transfer_ID):
        

    def random():
        import os
        return ' '.join([ '{:02X}'.format(i) for i in os.urandom(7) ])
