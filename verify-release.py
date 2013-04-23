#!/usr/bin/env python

import sys
import getopt
import subprocess
import ast

class ReleaseVerifier:
    results = []
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def make_call(self, action):
        output = ""
        try:
            print "COMMAND: " + action["command"]
            if "cwd" in action:
                output = subprocess.check_output("cd " + action["cwd"] + "; " + action["command"], stderr=subprocess.STDOUT, shell=True)
            else:
                output = subprocess.check_output(action["command"], stderr=subprocess.STDOUT, shell=True)
            action["result"] = "PASS"
            action["output"] = output
            self.results.append(action)
            print "OUTPUT: " + output
        except:
            if action["must_work"]:
                action["result"] = "FAILED"
                action["output"] = output
                self.results.append(action)
                print "OUTPUT: " + output
                raise
            else:
                action["result"] = "WARNING"
                action["output"] = output
                self.results.append(action)
                print "OUTPUT: " + output

    def make_calls(self, input_commands):
        for action in input_commands:
            self.make_call(action)

    def print_results(self):
        for action in self.results:
            if action["result"]=="PASS":
                print "[" + self.OKGREEN + action["result"] + self.ENDC + "]\t\t" + action["command"]
            elif action["result"]=="WARNING":
                print "[" + self.WARNING + action["result"] + self.ENDC + "]\t" + action["command"]
            else:
                print "[" + self.FAIL + action["result"] + self.ENDC + "]\t" + action["command"]

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print 'verify-release.py -i <inputfile> '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'verify-release.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    myfile = open(inputfile, "r")
    inputfiletext=myfile.read()

    input_commands = ast.literal_eval(inputfiletext)
    x = ReleaseVerifier()
    x.make_calls(input_commands)
    x.print_results()

if __name__ == "__main__":
    main(sys.argv[1:])
