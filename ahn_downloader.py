import urllib.request
import os.path

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




class AhnDownloader():

    def __init__(self, map_sheet, resolution='5', dem_type='dtm'):
        self.map_sheet = map_sheet.upper()
        self.resolution = resolution # '5' or '05'
        self.dem_type = dem_type.lower()


    def get_url(self):
        type_code = _TYPE_CODES[self.dem_type]
        if self.dem_type == 'laz':
            sub_dir = 'laz'
            fn = f'{type_code}_{self.map_sheet}.LAZ'
        else:
            sub_dir = f'{self.resolution}m_{self.dem_type}'
            fn = f'{type_code}{self.resolution}_{self.map_sheet}.ZIP'

        result = _BASE_URL.format(sub_dir, fn)
        return (result, fn)


    def download(self, output_dir):
        url, fn = self.get_url()
        #fn = 'kaas.zip'
        output_fn = os.path.join(output_dir, fn)
        print(output_fn)
        response = urllib.request.urlopen(url)
        data = response.read() # a `bytes` object
        with open(output_fn, 'wb') as output_file:
            output_file.write(data)




if __name__ == '__main__':
    ad = AhnDownloader('45cn2', resolution=5)
    print(ad.get_url())
    ad.download('/home/raymond/tmp')
