import time
import json
import pprint
import requests

entity_find_url = '<YOUR CAPURE URL>'
client_id = '<YOUR CLIENT ID>'
client_secret = '<YOUR CLIENT SECRET>'

current_record_id = 0
processed_records = 0
entity_type_name = 'user'
max_results = 1000
entity_array = []
result_file = open('entity_results.txt', 'wb+') # open results file to read and write in binary mode
parsed_api_response = {}
api_response = ''


post_params = {
	'client_id':client_id,
	'client_secret':client_secret,
	'type_name':entity_type_name,
	'timeout':"60",
	'sort_by':["id"],
	'max_results':max_results,
	'filter':'id>0'
}

all_results_retrieved = False
result_size = 0

while not all_results_retrieved:
	time.sleep(1) #wait 1 second between calls in order to avoid rate limits

	post_params['filter'] = 'id>'+ `current_record_id` #update filter to return records with id greater than last processed record

	api_response = requests.post(entity_find_url, data=post_params) #make POST to entity api

	parsed_api_response = json.loads(api_response.text) #transform response into python object

	if parsed_api_response['stat'] != "ok": #check for api errors, print information if there is an error
		print "The last response could not be processed. Please try reducing your max_results parameter."
		print "You should restart the script from the last processed record by setting the following variables to these values:"
		print "current_record_id: " + `current_record_id`
		print "processed_records: " + `processed_records`
		all_results_retrieved = True #exit script
	else:
		result_size = len(parsed_api_response['results']) # update the results retrieved from the last call
		processed_records += result_size # update the total records processed so far
		if result_size > 0: # check that records were actually returned
			for i in range(result_size): # for each record, write it's JSON to a line of the output file
				result_file.write(json.dumps(parsed_api_response['results'][i],sort_keys=True,separators=(',', ':')) + '\n')
				
			current_record_id = parsed_api_response['results'][-1]['id'] # update the current record id to match the last id proccessed
			
			print "Records processed so far: " + `processed_records` # print out information about the last api call
			print "Last ID processed: " + `current_record_id`
			print "------------------"
		if result_size != max_results: # check if we are done
			all_results_retrieved = True

result_file.close()
print "Total records processed:" + `processed_records` 

	