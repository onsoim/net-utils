from attack import attack

import argparse
import can
import sys


def test(data, attack_type):
    bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')
    # bus = "For testing"
    atk = attack(bus, data)

    if   attack_type == "CRC"  : atk.wrong_CRC()
    elif attack_type == "END"  : atk.wrong_END()
    elif attack_type == "NON"  : atk.nonTERMINATE()
    elif attack_type == "DOS"  : atk.DoS()
    elif attack_type == "FUZZ" : atk.Fuzz()


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a', '--attack_type', choices=[ 'CRC', 'END', 'NON', 'DOS', 'FUZZ' ], dest = 'attack_type', required=True)
    parser.add_argument('-d', '--data', default="data/boot_idle.txt", dest = 'data', required=True)
    parser.add_argument('-p', '--attack_parameters', dest = 'args')

    args = parser.parse_args()

    test(args.data, args.attack_type)


if __name__ == "__main__":
    sys.exit(main())