#!/usr/bin/env python
'''
maintains a jump-list of the directories you actually use

INSTALL:
  * put something like this in your .bashrc:
    export JPY=/path/to/j.py # tells j.sh where the python script is
    . /path/to/j.sh          # provides the j() function
  * make sure j.py is executable
  * cd around for a while to build up the db
  * PROFIT!!

USE:
  * j foo     # goes to most frecent dir matching foo
  * j foo bar # goes to most frecent dir matching foo and bar
  * j -t rank # goes to highest ranked dir matching foo
  * j -l foo  # list all dirs matching foo
'''

import os, sys, time

class J(object):

    def __init__(self, datafile):
        ''' datafile format: path|rank|atime '''
        self.datafile = datafile
        self.common = None
        self.args = []
        self.m = []
        self.ordered = { 'rank' : self.rank,
                         'recent' : self.recent,
                         'frecent': self.frecent }
        # get list
        try:
            with open(self.datafile, 'r') as f:
                self.d = [l.strip().split('|') for l in f.readlines()]
            self.d = [d for d in self.d if os.path.exists(d[0])]
        except:
            self.d = []

        # rewrite to disk
        with open(self.datafile, 'w') as f:
            f.write('\n'.join(['|'.join(d) for d in self.d]))
            f.write('\n')

    def pretty(self, order):
        ''' return a listing by order '''
        if order not in self.ordered:
            return ''
        r = ['by %s' % order]
        r.extend(['%-15s %s' % i for i in self.ordered[order]()])
        return '\n'.join(r)

    def go(self, order):
        ''' go by order '''
        if order == 'common':
            return self.common
        if self.m and order in self.ordered:
            return self.ordered[order]()[-1][1]

    def rank(self):
        ''' time spent/aging, taken care of in .sh '''
        r = ([(i[0], i[2]) for i in self.m])
        return sorted(r)

    def recent(self):
        ''' by recently accessed '''
        r = ([(i[1], i[2]) for i in self.m])
        return sorted(r, reverse=True)

    def frecent(self):
        ''' rank weighted by recently accessed '''
        r = []
        for i in self.m:
            if i[1] <= 3600:
                r.append((i[0]*4, i[2]))
            elif i[1] <= 86400:
                r.append((i[0]*2, i[2]))
            elif i[1] <= 604800:
                r.append((i[0]/2, i[2]))
            else:
                r.append((i[0]/4, i[2]))
        return sorted(r)

    def matches(self, args, nocase=False):
        '''
        set self.m to a list of possibly case sensitive path matches
        m format: (rank, atime, path)
        '''

        def common(r, l, nocase):
            '''
            return prefix if there's a common prefix to all matches,
            the prefix is in the list,
            and all the args match in it
            '''
            pref = os.path.commonprefix([i[2] for i in r])
            if not pref or pref == '/':
                return None
            r = [i for i in r if i[2] == pref]
            if not r:
                return None
            if nocase:
                pref = pref.lower()
            for i in l:
                if i not in pref:
                    return None
            return r[0][2]

        def cmpare(str, l, nocase):
            ''' every item in list l must match in string str '''
            match = True
            if nocase:
                str = str.lower()
            for i in l:
                if i not in str:
                    match = False
            return match

        self.args, self.m = args, []
        if nocase:
            args = [i.lower() for i in args]
        for d in self.d:
            if not cmpare(d[0], args, nocase):
                continue
            self.m.append((float(d[1]),
                           int(time.time())-int(d[2]),
                           d[0]))
        self.common = common(self.m, args, nocase)
        return self.m

def main(file, list, type, args):
    ''' make sure the only thing that gets to stdout is a place to cd '''
    if not file:
        return

    # if we hit enter on a completion, go there
    if args and os.path.isdir(args[-1]):
        sys.stdout.write(os.path.realpath(args[-1]))
        return

    j = J(file)

    # prefer case sensitive
    if not j.matches(args):
        j.matches(args, True)

    if list or not args:
        sys.stderr.write(j.pretty(type) + '\n')
        if j.common:
            sys.stderr.write('common: %s\n' % j.common)
    # if all our args match a common prefix, let's go there
    elif j.common:
        sys.stdout.write(j.common)
    else:
        go = j.go(type)
        if not go:
            return
        sys.stdout.write(go)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog -f datafile [options] args')
    parser.add_option('-f', '--file', help='data file')
    parser.add_option('-l', action='store_true', default=False,
                      help='list matches')
    parser.add_option('-t', default='frecent',
                      help='match type [frecent (default), rank, recent]')
    parser.add_option('-V', action='store_true', default=False,
                      help='documentation')
    saveout = sys.stdout
    sys.stdout = sys.stderr
    opts, args = parser.parse_args()
    if opts.V:
        sys.stdout.write(__doc__)
    elif not opts.file:
        parser.error('data file required (-f file)')
    elif opts.t not in ['frecent', 'rank', 'recent']:
        parser.print_help()
    else:
        sys.stdout = saveout
        main(opts.file, opts.l, opts.t, args)
