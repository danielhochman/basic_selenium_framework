#!/usr/bin/python

import sys
import re
import os
import glob
import tokenize
from collections import defaultdict

def main():
    
    outfile = open('nosetests.csv', 'w+')
    
    outfile.write('File,Class,Method,Description,Steps,Assertions\n')
    
    for filename in glob.glob('test_*.py'): 
        with open(filename) as source:
            basename = '.'.join(os.path.splitext(filename)[:-1])
            tokens = tokenize.generate_tokens(source.readline)
            
            docs = defaultdict(
                lambda: defaultdict(
                    lambda: defaultdict(
                        lambda: defaultdict()
                    )
                )
            )
            
            for token in tokens:
                toktype, tokstr, _, _, tokparent = token
                
                if toktype == tokenize.NAME and tokstr == 'class':
                    classname = re.search('class\s+(\w+)\s*\(', tokparent).group(1)
                elif toktype == tokenize.NAME and tokstr == 'def':
                    funcname = re.search('def\s+(\w+)\s*\(', tokparent).group(1)
                    docs[basename][classname][funcname]['desc'] = ''
                    docs[basename][classname][funcname]['steps'] = []
                    docs[basename][classname][funcname]['asserts'] = []
                
                elif toktype == tokenize.STRING and tokstr.startswith('"""'):
                    docstring = ' '.join([ x.strip() for x in tokstr.split('\n')[1:-1] ])
                    m = re.search('[Dd]esc(?:ription)?:\s*(.+)\s*', docstring)
                    if m:
                        docs[basename][classname][funcname]['desc'] = '"%s"' % m.group(1)
                    
                elif toktype == tokenize.COMMENT:
                    comment = tokparent.strip().lstrip('#').strip()
                    if comment.startswith('s:') or comment.startswith('step:'):
                        docs[basename][classname][funcname]['steps'].append(
                            comment.replace('s:', '').replace('step:', '').strip()
                        )
                    elif comment.startswith('a:') or comment.startswith('assert:'):
                        docs[basename][classname][funcname]['asserts'].append(
                            comment.replace('a:', '').replace('assert:', '').strip()
                        )
            
            
            for basename, classes in docs.iteritems():
                for classname, funcs in classes.iteritems():
                    for funcname, artifacts in funcs.iteritems():
                        if funcname.startswith('test'):
                            if funcs.has_key('setup'):
                                steps = funcs['setup']['steps'] + artifacts['steps']
                            else:
                                steps = artifacts['steps']
                            
                            if funcs.has_key('teardown'):
                                steps += funcs['teardown']['steps']
                            
                            outfile.write(','.join((basename, classname, funcname)))
                            outfile.write(',%s' % artifacts['desc'])
                            outfile.write(',"')
                            outfile.write('\n'.join(numbered_list(steps)))
                            outfile.write('","')
                            outfile.write('\n'.join(numbered_list(artifacts['asserts'])))
                            outfile.write('"\n')

def numbered_list(list_of_things):
    for i in xrange(len(list_of_things)):
        list_of_things[i] = "%s. %s" % (i+1, list_of_things[i])
    return list_of_things

if __name__ == '__main__':
    main()
