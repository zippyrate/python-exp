#!/usr/bin/python

import argparse, os, sys, subprocess

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
summary = args.summary

if args.path:
  path = args.path
else:
  path = '.'

if args.extension:
  extension = args.extension
else:
  extension = ''

expression = args.expression

process_args = ['find', path, '-type', filetype]

if extension:
  process_args.extend(['-name', '*.'+extension])

exec_args = ['-exec', 'grep', expression, '{}', ';']

grep_args = []

if summary:
  grep_args.append('-l')

if args.ignorecase:
  grep_args.append('-i')

if grep_args:
  exec_args[2:2] = grep_args

process_args.extend(exec_args)

if args.pf:
  process_args.append('-print')

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


