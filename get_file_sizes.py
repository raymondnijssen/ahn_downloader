import csv

from ahn_downloader import AhnDownloader


# Example script for downloading all ahn3 files
# based on the bladindex csv.



bladindex_fn = 'bladindex_ahn3.csv'
output_csv_fn = 'bladindex_metadata.csv'

counter = 0

bladnr_list = []
with open(bladindex_fn, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for in_rec in csv_reader:
        bladnr = in_rec['bladnr']
        bladnr_list.append(in_rec['bladnr'])

bladnr_list.sort()
total = len(bladnr_list)

with open(output_csv_fn, 'w') as output_csv_file:
    csv_writer = csv.DictWriter(output_csv_file, ['bladnr', 'dsm_5_size', 'dtm_5_size', 'dsm_05_size', 'dtm_05_size', 'laz_size'])
    csv_writer.writeheader()
    for bladnr in bladnr_list:
        counter += 1

        out_rec = {}
        #bladnr
        print(f'{bladnr} ({counter}/{total})')
        out_rec['bladnr'] = bladnr

        ad = AhnDownloader(bladnr)

        #05, dsm
        ad.resolution = '5'
        ad.dem_type = 'dsm'
        out_rec['dsm_5_size'] = ad.get_remote_file_size(use_cache=False)

        #05, dtm
        ad.resolution = '5'
        ad.dem_type = 'dtm'
        out_rec['dtm_5_size'] = ad.get_remote_file_size(use_cache=False)

        #05, dsm
        ad.resolution = '05'
        ad.dem_type = 'dsm'
        out_rec['dsm_05_size'] = ad.get_remote_file_size(use_cache=False)

        #05, dtm
        ad.resolution = '05'
        ad.dem_type = 'dtm'
        out_rec['dtm_05_size'] = ad.get_remote_file_size(use_cache=False)

        #laz
        ad.dem_type = 'laz'
        out_rec['laz_size'] = ad.get_remote_file_size(use_cache=False)

        csv_writer.writerow(out_rec)

        if counter >= 5000:
            break
