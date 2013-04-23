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

    def __init__(self, input_commands, version, commitsh):
        self.input_commands = input_commands
        self.version = version
        self.commitsh = commitsh

    def do_replacements(self, toclean):
        toclean = toclean.replace("${commit-sh}", self.commitsh)
        toclean = toclean.replace("${version}", self.version)
        return toclean

    def make_call(self, action):
        output = ""
        action["command"] = self.do_replacements(action["command"])
        if "cwd" in action:
            action["cwd"] = self.do_replacements(action["cwd"])

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

    def make_calls(self):
        for action in self.input_commands:
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
    version = ''
    commitsh = ''
    try:
        opts, args = getopt.getopt(argv,"hi:c:v:")
    except getopt.GetoptError:
        print 'verify-release.py -i <inputfile> -c <commit-sh> -v <version>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'verify-release.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-c"):
            commitsh = arg
        elif opt in ("-v"):
            version = arg

    myfile = open(inputfile, "r")
    inputfiletext=myfile.read()

    input_commands = ast.literal_eval(inputfiletext)
    x = ReleaseVerifier(input_commands, version, commitsh)
    x.make_calls()
    x.print_results()

if __name__ == "__main__":
    main(sys.argv[1:])
