from attack import attack

import argparse
import can
import sys


def test(data, attack_type, data_exclude, interval, output):
    bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')
    # bus = "For testing"
    atk = attack(bus, data, data_exclude, float(interval), output)

    if   attack_type == "CRC"  : atk.wrong_CRC()
    elif attack_type == "END"  : atk.wrong_END()
    elif attack_type == "NON"  : atk.nonTERMINATE()
    elif attack_type == "DOS"  : atk.DoS()
    elif attack_type == "FUZZ" : atk.Fuzz()


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a', '--attack_type', choices=[ 'CRC', 'END', 'NON', 'DOS', 'FUZZ' ], dest = 'attack_type', required=True)
    parser.add_argument('-d', '--data', default="data/boot_idle.txt", dest = 'data', required=True)
    parser.add_argument('-e', '--data_exclude', default=None, dest = 'data_exclude')
    parser.add_argument('-i', '--interval', default="0.05", dest = 'interval')
    parser.add_argument('-o', '--attack_output', dest = 'output')
    parser.add_argument('-p', '--attack_parameters', dest = 'args')

    args = parser.parse_args()

    test(args.data, args.attack_type, args.data_exclude, args.interval, args.output)


if __name__ == "__main__":
    sys.exit(main())