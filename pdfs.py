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
    except IOError:
        return False

def get_pdfs_for_activity(activity):
    # Grab documents from the activity data
    activity_data = activity['iati-activity']
    document_links = activity_data.get('document-link', [])
    if not isinstance(document_links, list):
        document_links = [document_links]
    pdf_paths = []
    for document_link in document_links:
        is_pdf = document_link.get('format') == 'application/pdf'
        document_categories = document_link.get('category', [])
        if not isinstance(document_categories, list):
            document_categories = [document_categories]
        document_category_codes = map(lambda x: x['code'], document_categories)
        is_result_document = RESULT_DOCUMENT_CODE in document_category_codes
        if is_pdf and is_result_document:
            document_url = document_link['url']
            print(document_url)
            target_filename = document_url[document_url.rfind('/')+1:]
            target_dir = 'pdf_cache'
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            target_path = os.path.join("%s/%s" % (target_dir, target_filename))
            dead_target_path = "%s.404" % target_path
            if os.path.exists(target_path):
                print("Skipping download (already exists)")
                pdf_paths.append(target_path)
                continue
            if os.path.exists(dead_target_path):
                print("Skipping download (marked as dead link)")
                continue
            if not download_document(document_url, target_path):
                # Target PDF is a dead link, mark it to avoid trying to download it again
                print("Dead url: %s" % document_url)
                with open(dead_target_path, 'w') as fp:
                    fp.write('')
            else:
                pdf_paths.append(target_path)
    return pdf_paths


def get_filtered_activities(activities):
    STATUS_RESULT_CODE_COMPLETION = "3"
    STATUS_RESULT_CODE_POST_COMPLETION = "4"
    def should_use(activity):
        status = activity['iati-activity']['activity-status']
        return status.get('code') in [STATUS_RESULT_CODE_COMPLETION, STATUS_RESULT_CODE_POST_COMPLETION]
    return [activity for activity in activities if should_use(activity)]


def main():
    with open('all_sedi_activites_api_call.json') as f:
        data = json.load(f)
        activities = data['iati-activities']
    activities_to_use = get_filtered_activities(activities)
    print(len(activities_to_use))
    for activity in activities_to_use:
        pdfs = get_pdfs_for_activity(activity)
        if len(pdfs) > 0:
            print(json.dumps(activity, indent=4), pdfs)

if __name__ == "__main__":
    main()
