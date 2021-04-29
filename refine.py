import argparse
import sys


def diffing(attack, dump, output):
    with open(attack)as f: attacks  = f.readlines()[ 1 : ]
    with open(dump)  as f: dumps    = f.readlines()

    for attack in attacks:
        s = (list(filter(None, attack.split(' '))))
        # print(s[3].upper())         # AID
        # print(s[6])                 # DLC
        # print(' '.join(s[ 7 : ]))   # DATA
        atk = f'{s[3].upper()}   [{s[6]}]  {" ".join(s[ 7 : ])[ : -1 ].upper()}'

        # n + m
        ''' two pointers
        while atk not in dumps[index]:
            print(dumps[index], end='')
            index += 1
            # t.__next__()
            # print(atk)
        index += 1
        '''

        # n * m
        flag = True
        for dump in dumps:
            if atk in dump:
                flag = False
                dumps.remove(dump)
                break
        if flag: print(attack, atk, end="\n\n")
    
    res = "".join(dumps)
    if output:
        with open(output, 'w') as f:
            f.write(res)


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a', '--attack', dest = 'attack', required = True)
    parser.add_argument('-d', '--dump', dest = 'dump', required = True)
    parser.add_argument('-o', '--output', dest = 'output')

    args = parser.parse_args()

    diffing(args.attack, args.dump, args.output)


if __name__ == "__main__":
    sys.exit(main())
