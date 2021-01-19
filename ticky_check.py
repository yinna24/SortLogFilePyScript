#!/usr/bin/env python3

import operator
import re
#import sys
import csv

errors = {}
per_user = {}
line = []

with open("syslog.log") as files:
  file = files.readlines()
  for lines in file:
    line.append(lines.strip())

  for value in line:

    if re.search(r"ticky: INFO ([\w]*)", value):
      match = re.search(r"\(([a-zA-Z.]+)\)", value).group(1)
      
      if match in per_user:
        per_user[match][0] = per_user[match][0] + 1
      else:
        per_user.setdefault(match, []).append(1)
        per_user.setdefault(match, []).append(0)

    elif re.search(r"ticky: ERROR ([\w]*)", value):
      match = re.search(r"\(([a-zA-Z.]+)\)", value).group(1)
      err = re.search(r"ERROR ([\w ]*)", value).group(0)
      #print(err)

      if match in per_user:
        per_user[match][1] = per_user[match][1] + 1
      else:
        
        per_user.setdefault(match, [1]).append(1)

      if err in errors:
        errors[err] = errors[err] + 1
      else:
        errors[err] = 1

  #print(per_user)

  errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
  per_user = sorted(per_user.items(), key=operator.itemgetter(0))

  header = ("Username","INFO","ERROR")
  per_user.insert(0, header)

  for elements in per_user:
    for element in elements:
      if type(element) is list:
        converted = [str(val) for val in element]
        joined_string = "".join(converted)

        temp = list(elements)
        temp.pop(1)
        for elmnt in joined_string:
          temp.append(elmnt)
        new_elements = tuple(temp)
        per_user[per_user.index(elements)] = new_elements

  #print(per_user)

  header2 = ("ERROR","COUNT")
  errors.insert(0, header2)
  #print(errors)

  with open('user_statistics.csv', 'w') as user_stat:
    writer = csv.writer(user_stat)
    writer.writerows(per_user)

  with open('error_message.csv', 'w') as err_message:
    writer = csv.writer(err_message)
    writer.writerows(errors) 


