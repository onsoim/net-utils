class UAVCAN_AID:
    def __init__(self):
        pass
    
    def get_aid_service(self, 
                        priority: int,
                        service_id: int,
                        is_request: int,
                        destination_node_id: int,
                        is_service: int,
                        source_node_id: int) -> int:
        def assert_field(value: int, width: int) -> None:
            assert isinstance(value, int)
            assert 0 <= value < 2 ** width, '0 <= value <= {}'.format(2 ** width)

        assert_field(priority, 5)
        assert_field(service_id, 8)
        assert_field(is_request, 1)
        assert_field(destination_node_id, 7)
        assert_field(is_service, 1)
        assert_field(source_node_id, 7)

        aid = 0
        aid += priority << 24
        aid += service_id << 16
        aid += is_request << 15
        aid += destination_node_id << 8
        aid += is_service << 7
        aid += source_node_id << 0

        return aid

    def get_value(self, value, n_bits, bitidx):
        return (value >> bitidx) & ((2 ** n_bits) - 1)

    def dissect_aid_service(self, aid):
        print('priority={}'.format(self.get_value(aid, 5, 24)), end='\t')
        print('service_id={}'.format(self.get_value(aid, 8, 16)), end='\t')
        print('is_request={}'.format(self.get_value(aid, 1, 15)), end='\t')
        print('destination_node_id={}'.format(self.get_value(aid, 7, 8)), end='\t')
        print('is_service={}'.format(self.get_value(aid, 1, 7)), end='\t')
        print('source_node_id={}'.format(self.get_value(aid, 7, 0)))
