import urllib.request
import os.path
import ssl

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

class AhnDownloader:

    def __init__(self, map_sheet, resolution='5', dem_type='dtm', ssl_check=True):
        self.map_sheet = map_sheet.upper()
        self.resolution = resolution # '5' or '05'
        self.dem_type = dem_type.lower()
        self.ssl_check = ssl_check


    def create_url(self):
        type_code = _TYPE_CODES[self.dem_type]
        if self.dem_type == 'laz':
            sub_dir = 'laz'
            fn = f'{type_code}_{self.map_sheet}.LAZ'
        else:
            sub_dir = f'{self.resolution}m_{self.dem_type}'
            if self.resolution == '5':
                resolution7 = '5'
            else:
                resolution7 = ''
            fn = f'{type_code}{resolution7}_{self.map_sheet}.ZIP'

        result = _BASE_URL.format(sub_dir, fn)
        return (result, fn)


    def download(self, output_dir, ssl_check=True):
        url, fn = self.create_url()
        output_fn = os.path.join(output_dir, fn)
        print(output_fn)
        if self.already_downloaded(output_fn):
            print(f'  already downloaded file')
            return
        response = self.get_response(url)
        data = response.read() # a `bytes` object
        with open(output_fn, 'wb') as output_file:
            output_file.write(data)


    def get_response(self, url):
        if self.ssl_check:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(url, context=ctx)
        else:
            response = urllib.request.urlopen(url)
        return response


    def get_remote_file_size(self):
        url, fn = self.create_url()
        site = self.get_response(url)
        return site.length


    def get_local_file_size(self, output_fn):
        if os.path.isfile(output_fn):
            return os.path.getsize(output_fn)
        else:
            return None


    def already_downloaded(self, output_fn):
        remote_size = self.get_remote_file_size()
        local_size = self.get_local_file_size(output_fn)
        print(f'  remote size: {remote_size}, local_size: {local_size}')
        return remote_size == local_size




if __name__ == '__main__':
    ad = AhnDownloader('45cn1', resolution='5')
    print(ad.create_url())
    ad.download('/home/raymond/tmp/ahn3')
