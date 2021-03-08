import scrapy
import json
from .generate_file import generate_path


class CollectionsSpider(scrapy.Spider):
    # Spider responsable for collection csv data 
    # by forms from page

    # spider`s name
    name = 'collections' 

    # A list of URLs where the spider will begin crawlling from
    start_urls = ['https://pathogen.watch/api/collection/summary?prefilter=all']

    def parse(self, response):
        # Default callback to process downloaded responses from
        # :param response response: return scrapped data from each URL
        
        # data variable receive page data 
        # from body HTML in str format.
        data = response.body
        
        # parse to JSON format
        parsed_json_data = json.loads(data)

        # loop responsable to pass for each collection page
        for collection in parsed_json_data['collections']:

            # URL variable receive each mountted collection URL
            url = self.mount_url(collection['token'])

            # Callback each processed collection
            # and return each scrapped collection
            yield scrapy.Request(
                url=url,
                callback=self.parse_collection
            )

    def mount_url(self, token):
        # mount each URL collection page
        # :param str token: receive collection identification
        # mounting each URL`s collection to be scrapped

        #return mounted URL`S collection
        return f'https://pathogen.watch/api/collection/{token}'

    def parse_collection(self, response):
        # Get source collection page to filter
        # :param response response: return scrapped data from collection page

        # data variable receive page data 
        # from body HTML in str format.
        data = response.body

        # parse to JSON format
        parsed_json_data = json.loads(data)

        # init ids array variable
        ids = []

        # init separator str variable
        separator = ','

        # loop responsable to pass for each id 
        # on genomes property and push to ids array
        for genome in parsed_json_data['genomes']:
            ids.append(genome['id'])
        
        # genome_ids variable receive amount of ids 
        # to pass by form submit
        genome_ids = separator.join(ids)

        # form_data variable receive mountted params in JSON format
        form_data = {
            'ids': genome_ids
        }

        # token variable receive token identification from page data
        token = parsed_json_data['token']

        # organism list
        organisms = [
            'sequi',
            'klepn',
            'ngonorrhoeae',
            'styphi',
            'rensm-rensm',
            'saureus',
            'zikv'
        ]

        # loop responsable for take each organism and token to correct collection`s URL
        for organism in organisms:

            # urls list variable
            urls = [
                f'https://pathogen.watch/download/collection/{token}/speciator?filename=pathogenwatch-{organism}-{token}-species-prediction.csv',
                f'https://pathogen.watch/download/collection/{token}/kleborate?filename=pathogenwatch-{organism}-{token}-kleborate.csv',
                f'https://pathogen.watch/download/collection/{token}/core-allele-distribution?filename=pathogenwatch-{organism}-{token}-core-allele-distribution.csv',
                f'https://pathogen.watch/download/collection/{token}/score-matrix?filename=pathogenwatch-{organism}-{token}-score-matrix.csv',
                f'https://pathogen.watch/download/collection/{token}/difference-matrix?filename=pathogenwatch-{organism}-{token}-difference-matrix.csv'
            ]

            # loop responsable to submit each data created by form_data variable
            # to correct collection`s URL 
            # and by pass token (collection identification) args & organism name
            for url in urls:
                yield scrapy.FormRequest(
                    url=url,
                    method='POST',
                    formdata=form_data,
                    callback=self.save_csv_file,
                    cb_kwargs=dict(token=token)
                )

    def save_csv_file(self, response, token):
        # method responsable for save csv file
        # and getting token
        # and mount directory`s name pattern
        # :param str token: collection`s identification

        # filename variable receive URL collection page
        # splitted by slash, question mark and equals
        # to get filename from URL
        filename = response.url.split('/')[-1].split('?')[-1].split('=')[-1]

        # split token to get separated year, name and identification
        formatted_token = token.split('-')
        
        # year variable receive last item from list
        year = formatted_token[-1]

        # ID variable receive first item from list and pass to str
        ID = formatted_token[0:1][0]

        # author variable receive second item from list
        author = formatted_token[1:2]

        # check if year variable has more than 4 characters
        if len(year) > 4:

            # author variable going to be all characters less last 4 characters
            author = year[:-4]

            # year variable going to be the last 4 characters
            year = year[-4:]

            # check if last 4 characters is int type
            try:
                year = int(year)

            # confirm that year is not an int type
            # concat last 4 year characters to author`s name
            # it is mounting correct author`s name
            # and define year like None
            except:
                # debug point
                # self.log(f'It is not year ==>>{year}')
                author = f'{author}{year}'
                year = None

        # check year type is str
        # if year is list get first item
        # and year variable receive correct type (str)
        if isinstance(year, list):
            year = year[0]

        # check author type is str
        # if author is list get first item
        # and author variable receive correct type (str)
        if isinstance(author, list):
            author = author[0]

        # debug point
        # self.log(f'DEBUG ===>>>>> YEAR = {year}')
        # self.log(f'DEBUG ===>>>>> ID = {ID}')
        # self.log(f'DEBUG ===>>>>> AUTHOR = {author}')

        # path variable receive generated path to save file
        path = generate_path(filename, ID, author, year)

        # debug point
        self.log(f'Saving on {path}')

        # open created file to write data
        with open(path, 'wb') as f:

            # write csv data on file
            f.write(response.body)
        
    
