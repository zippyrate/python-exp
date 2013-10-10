#!/usr/bin/python

import argparse, os, sys, subprocess, re

patient_id_element_name='Patient\'s Name'

parser = argparse.ArgumentParser() 

parser.add_argument("-p", "--preview", help="preview", action="store_true")
parser.add_argument("basepath", help="base directory path")

args = parser.parse_args()

preview = args.preview
basepath = args.basepath

series_find_args = ['find', basepath, '-type', 'd', '-mindepth', '1', '-maxdepth', '1']

try:
  series_dirs = subprocess.check_output(series_find_args)

  for series_dir in series_dirs.split('\n'):

    # Porcess directories directly under the base directory (which should contain DICOM series)
    if series_dir:
      series_id = os.path.basename(series_dir).replace('_', '.') # ePAD converts . to _ in file names

      # Look for DICOM header files in each directory
      header_file_find_args = ['find', series_dir, '-type', 'f', '-name', '*.tag']
      header_files = subprocess.check_output(header_file_find_args)

      # We found at least one DICOM header file
      if header_files:
        header_file_path = header_files.split('\n')[0] # Pick the first (patient ID will be same in all files)
        if header_file_path:
          header_file_name = os.path.basename(header_file_path)

          # Find the line containing the patient ID DICOM element. TODO replace with grep and no error code on no match
          id_grep_args = ['find', '.', '-name', header_file_name, '-exec', 'grep', patient_id_element_name, '{}', ';']
          patient_id_elements = subprocess.check_output(id_grep_args)
      
          if patient_id_elements:
            patient_id_element = patient_id_elements.split('\n')[0] # Should only be one
            m = re.match('.+\[(?P<pid>.+)\].+', patient_id_element)
            if m:
              raw_pid = m.group('pid')
              if raw_pid:
                pid = re.sub('[\^ ]', '_', raw_pid)
                print pid.ljust(30), series_id
              else:
                print 'Warning: patient ID value missing in DICOM element ', patient_id_element, ' in header file', header_file_path
            else:
              print 'Warning: error extracting patient ID from DICOM element ', patient_id_element, ' in header file', header_file_path
          else:
            print 'Warning: did not find a patient ID DICOM element in tag file', header_file_path
      else:
        print "Warning: no DICOM header file found for series", series


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


