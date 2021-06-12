#!/usr/bin/env python3
import os
from datetime import datetime

# Function to start the parser script and update data every week
def update_week():

	# Check the number of files in the folder for a week and run the script
	listdir_data = os.listdir('data')
	if len(listdir_data) >= 30:

		# We get the current date
		date_now = datetime.now()

		# Get a list of all files in the folder
		for filename in listdir_data:
			if filename[4:5] == '2':

				# Get the date from the file name
				date_filename = datetime.strptime(filename[7:17], "%Y-%m-%d")

				# Find the difference in numbers
				datetime_delta = date_now - date_filename
				datetime_delta = str(datetime_delta)

				# Delete the file that is more than a week
				if int(datetime_delta[:2]) >= 7:
					os.remove(os.path.join(os.getcwd(), os.path.abspath('data'), filename))
					
			else:
				date_filename = datetime.strptime(filename[6:16], "%Y-%m-%d")
				datetime_delta = date_now - date_filename
				datetime_delta = str(datetime_delta)
				if int(datetime_delta[:2]) >= 7:
					os.remove(os.path.join(os.getcwd(), os.path.abspath('data'), filename))

	os.system('python3 cgo_parse.py')

# Function to start the parser script and update data every month
def update_month():
	
	# Save the current date
	date_now = datetime.now().date()
	month_now = date_now.strftime('%m')

	# Delete obsolete data (more than a month)
	listdir_file = os.listdir('data')
	if listdir_file != []:
		for filename in listdir_file:
			if filename[4:5] == '2':
				if filename[12:14] != month_now:
					os.remove(os.path.join(os.getcwd(), os.path.abspath('data'), filename))
			else:
				if filename[11:13] != month_now:
					os.remove(os.path.join(os.getcwd(), os.path.abspath('data'), filename))
					
	os.system('python3 cgo_parse.py')

# Function to start the parser script and update data every day
def update_day():
	
	# Delete obsolete data (all from folder)
	listdir_file = os.listdir('data')
	if listdir_file != []:
		for filename in listdir_file:
			os.remove(os.path.join(os.getcwd(), os.path.abspath('data'), filename))

	os.system('python3 cgo_parse.py')

update_month()
#update_week()
#update_day()
