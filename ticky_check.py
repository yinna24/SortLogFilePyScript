#!/usr/bin/env python3

#import modules
import operator
import re
import csv

errors = {}
per_user = {}
line = []

with open("syslog.log") as files:
  file = files.readlines()
  for lines in file:
    line.append(lines.strip())

  for value in line:
    #use regular expressions to search for INFO messages
    if re.search(r"ticky: INFO ([\w]*)", value):
      match = re.search(r"\(([a-zA-Z.]+)\)", value).group(1) #get user name
      
      #if user already exist, increase the Info message value by 1
      if match in per_user:
        per_user[match][0] = per_user[match][0] + 1 #dictionary key with two values
      else:
        per_user.setdefault(match, []).append(1)
        per_user.setdefault(match, []).append(0)

    #use regular expression to search for ERROR messages
    elif re.search(r"ticky: ERROR ([\w]*)", value):
      match = re.search(r"\(([a-zA-Z.]+)\)", value).group(1) #get user name
      err = re.search(r"ERROR ([\w ]*)", value).group(0)
      #print(err)
      
      #if user exists add one to the error message value
      if match in per_user:
        per_user[match][1] = per_user[match][1] + 1
      else:
        per_user.setdefault(match, [1]).append(1)
        
      #save the error message and increase it's count by one
      if err in errors:
        errors[err] = errors[err] + 1
      else:
        errors[err] = 1

  #print(per_user)
 
  #sort the error items values from most to least
  errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
  #sort the per_user items keys in alphabetical order
  per_user = sorted(per_user.items(), key=operator.itemgetter(0))

  #insert a header to the 0 index of the new list of tuples
  header = ("Username","INFO","ERROR")
  per_user.insert(0, header)

  for elements in per_user:
    for element in elements:
      #convert the numbers in the lists in the tuples to a string
      if type(element) is list:
        converted = [str(val) for val in element]
        joined_string = "".join(converted)
        
        #since a tuple is immutable, it is converted to a list, appended and converted back to a tuple
        temp = list(elements)
        temp.pop(1) #get rid of the int value
        for elmnt in joined_string:
          temp.append(elmnt) #append the string value
        new_elements = tuple(temp)
        per_user[per_user.index(elements)] = new_elements

  #print(per_user)

  header2 = ("ERROR","COUNT")
  errors.insert(0, header2)
  #print(errors)

  #write the contents of per_user to a csv file
  with open('user_statistics.csv', 'w') as user_stat:
    writer = csv.writer(user_stat)
    writer.writerows(per_user)

  #write the contents of errors to a csv file
  with open('error_message.csv', 'w') as err_message:
    writer = csv.writer(err_message)
    writer.writerows(errors) 


