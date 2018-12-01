import json
import requests
import urllib

with open('all_sedi_activites_api_call.json') as f:
    data = json.load(f)
    data = data['iati-activities']
    
for activity in data:
    try:
        document = activity['iati-activity']['document-link']
        for urls in document:
            if(urls['format'] == 'application/pdf' and urls['category']['code'] == 'A08'):
                url = urls['url']
                print(url)
                try:
                    doc = url[url.rfind('/')+1:]
                    path = 'pdf/'
                    path = path + doc
                    print(path)
                    urllib.request.urlretrieve(url, path)
#                     print("test")
                    
#                     response = requests.get(str(url))
#                     print("test")
#                     with open(doc, 'wb') as d:
#                         d.write(response.content)
                except:
                    pass
                    
    except:
        pass