#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is simply a library to wrap unittest's TextTestRunner and provide
several output formats that match those provided by mocha: https://mochajs.org/#reporters

Current available formats: list,dots,jsstream,json,progress,min,tap,spec

to use: import TestRunner from this file, pass in the desired format, and run your suite:
TestRunner(verbosity=2,format='json').run(suite)
"""

try:
    import unittest2 as unittest #python2.6
except ImportError:
    import unittest
import sys, os
import time
import json


class ExpectedFailure(Exception):
    pass


class Result(unittest.TestResult):
    """ Generic TestResult wrapper class
        to handle repetitive boilerplate things
        and create helper functions for fancy output
    """
    icon = {
        'check': '✓',
        'check_bold': '✔',
        'cross': '✖',
        'dot': '․',
        'bullet': '•',
        'dash': '▬',
    }
    color_names = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
    escape='\033[%sm'
    reset=escape % ("0",)

    def __init__(self,stream,descriptions,verbosity,count):
        super(Result,self).__init__(stream,descriptions,verbosity)
        self.stream=stream
        self.verbosity = verbosity
        self.descriptions = descriptions
        self.testCount=count
        self.failCount=0
        self.successes = []

        #determine whether the output stream can handle colors
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(self.stream, 'isatty') and self.stream.isatty()
        if not supported_platform or not is_a_tty:
            self.supports_color=False
        else:
            self.supports_color = True

    def stopTestRun(self,starttime,stoptime):
        super(Result,self).stopTestRun()
        #break and newline after dots
        self.write('\n\n')

        #display check only if we got an overall pass
        if self.wasSuccessful():
            self.write(self.icon['check_bold']+' ','green')
        else:
            self.write('  ')

        #number of passing tests
        self.write('%d passing ' % len(self.successes),'green')
        #print runtime
        self.write('(%.3fs)\n'% (stoptime-starttime,),'lightblack')

        #print all other test statuses
        if len(self.skipped):
            self.write("  %d pending\n"%len(self.skipped),'blue')
        if len(self.errors):
            self.write(self.icon['cross']+' %d error%s\n'% (
                       len(self.errors),
                       's' if len(self.errors) > 1 else ''
            ),'magenta')
        if len(self.failures):
            self.write(self.icon['cross']+' %d failing\n' % len(self.failures), 'red')

        #going to print some error traces, so make some room
        if not self.wasSuccessful():
            self.write("\n")

        errlist = {}
        for e in self.errors:
            e[0].type='error'
            errlist[e[0].failNum] = e
        for f in self.failures:
            f[0].type='failure'
            errlist[f[0].failNum] = f

        for x in sorted(map(int,errlist.keys())):
            self.writeTrace(errlist[x][0],errlist[x][1],x,type=errlist[x][0].type)

        #put next prompt on newline without extra spaces
        self.write("\n")


    def addSuccess(self,test):
        super(Result,self).addSuccess(test)
        self.successes.append(test)

    def addFailure(self,test,err):
        super(Result,self).addFailure(test,err)
        self.failCount +=1
        test.failNum = self.failCount

    def addError(self,test,err):
        super(Result,self).addError(test,err)
        self.failCount +=1
        test.failNum = self.failCount

    def addExpectedFailure(self,test,err):
        super(Result,self).addExpectedFailure(test,err)
        self.addSuccess(test)

    def addUnexpectedSuccess(self,test):
        super(Result,self).addUnexpectedSuccess(test)
        self.addFailure(test,(ExpectedFailure,ExpectedFailure("Test expected Failure, but passed"),None))

    def colorize(self,text,color):
        """ supports color names: black,red,green,yellow,blue,magenta,cyan,white
            and lightblack, lightred, etc.. for bold colors
        """
        if not self.supports_color:
            return text

        c = color.lower()
        if c[:5] == 'light':
            escaped_color = self.escape % (str(self.color_names.index(c[5:])+30)+";1",)
        else:
            escaped_color = self.escape % (str(self.color_names.index(c)+30),)
        return "%s%s%s" % (escaped_color,text,self.reset)

    def write(self,text,color=None):
        if color:
            text = self.colorize(text,color)
        self.stream.write(text)
        self.stream.flush()

    def writeTrace(self,test,trace,n,type='failure'):
        if type == 'error':
            color='magenta'
        else:
            color='red'

        testname = test.id().split('.')
        desc = test.shortDescription()
        if desc is None:
            desc = ''

        try:
            self.write("  %d) %s.%s.%s %s\n" % (
                n,
                testname[-3],
                testname[-2],
                testname[-1],
                desc,
            ),'white')
        except:
            self.write("  %d) %s %s\n" % (
                n,
                ".".join(testname),
                desc,
            ),'white')
        #self.write(str(f[0]),'white')

        trace = self.reindent(trace,5)
        trace = trace.split('\n')
        trace.pop() #removes last newline
        assertion = trace.pop()
        if len(trace):
            trace.pop(0) # remove "Traceback" line
        trace = "\n".join(trace)
        self.write(assertion+"\n",color)
        self.write(trace+"\n")

    def testToJSON(self,test,**kwargs):
        o = {
            'test':test.id(),
            'description':test.shortDescription()
        }
        if 'error' in kwargs and type(kwargs['error']) is tuple:
            kwargs['error'] = "%s: %s" % (
                kwargs['error'][0].__name__,
                kwargs['error'][1]
            )
        o.update(kwargs)
        if 'string' in kwargs and kwargs['string'] == False:
            return o
        return json.dumps(o)


    def reindent(self,str,n=2):
        return "\n".join(
            map(lambda x: " "*n+x,
                str.split("\n"))
        )[:-1]

    def up(self,n=1):
        if self.supports_color:
            self.stream.write('\033[%dA'%n)
    def down(self,n=1):
        if self.supports_color:
            self.stream.write('\033[%dB'%n)
    def left(self,n=1):
        if self.supports_color:
            self.stream.write('\033[%dD'%n)
    def right(self,n=1):
        if self.supports_color:
            self.stream.write('\033[%dC'%n)
    def rewind(self):
        if self.supports_color:
            self.stream.write('\033[1K')
            self.stream.write('\033[900D')#this assumes 900 char max length line






class Spec(Result):
    def startTestRun(self):
        super(Spec,self).startTestRun()
        self.tests_seen = {}

    def startTest(self,test):
        super(Spec,self).startTest(test)
        test_path = test.id().split('.')
        if test_path[-3] not in self.tests_seen:
            self.write("  %s\n"%test_path[-3],'white')
            self.tests_seen[test_path[-3]] = []
        if test_path[-2] not in self.tests_seen[test_path[-3]]:
            self.write("    %s\n"%test_path[-2],'white')
            self.tests_seen[test_path[-3]].append(test_path[-2])

    def addSuccess(self,test):
        super(Spec,self).addSuccess(test)
        self.write("      %s"%self.icon['check'],'green')
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write(" %s\n"%desc,'lightblack')

    def addSkip(self,test,reason):
        super(Spec,self).addSkip(test,reason)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write("      - %s (%s)\n"%(desc,reason),'blue')

    def addError(self,test,err):
        super(Spec,self).addError(test,err)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write("      %d) %s\n"%(test.failNum,desc),'magenta')

    def addFailure(self,test,err):
        super(Spec,self).addFailure(test,err)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write("      %d) %s\n"%(test.failNum,desc),'red')


class TAP(Result):
    def startTestRun(self):
        super(TAP,self).startTestRun()
        self.testCounter=1
        self.write('1..%d\n'%self.testCount)

    def stopTest(self,test):
        super(TAP,self).stopTest(test)
        self.testCounter +=1

    def stopTestRun(self,starttime,stoptime):
        pass

    def addSuccess(self,test):
        super(TAP,self).addSuccess(test)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write('ok %d - %s %s\n' % (
            self.testCounter,
            test.id().split('.')[-2],
            desc
        ))
    def addSkip(self,test,reason):
        super(TAP,self).addSkip(test,reason)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write('ok %d - %s %s # SKIP %s\n' % (
            self.testCounter,
            test.id().split('.')[-2],
            desc,
            reason
        ))
    def addError(self,test,err):
        super(TAP,self).addError(test,err)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write('not ok %d - %s %s\n' % (
            self.testCounter,
            test.id().split('.')[-2],
            desc
        ))        
    def addFailure(self,test,err):
        super(TAP,self).addFailure(test,err)
        desc = test.shortDescription()
        if desc is None:
            desc = test.id().split('.')[-1]
        self.write('not ok %d - %s %s\n' % (
            self.testCounter,
            test.id().split('.')[-2],
            desc
        ))    


class List(Result):
    def getTestLine(self,test):
        desc = test.shortDescription()
        if desc is None:
            desc = ''
        try:
            return '%s.%s %s' % (
                test.id().split('.')[-3],
                test.id().split('.')[-2],
                desc
            )
        except Exception as e:
            return '%s %s' % (test.id(),desc)

    def startTestRun(self):
        super(List,self).startTestRun()
        self.write("\n")

    def addSuccess(self,test):
        super(List,self).addSuccess(test)
        self.write("  %s "% (self.icon['check'],),'green')
        self.write("%s\n" % (self.getTestLine(test)),'lightblack')

    def addSkip(self,test,reason):
        super(List,self).addSkip(test,reason)
        self.write("  - %s (%s)\n" % (
            self.getTestLine(test),
            reason
        ), 'blue')

    def addFailure(self,test,err):
        super(List,self).addFailure(test,err)
        self.write("  %d) %s\n" % (
            test.failNum,
            self.getTestLine(test)
        ), 'red')

    def addError(self,test,err):
        super(List,self).addError(test,err)
        self.write("  %d) %s\n" % (
            test.failNum,
            self.getTestLine(test)
        ), 'magenta')

class Progress(Result):
    def startTestRun(self):
        super(Progress,self).startTestRun()
        #self.testsDone=0
        if self.testCount < 50:
            self.progress_bars = int(round(50.0/self.testCount))*self.testCount
        else:
            self.progress_bars = int(self.testCount/int(round(self.testCount/50.0)))
            self.progress_interval=int(self.testCount/self.progress_bars)
            self.progress_count=1
        self.write('  ['+self.icon['dot']*self.progress_bars+']\n\n')
        self.up(2)
        self.right(3)


    def stopTest(self,test):
        super(Progress,self).stopTest(test)
        #self.testsDone += 1
        if self.testCount < self.progress_bars:
            n = int(round(self.progress_bars/self.testCount*1.0))
        else:
            if self.progress_count == self.progress_interval:
                self.progress_count=1
                n=1
            else:
                n=0
                self.progress_count +=1
        self.write(self.icon['dash']*n)

class JSON(Result):
    def stopTestRun(self,starttime,stoptime):
        o = {
            'stats': {
                'tests': self.testsRun,
                'passed': len(self.successes),
                'errors': len(self.errors),
                'failures': len(self.failures),
                'skipped': len(self.skipped),
                'successful': self.wasSuccessful(),
                'start': time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime(starttime)),
                'end': time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime(stoptime)),
                'duration': stoptime-starttime
            },
            'passes': list(map(lambda x: self.testToJSON(x,string=False), self.successes)),
            'failures': list(map(lambda x: self.testToJSON(x[0],error=x[1],string=False),self.failures)),
            'skipped': list(map(lambda x: self.testToJSON(x[0],reason=x[1],string=False), self.skipped)),
            'errors': list(map(lambda x: self.testToJSON(x[0],error=x[1],string=False), self.errors)),
        }
        self.write(json.dumps(o)+"\n")


class JSONStream(Result):
    def startTestRun(self):
        super(JSONStream,self).startTestRun()
        self.write('["start",{"total": %d}]\n' % self.testCount)

    def stopTestRun(self,starttime,stoptime):
        o = {
            'tests': self.testsRun,
            'passed': len(self.successes),
            'errors': len(self.errors),
            'failures': len(self.failures),
            'skipped': len(self.skipped),
            'successful': self.wasSuccessful(),
            'start': time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime(starttime)),
            'end': time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime(stoptime)),
            'duration': stoptime-starttime
        }
        self.write('["end",%s]\n'%json.dumps(o))

    def addSkip(self,test,reason):
        super(JSONStream,self).addSkip(test,reason)
        self.write('["skip",%s]\n'%self.testToJSON(test,reason=reason))

    def addFailure(self,test,err):
        super(JSONStream,self).addFailure(test,err)
        self.write('["fail",%s]\n'%self.testToJSON(test,error=err))

    def addError(self,test,err):
        super(JSONStream,self).addError(test,err)
        self.write('["error",%s]\n'%self.testToJSON(test,error=err))

    def addSuccess(self,test):
        super(JSONStream,self).addSuccess(test)
        self.write('["pass",%s]\n'%self.testToJSON(test))


class Min(Result):
    pass

class Dots(Result):
    def startTestRun(self):
        super(Dots,self).startTestRun()
        self.write("\n  ")

    def startTest(self,test):
        super(Dots,self).startTest(test)
        self.write(self.icon['dot'],'lightblack')

    def addSkip(self,test,reason):
        super(Dots,self).addSkip(test,reason)
        self.left()
        self.write(self.icon['dot'],'blue')

    def addFailure(self,test,err):
        super(Dots,self).addFailure(test,err)
        self.left()
        self.write(self.icon['dot'],'red')

    def addError(self,test,err):
        super(Dots,self).addError(test,err)
        self.left()
        self.write(self.icon['dot'],'magenta')

    def addSuccess(self,test):
        super(Dots,self).addSuccess(test)
        self.left()
        self.stream.write(self.icon['dot'])




#custom Runner just to select custom Result
class TestRunner(unittest.TextTestRunner):
    """ Main interface for unitstyle """

    #@todo change to **kwargs for future-proofing argument format
    def __init__(self,stream=sys.stderr,descriptions=True,verbosity=1,
                     failfast=False,buffer=False,resultclass=None,format='dots'):
        super(TestRunner,self).__init__(stream,descriptions,verbosity,failfast,buffer,resultclass)
        self.format=format


    #not super'd to control the timing and printing at the end of a test run
    def run(self,test):
        #somewhat unnecessary. Call parent helper method that's just there
        #for easy overriding for us, which ends up calling resultclass anyway
        fmt = self.format.lower()
        if fmt == 'list': resulthandler = List
        elif fmt == 'dots': resulthandler = Dots
        elif fmt == 'jsstream': resulthandler = JSONStream
        elif fmt == 'json': resulthandler = JSON
        elif fmt == 'progress': resulthandler = Progress
        elif fmt == 'min': resulthandler = Min
        elif fmt == 'tap': resulthandler = TAP
        elif fmt == 'spec': resulthandler = Spec
        else: resulthandler = Dots
        result = resulthandler(self.stream,self.descriptions,self.verbosity,test.countTestCases())

        result.failfast=self.failfast
        result.buffer=self.buffer

        #register with unittest signaling for ctrl-C handling in result
        unittest.registerResult(result)

        if hasattr(result,'startTestRun'):
            result.startTestRun()
        starttime = time.time()
        try:
            test(result)
        finally:
            stoptime = time.time()
        if hasattr(result,'stopTestRun'):
            result.stopTestRun(starttime,stoptime)
        return result


