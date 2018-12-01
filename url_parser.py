import json
import os

print(os.listdir())
with open('all_sedi_activites_api_call.json') as f:
	data = json.load(f)
	data = data['iati-activities']

with open('url.txt', "w") as text_file:
	for activity in data:	
		try:
			document = activity['iati-activity']['document-link']
			for urls in document:
				if(urls['format'] == 'application/pdf' and urls['category']['code'] == 'A08'):
					url = urls['url']
					print(url)
					text_file.write("%s\n" % url)
					narrative = urls['title']['narrative']
					print(narrative)
					text_file.write("%s\n" % narrative)
		except:
			pass

# print(json.dumps(data, indent=4))
# with open("sample3.txt", "w") as text_file:
# 	text_file.write("%s" % json.dumps(data, indent=4))
