import random

SHARES_COUNT = 100000000

if __name__ == '__main__':
    fname = 'input.txt'
    with open(fname,'w')as f:
        f.write("{:d}\n".format(SHARES_COUNT))
        for i in range(SHARES_COUNT):
            f.write("{:.1f}\n".format(random.uniform(1.5, 10)))
    print('done')