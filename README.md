# Resi  
  
## Chosen case: Sida Open Aid Visualisation Challenge  
  
## The solution: 
Categorize PDF documents with one-word tags and display the number of projects devoted to different causes via country-specific, weighted wordclouds.  
  
## Applied open source licenses:    
- libnabo (no license)  
- ocrmypdf (GNU general public license)  
- coreNLP (GNU general public license)  
- Swedish Python Routines (GNU general public license)  

  
## Getting started with your development-environment: 
```
pip install virtualenv
virtualenv venv
osource venv/bin/activate (or venv/Scripts/activate.bat if on Windows)
```
  
## Services used:  
- API calls from d-portal.org for SIDA's activities  
- Jupyter Lab and Jupyter Notebook (running scripts online)  
- ocrmypdf (running OCR on PDFs)  
- coreNLP (language processing for English documents)  
- Swedish Python Routines (language processing for Swedish documents)  
- libnado (running k-nearest neighbor algorithm)  
  
## Steps to carry out solution:  
1) Get IATI-identifiers of activities with known recipient country from d-portal.org  
2) Make API calls to get JSON file containing details tied with the activity  
3) Filter for completed activities using the activity status code  
4) Obtain and filter url to PDF results documents tied to the activities using the document format and report format code  
5) Determine if the language of the document is English or Swedish  
6) Run NLP on the document to do word stemming and remove stop words  
7) Filter for pre-defined keywords    
8) Use the k-nearest neighbor algorithm to calculate the weight of keywords  
9) Create a JSON file tying a country to its weighted key words  
10) Fetch JSON file on webpage to display results on webpage  
  
## Languages used:    
- Python3  
- Bash ShellScript
- HTML
- CSS
- JavaScript
  
## Team members:  
- Christoffer Klang
- Eric Kuan  
- Mikael Zwahlen  
- Sharon Yeo    
