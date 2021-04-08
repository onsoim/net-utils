from attack import attack

import sys


def usage():
    print('python3 main.py [attack type] [attack options]')

    print('1. Wrong CRC')
    print('$ python3 main.py 1 10')

    print('2. Wrong END')
    print('$ python3 main.py 2')

    print('3. non Termination')
    print('$ python3 main.py 3')

    print('4. DoS')
    print('$ python3 main.py 4')

    print('5. Fuzz')
    print('$ python3 main.py 5')


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    
    type = sys.argv[1]
    if   type == "1": attack().wrong_CRC()
    elif type == "2": attack().wrong_END()
    elif type == "3": attack.nonTERMINATE()
    elif type == "4": attack.nonTERMINATE()
    elif type == "5": attack.nonTERMINATE()


if __name__ == "__main__":
    sys.exit(main())