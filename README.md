cloudstack-release-verification-tool
====================================

A python script used to more automatically verify Apache CloudStack release candidates.

This was created to make the more repititive aspects of verifying an Apache CloudStack release easier to complete, although it can be generalized by editing the instructions.conf file to suite your needs.

How to run:

./verify-release.py -i instructions.conf

How to edit instructions.conf (or your own file):

The format of the file is expected to be a python list, containing dictionary objects that describe steps to be executed.  The parent object is a list specifically to ensure that the commands are executed in the order described.

The specific command step dictionary objects contain the following keys:

* instructions - (excludes all other keys) A string appended to the post automation instruction set printed to the user
* command - The string to execute within the shell
* must_work - (Required if "command" key exists) True or False, signifying the reaction of the verification script to any non-zero exit status from the command (True will exit immediately, while False will allow processing to continue)
* cwd - (Optional and only used if "command" key exists) The path to cd into prior to the command being run.  This is a critical field, given that each command is executed within it's own context (i.e.: you can't have a "command" to cd into a folder, and then expect to be in that folder for the next command)

There are also 2 replacement strings that can be used in the instructions.conf file:

* ${commit-sh} - passed in via the -c command line option, meant to be the commit-sh being tested
* ${version} - passed in via the -v command line option, meand to be the version of the software being tested

These two replacement strings are useful in describing a generic testing process, and passing in the specific commitsh and version to be tested against.

Example:

```
[
    {
        "command":"rm -Rf /tmp/cloudstack", 
        "must_work":True
    },
    {
        "command":"rm -Rf ~/.m2", 
        "must_work":True
    },
    {
        "command":"mkdir /tmp/cloudstack", 
        "must_work":True
    },
    {
        "cwd":"/tmp/cloudstack",
        "command":"wget --no-check-certificate -q https://dist.apache.org/repos/dist/release/cloudstack/KEYS", 
        "must_work":True
    },
    {
        "instructions":"""
This is a post instruction
that has two lines"""
    }
]
```
