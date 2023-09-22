#!/usr/bin/python3.8
#
# Ed Silva
# July 25, 2022
#

import json
import requests
import csv
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--token', '-t', required=True, help="Authorization token for PUT request")
args = parser.parse_args()

if (len(args.token)):
	my_token = (args.token)
else:
	print("Invalid TOKEN")
	exit(1)

csv_file = "Sheet1.csv"
my_url = "https://mydomain.com/api/v1/group?"
my_token_url = my_url + "token=" + my_token

if not ( os.path.exists(csv_file) ):
	print (" ")
	print ("ERROR: Can't open CSV file: " + csv_file )
	print (" ")
	exit(1)

with open(csv_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	next(csv_reader)

	for new_group in csv_reader:
		
		new_cn_rd = ""
	
		for x in range(2,4):   
			if (new_group[x] != "" ):
				new_cn_rd = new_cn_rd + new_group[x] + ","

		new_cn_rd = (new_cn_rd.rstrip(',')).lstrip(',')
		my_group_api = my_url + "name=" + new_group[0]
		response = requests.get(my_group_api)

		if ( response.status_code == 200 ):
					
			my_group = response.json()
			my_data = (len(my_group['data']))

			if (my_data == 0 ):
				print (" ")
				print ("There are no GROUPs to list")
				print (" ")

			else:
				r_post = requests.post(my_token_url, data = {'name': my_group['data']['name'],'cn_rd': new_cn_rd})
					
				if ( r_post.status_code == 200 ):
					print ("Updated:", my_group['data']['name'], my_group['data']['cn_rd'],"->", new_cn_rd)
					
				else:
					print(r_post.status_code)
					print (r_post)
					print ("Failed update of: ", my_group['data']['name'], my_group['data']['cn_rd'],"->", new_cn_rd)
					
		else:
			print("GROUP:", new_group[0] + " not found " + "response.status_code:", response.status_code)
