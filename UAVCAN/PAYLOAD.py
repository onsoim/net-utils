class UAVCAN_PAYLOAD:
    def tail(transfer_start, transfer_end, toggle, transfer_ID):
        return f' {(transfer_start << 7) + (transfer_end << 6) + (toggle << 5) + transfer_ID:02X}'

    def random():
        import os
        return ' '.join([ f'{i:02X}' for i in os.urandom(7) ])
