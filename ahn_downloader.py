import urllib.request, urllib.error
import os.path
import ssl
import csv

'''
example url's
https://download.pdok.nl/rws/ahn3/v1_0/05m_dsm/R_45CN2.ZIP
https://download.pdok.nl/rws/ahn3/v1_0/05m_dtm/M_45CN2.ZIP
https://download.pdok.nl/rws/ahn3/v1_0/5m_dsm/R5_45CN2.ZIP
https://download.pdok.nl/rws/ahn3/v1_0/5m_dtm/M5_45CN2.ZIP
https://download.pdok.nl/rws/ahn3/v1_0/laz/C_45CN2.LAZ
'''

_BASE_URL = 'https://download.pdok.nl/rws/ahn3/v1_0/{}/{}'
_TYPE_CODES = {'laz': 'C', 'dtm': 'M', 'dsm': 'R'}

_FILE_SIZE_CSV = 'bladindex_metadata.csv'
_FILE_SIZES = {}

class AhnDownloader:

    def __init__(self, map_sheet, resolution='5', dem_type='dtm', ssl_check=True):
        self.map_sheet = map_sheet.upper()
        self.resolution = resolution # '5' or '05'
        self.dem_type = dem_type.lower()
        self.ssl_check = ssl_check
        if len(_FILE_SIZES) == 0:
            self.load_file_sizes()

    def load_file_sizes(self):
        print('loading file sizes')
        with open(_FILE_SIZE_CSV) as file_size_csv:
            csv_reader = csv.DictReader(file_size_csv)
            for in_rec in csv_reader:
                bladnr = in_rec['bladnr'].upper()
                _FILE_SIZES[bladnr] = in_rec
        #print(_FILE_SIZES)


    def create_url(self):
        type_code = _TYPE_CODES[self.dem_type]
        if self.dem_type == 'laz':
            sub_dir = 'laz'
            fn = f'{type_code}_{self.map_sheet}.LAZ'
        else:
            sub_dir = f'{self.resolution}m_{self.dem_type}'
            if self.resolution == '5':
                resolution = '5'
            else:
                resolution = ''
            fn = f'{type_code}{resolution}_{self.map_sheet}.ZIP'

        result = _BASE_URL.format(sub_dir, fn)
        return (result, fn)


    def download(self, output_dir, ssl_check=True):
        url, fn = self.create_url()
        output_fn = os.path.join(output_dir, fn)
        print(f'{url} --> {output_fn}')
        if self.already_downloaded(output_fn):
            print(f'  already downloaded file')
            return
        response = self.get_response(url)
        if response is None:
            print('Bad response')
            return
        data = response.read() # a `bytes` object
        with open(output_fn, 'wb') as output_file:
            output_file.write(data)


    def get_response(self, url):
        if self.ssl_check:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(url, context=ctx)
                return response
            except:
                return None
        else:
            try:
                response = urllib.request.urlopen(url)
                return response
            except:
                return None


    def get_remote_file_size(self, use_cache=True):
        if use_cache:
            if self.dem_type == 'laz':
                field_name = 'laz_size'
            else:
                field_name = f'{self.dem_type}_{self.resolution}_size'
            if self.map_sheet in _FILE_SIZES:
                size = int(_FILE_SIZES[self.map_sheet][field_name])
                return size
        url, fn = self.create_url()
        response = self.get_response(url)
        if response is None:
            return -1
        else:
            return response.length


    def get_local_file_size(self, output_fn):
        if os.path.isfile(output_fn):
            return os.path.getsize(output_fn)
        else:
            return None


    def already_downloaded(self, output_fn):
        remote_size = self.get_remote_file_size()
        if remote_size == -1:
            return False

        local_size = self.get_local_file_size(output_fn)
        if local_size is None:
            return False

        print(f'  remote size: {remote_size}, local_size: {local_size}')
        return remote_size == local_size




if __name__ == '__main__':
    ad = AhnDownloader('45cn1', resolution='5')
    print(ad.create_url())
    ad.download('/home/raymond/tmp/ahn3')
    ad = AhnDownloader('01CZ2', resolution='5')
    ad.download('/home/raymond/tmp/ahn3')
