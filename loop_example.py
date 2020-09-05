import csv

from ahn_downloader import AhnDownloader


# Example script for downloading all ahn3 files
# based on the bladindex csv.



bladindex_fn = 'bladindex_ahn3.csv'

counter = 0

with open(bladindex_fn, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    total = sum(1 for row in csv_reader)

with open(bladindex_fn, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for rec in csv_reader:
        counter += 1
        bladnr = rec['bladnr']
        print(f'{bladnr} ({counter}/{total})')
        if counter > 1300:
            ad = AhnDownloader(bladnr, resolution='5', dem_type='dsm')
            ad.download('/home/raymond/data/ahn3')
            if counter > 5000:
                break
