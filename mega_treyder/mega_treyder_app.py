import os
import time
import sys


PAY_DAY = 30


class Bond:

    denomination_price = 1000

    def __init__(self, day,  name, price, count):
        self.day = day
        self.name = name
        self.price = price
        self.count = count

    @staticmethod
    def create(input_str):
        inputs = str(input_str).split(' ')
        return Bond(int(inputs[0]), inputs[1], float(inputs[2]), int(inputs[3]))

    def denomination(self):
        return self.count * self.denomination_price

    def real(self):
        return self.denomination() * self.price / 100

    def profit(self, days):
        return self.denomination() + self.count * (days - self.day) - self.real()

    def __str__(self):
        return "{:d} {:s} {:.3f} {:d}\n".format(self.day, self.name, self.price, self.count)


class Node:

    def __init__(self, bond):
        self.left = None
        self.right = None
        self.bond = bond

    def insert_bond(self, bond, days):
        global S
        # exclude lots which are more expensive than we have
        if bond.denomination() <= S:
            if self.bond:
                current_bond_profit = self.bond.profit(days)
                new_bond_profit = bond.profit(days)

                if new_bond_profit > current_bond_profit:
                    if self.left is None:
                        self.left = Node(bond)
                    else:
                        self.left.insert_bond(bond, days)
                elif new_bond_profit < current_bond_profit:
                    if self.right is None:
                        self.right = Node(bond)
                    else:
                        self.right.insert_bond(bond, days)
            else:
                self.bond = bond

    def print_tree(self, days, output_file):
        if self.left:
            self.left.print_tree(days, output_file)

        # check if we spend all money and print bond otherwise
        global S
        S -= self.bond.real()
        if S > 0:
            global result
            result += self.bond.profit(days)
            output_file.write(str(self.bond))
        else:
            return result

        if self.right:
            self.right.print_tree(days, output_file)


def read_settings(settings_str):
    inputs = str(settings_str).split(' ')
    return int(inputs[0]), int(inputs[1]), float(inputs[2])


if __name__ == '__main__':

    input_file_name = "input.txt"
    output_file_name = "output.txt"

    print("reading started\n")
    start = time.time()

    with open(input_file_name, 'r') as input_file:
        N, M, S = read_settings(input_file.readline())
        print('N = {:d}, M = {:d}, S = {:f}'.format(N, M, S))

        # create a binary tree for storing bonds
        root = Node(Bond.create(input_file.readline()))
        for ln in input_file:
            root.insert_bond(Bond.create(ln), N+PAY_DAY)

    done = time.time()
    elapsed = done - start
    print("reading and binary tree creation complete in {:f} sec\n".format(elapsed))

    result = 0
    try:
        # clear temporary file
        with open('tmp', 'w'):
            pass

        print("binary tree to tmp file writing started\n")
        start = time.time()

        # open a new file to print best bonds from the tree
        with open('tmp', 'r+') as tmp_f:
            # get the best profit along with tmp file filled with bonds
            root.print_tree(N+PAY_DAY, tmp_f)

            done = time.time()
            elapsed = done - start
            print("binary tree to tmp file writing complete in {:f} sec\n".format(elapsed))

            print("rewriting binary tree with profit value started\n")
            start = time.time()

            # in order to put profit at the start we need to copy lines from tmp to output file after
            with open(output_file_name, 'w') as output_f:
                output_f.write("{:.3f}\n".format(result))
                tmp_f.seek(0)
                for ln in tmp_f:
                    output_f.write(ln)

            done = time.time()
            elapsed = done - start
            print("rewriting binary tree with profit value complete in {:f} sec\n".format(elapsed))
            os.remove('tmp')

        print("output file size is {:f} Kb\n".format(os.path.getsize(output_file_name) / 1024))

    except Exception as ex:
        print(ex)
