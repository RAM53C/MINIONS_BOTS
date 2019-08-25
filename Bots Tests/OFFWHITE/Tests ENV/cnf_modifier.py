#!/usr/bin/python
import json
import ast
import sys, getopt

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def main(argv):
   print '================'
   print 'CNF Modifier CLI'
   print '================'
   cnfent = False
   try:
      opts, args = getopt.getopt(argv,"hc:",["config="])
   except getopt.GetoptError:
      print 'Usage: cnf_modifier.py -c <config>'
      sys.stdout.flush()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Usage: cnf_modifier.py -c <config>'
         sys.stdout.flush()
         sys.exit()
      elif opt in ("-c", "--config"):
         objconfig = arg
         cnfent = True
   if cnfent == True:
       print ('Config to be applied:')
       sys.stdout.flush()
       print ('Config ==> ' + str(objconfig))
       sys.stdout.flush()
       #It will replace ALL the config, be carefull
       print ('Replacing config...')
       sys.stdout.flush()
       config_file = open('config.json')
       loadcnf = ast.literal_eval(objconfig) #dict1
       keys = json.load(config_file) #dict2
       keys = ast.literal_eval(json.dumps(keys))
       old = keys
       new = merge_dicts(keys, loadcnf)
       #Write to file
       with open('config.json', 'w') as outfile:
           json.dump(new, outfile, indent=4, sort_keys=True)
       print ('Done!\n')
       sys.stdout.flush()
       #print ('Old config ==> ' + str(old) + "\n")
       #print ('New config ==> ' + str(new))


   else:
       print("CNF_NULL")
       print 'Usage: cnf_modifier.py -c <config>'

if __name__ == "__main__":
   main(sys.argv[1:])
