# Token distributor
Self service script which helps you disctribute tokens from a newly deployed contract to addresses, specified in CSV file.

Make sure you have your CSV file of the form provided in sample file.csv

Clone repository

`git clone https://github.com/phDooY/pyweb3.git`

Move to directory of tonek distributor script

`cd pyweb3/token_distributor`

Install requirements

`sudo pip install -r requirements.txt`

Start script and provide additional info

`python token_distributor.py`

When script finishes, a \<your_file\>_out.csv will be generated, with a new column "tx", which will help you monitor sendout transaction status.
