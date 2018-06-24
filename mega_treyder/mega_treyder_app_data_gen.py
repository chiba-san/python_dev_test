import random
import string

DENOMINATION_PRICE = 1000
PAY_DAY = 30
SUM = 8000
LOTS = 5000

if __name__ == '__main__':
    fname = 'input.txt'
    with open(fname, 'w') as f:
        f.write("{:d} {:d} {:d}\n".format(PAY_DAY, LOTS, SUM))
        for i in range(PAY_DAY):
            for j in range(random.randint(0, LOTS)):
                bond_rand_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
                f.write("{:d} {:s} {:.3f} {:d}\n".format(i,
                                                         bond_rand_name,
                                                         random.uniform(90, 150),
                                                         random.randint(1, int(SUM/DENOMINATION_PRICE/4))))
    print('done')