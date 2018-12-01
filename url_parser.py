import json
import os

urlData = {}

print(os.listdir())
with open('all_sedi_activites_api_call.json') as f:
	data = json.load(f)
	data = data['iati-activities']

counter = 0
with open('url.txt', "w") as text_file:
	for activity in data:	
		try:
			document = activity['iati-activity']['document-link']
			for urls in document:
				if(urls['format'] == 'application/pdf' and urls['category']['code'] == 'A08'):
					narrative = urls['title']['narrative']
					print(narrative)
					text_file.write("%s\n" % narrative)

					url = urls['url']
					print(url)
					text_file.write("%s\n" % url)

					urlData.update({counter : {'narrative' : narrative, 'url' : url}})
					counter += 1
		except:
			pass

with open('url.json', "w") as fp:
	json.dump(urlData, fp)

# json_data = json.dumps(urlData)
# print(json_data)

print(urlData)

# with open('json.txt', "w") as text_file:
	# text_file.write("%s\n" % json_data)

# json_file = json.dumps(file)
# with open("json.txt", "w") as file:
# 	file.write("%s" % json_file)

# print(json.dumps(data, indent=4))
# with open("sample3.txt", "w") as text_file:
# 	text_file.write("%s" % json.dumps(data, indent=4))
