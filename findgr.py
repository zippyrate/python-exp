#!/usr/bin/python

import argparse
import os
import sys
import subprocess

parser = argparse.ArgumentParser() 

parser.add_argument("-i", "--ignorecase", help="ignore case", action="store_true")
parser.add_argument("-t", "--type", help="type argument;f=file,d=directory", choices=['f','d'], default='f')
parser.add_argument("-s", "--summary", help="summary", action="store_true")
parser.add_argument("-p", "--path", help="path")
parser.add_argument("-e", "--extension", help="file extension")
parser.add_argument("-pf", help="print file name", action="store_true")
parser.add_argument("expression", help="expression")

args = parser.parse_args()

if args.ignorecase:
  print "Ignorecase"

filetype = args.type

print "Type =", filetype

summary = args.summary

print "Summary =", summary

if args.path:
  path = args.path
else
  path = '.'

print "Path =", path

if args.extension:
  extension = args.extension
  print "Extension =", extension
else
  extension = ''

expression = args.expression

print "Expression =", expression

if extension:
  file_name_arg = '*.'+extension
else:
  file_name_arg = '*'

process_args = ['find', path, '-type', filetype, '-name', file_name_arg]

exec_args = ['-exec', 'grep', expression, '{}', ';']

grep_args = []

if summary:
  grep_args.append('-l')

if args.ignorecase:
  grep_args.append('-i')

if not grep_args:
  exec_args[2:2] = grep_args

process_args.extend(exec_args)

if args.pf:
  process_args.append('-print')

print "Process arguments =", process_args

try:

  r = subprocess.check_output(process_args)

  print 'r: ', r
  print 'r.length: ', len(r)

except subprocess.CalledProcessError as e:
  print "Called process error: {0}".format(e.message)
except AttributeError as e:
  print "Attribute error: {0}".format(e.message)
except OSError as e:
  print "OS error({0}): {1}".format(e.errno, e.strerror)
except IOError as e:
  print "IO error({0}): {1}".format(e.errno, e.strerror)
except NameError as e:
  print "Name error: {0}".format(e.message)
except RuntimeError as e:
  print "Runtime error({0}): {1}".format(e.errno, e.strerror)
except:
  print "Unexpected error:", sys.exc_info()[0]


