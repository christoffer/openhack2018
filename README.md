Team name: Resi  
  
Chosen case  
  
The solution (One sentence only)  
  
Applied open source license    
- libnabo (no license)  
- ocrmypdf (GNU general public license)  
- coreNLP (GNU general public license)  
- Swedish Python Routines (GNU general public license)  

  
Getting started with your development-environment 
```
pip install virtualenv
virtualenv venv
osource venv/bin/activate (or venv/Scripts/activate.bat if on Windows)
```
  
Services used:  
- API calls from d-portal.org for SIDA's activities  
- Jupyter Lab and Jupyter Notebook (running scripts online)  
- ocrmypdf (running OCR on PDFs)  
- coreNLP (language processing for English documents)  
- Swedish Python Routines (language processing for Swedish documents)  
- libnado (running k-nearest neighbor algorithm)  
  
Steps to carry out solution:  
1) Get iata-identifiers of activities with known recipient country  
2) Make API calls to get JSON file containing details tied with the activity  
3) Filter for completed activities using the activity status code  
4) Get and filter url to PDF results documents tied to the activities using the document format and report format code  
5) Determine the language of the document  
6) Run NLP on the document to do word stemming and remove stop words  
7) Use the k-nearest neighbor algorithm to calculate the weight of key words  
8) Create a JSON file tying a country to its weighted key words  
9) Fetch JSON file on webpage to display results on webpage  
  
Languages used    
- Python3  
- Bash ShellScript
- HTML
- CSS
- JavaScript
  
Team members: Christoffer Klang, Mikael Zwahlen, Eric Kuan, Sharon Yeo    
