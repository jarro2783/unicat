#!/usr/bin/python

from __future__ import print_function

import numpy as np
import sys
#from uniclass.generators.cxx import cxx
import jinja2

class Category:
    def __init__(self):
        self.current = None
        self.__ranges = []

    def add(self, cp):
        if self.current is None:
            self.current = [cp, cp]
            self.__ranges.append(self.current)
        else:
            if self.current[1] == cp - 1:
                self.current[1] = cp
            else:
                self.current = [cp, cp]
                self.__ranges.append(self.current)

    def add_first(self, cp):
        self.__ranges.append([cp, cp])

    def add_last(self, cp):
        self.__ranges[-1][1] = cp
        self.current = None

    def count(self):
        return len(self.__ranges)

    def ranges(self):
        return self.__ranges


class UnicodeClasses:
    def __init__(self):
        self.categories = {}

    def __category(self, cat):
        if cat not in self.categories:
            self.categories[cat] = Category()

        return self.categories[cat]
        

    def add(self, cp, cat):
        self.__category(cat).add(cp)
        general = cat[0]
        self.__category(general).add(cp)

    def add_first(self, cp, cat):
        self.__category(cat).add_first(cp) 
        general = cat[0]
        self.__category(general).add_first(cp)

    def add_last(self, cp, cat):
        self.__category(cat).add_last(cp)
        general = cat[0]
        self.__category(general).add_last(cp)

    def count(self):
        for cat in sorted(self.categories.keys()):
            print("{}: {}".format(cat, self.categories[cat].count()))

    def print_ranges(self):
        for cat in sorted(self.categories.keys()):
            print("{}: {}".format(cat, self.categories[cat].ranges()))

class Indenter:
    def __init__(self, n, out):
        self.__n = n
        self.__out = out

    def write(self, s):
        self.__out.write(self.__n * " ")
        self.__out.write(s)

class Holder:
    pass

def write_range(rr, out, name):
    out.write("std::pair<int, int> {}[] = {{\n".format(name))
    for r in rr:
        out.write("  {{0x{:x}, 0x{:x}}},\n".format(r[0], r[1]))
    out.write("};\n")

        

def main():
    ucd = open("UnicodeData.txt")

    classes = {}

    uc = UnicodeClasses()

    n = 0
    for l in ucd.readlines():
        if n % 100 == 0:
            print('.', end="")
            sys.stdout.flush()
        try:
            fields = l.split(';')
            codepoint = int(fields[0], 16)
            desc = fields[1]

            cat = fields[2]

            # don't worry about errors here, we assume that Unicode can
            # provide a valid spec file
            if desc[-6:] == "First>":
                uc.add_first(codepoint, cat)
            elif desc[-5:] == "Last>":
                uc.add_last(codepoint, cat)
            else:
                uc.add(codepoint, cat)

        except IndexError:
            print("Index error in {}".format(l))

        n += 1

    print("")

    uc.count()

    print("Copying to jinja variables")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    writer = env.get_template('cxx')

    cat = []
    for key in sorted(uc.categories.keys()):
        rr = uc.categories[key].ranges()
        ranges = []
        for r in rr:
            toadd = Holder()
            toadd.begin = r[0]
            toadd.end = r[1]
            ranges.append(toadd)
        c = Holder()
        c.name = key
        c.ranges = ranges
        cat.append(c)

    #writer = cxx()
    #writer.categories = cat

    print("Generating C++")
    out = open("uniclass.h", "w")
    out.write(writer.render(categories=cat))

    #out.write("namespace uniclass {\n")

    #out.write("  namespace cat {\n")

    #for key in sorted(uc.categories.keys()):
    #    write_range(uc.categories[key].ranges(), Indenter(4, out), key)

    #out.write("  }\n}\n")
    #out.close()
    print("Done")

if __name__ == '__main__':
    main()
