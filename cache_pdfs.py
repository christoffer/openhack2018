import os
import json
import requests
import urllib

RESULT_DOCUMENT_CODE = 'A08'

def download_document(url, target_path):
    print("Downloading missing PDF: %s -> %s" % (url, target_path))
    try:
        urllib.request.urlretrieve(url, target_path)
        return True
    except:
        return False

def download_and_cache_missing_pdfs(activities):
    for activity in activities:
        # Grab documents from the activity data
        activity_data = activity['iati-activity']
        document_links = activity_data.get('document-link', [])
        for document in document_links:
            if(document['format'] == 'application/pdf' and document['category']['code'] == RESULT_DOCUMENT_CODE):
                document_url = document['url']
                print(document_url)
                target_filename = document_url[document_url.rfind('/')+1:]
                target_dir = 'pdf_cache'
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                target_path = os.path.join("%s/%s" % (target_dir, target_filename))
                dead_target_path = "%s.404" % target_path
                if os.path.exists(target_path):
                    print("Skipping download (already exists)")
                    continue
                if os.path.exists(dead_target_path):
                    print("Skipping download (marked as dead link)")
                    continue
                if not download_document(document_url, target_path):
                    # Target PDF is a dead link, mark it to avoid trying to download it again
                    print("Dead url: %s" % document_url)
                    with open(dead_target_path, 'w') as fp:
                        fp.write('')

def main():
    with open('all_sedi_activites_api_call.json') as f:
        data = json.load(f)
        activities = data['iati-activities']
    download_and_cache_missing_pdfs(activities)
    
if __name__ == "__main__":
    main()
