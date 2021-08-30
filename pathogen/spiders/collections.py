from pymongo import collection
import scrapy
import json
from logging import debug
from ..common.save_csv_file import save_csv_file
from ..common.mount_url import mount_url
from ..common.organisms import organisms


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

        parsed_json_data['summary']['organismId']

        # loop responsable to pass for each collection page
        for collection in parsed_json_data['collections']:

        #     # URL variable receive each mountted collection URL
            url = mount_url(collection['token'])
            
            # Callback each processed collection
            # and return each scrapped collection
            yield scrapy.Request(
                url=url,
                callback=self.parse_collection
            )

    def parse_collection(self, response):
        # Get source collection page to filter
        # :param response response: return scrapped data from collection page

        # data variable receive page data 
        # from body HTML in str format.
        data = response.body

        debug(data)

        # parse to JSON format
        parsed_json_data = json.loads(data)

        # # token variable receive token identification from page data
        token = parsed_json_data['token']

        title = parsed_json_data['title']

        organismId = parsed_json_data['organismId']

        # # init ids array variable
        # ids = []

        amr_profile_data = []
        amr_snps_data = []
        amr_genes_data = []

        # # init separator str variable
        # separator = ','

        # file_type = 'amr_profile'

        # labels = ['NAME', 'AMP', 'CEP', 'CHL', 'CIP', 'SMX', 'TMP', 'SXT', 'TCY', 'AZM', 'CST', 'MEM']

        # # loop responsable to pass for each id 
        # # on genomes property and push to ids array
        for genome in parsed_json_data['genomes']:
        #     ids.append(genome['id'])

            if genome['analysis'] and genome['analysis']['paarsnp']:
                profile_data = dict()

                snps_data = dict()

                genes_data = dict()

                profile_data.update(dict(name=genome['name']))

                snps_data.update(dict(name=genome['name']))

                genes_data.update(dict(name=genome['name']))

                for resistance in genome['analysis']['paarsnp']['resistanceProfile']:
                    if resistance['determinantRules']:
                        for key, value in resistance['determinantRules'].items():
                            # debug(f'{key}, {value}')
                            if value == 'NOT_FOUND':
                                snps_data.update(
                                    {
                                        key: '0'
                                    }
                                )
                            else:
                                snps_data.update(
                                    {
                                        key: 1
                                    }
                                )

                    if resistance['determinants']['acquired']:
                        for gene in resistance['determinants']['acquired']:
                            if gene['resistanceEffect'] == 'NOT_FOUND':
                                genes_data.update(
                                    {
                                        gene['gene']: '0'
                                    }
                                )
                            else:
                                genes_data.update(
                                    {
                                        gene['gene']: 1
                                    }
                                )

                    if resistance['state'] == 'NOT_FOUND':
                        profile_data.update(
                            {
                                resistance['agent']['key']: '0'
                            }
                        )  
                    else:
                        profile_data.update(
                            {
                                resistance['agent']['key']: 1
                            }
                        )

                amr_profile_data.append(profile_data)
                amr_snps_data.append(snps_data)
                amr_genes_data.append(genes_data)


        # # self.log(amr_profile_data)
            
        collection_data = {
            'token': token,
            'amr_profile': amr_profile_data,
            'amr_snps': amr_snps_data,
            'amr_genes': amr_genes_data,
            'title': title
        }
        
        # # genome_ids variable receive amount of ids 
        # # to pass by form submit
        # genome_ids = separator.join(ids)

        # # form_data variable receive mountted params in JSON format
        # form_data = {
        #     'ids': genome_ids
        # }

        return dict(organismId=organismId, collection_data=collection_data)

        # loop responsable for take each organism and token to correct collection`s URL
        # for organism_name, organism_id in organisms():
        #     # check if on correct organism
        #     if organism_id == parsed_json_data['organismId']:

        #         save_csv_file(response, token, organism_name, amr_profile_data)

        #         # urls list variable
        #         urls = [
        #             f'https://pathogen.watch/download/collection/{token}/speciator?filename=pathogenwatch-{organism_name}-{token}-species-prediction.csv',
        #             f'https://pathogen.watch/download/collection/{token}/kleborate?filename=pathogenwatch-{organism_name}-{token}-kleborate.csv',
        #             f'https://pathogen.watch/download/collection/{token}/core-allele-distribution?filename=pathogenwatch-{organism_name}-{token}-core-allele-distribution.csv',
        #             f'https://pathogen.watch/download/collection/{token}/score-matrix?filename=pathogenwatch-{organism_name}-{token}-score-matrix.csv',
        #             f'https://pathogen.watch/download/collection/{token}/difference-matrix?filename=pathogenwatch-{organism_name}-{token}-difference-matrix.csv'
        #         ]

        #         yield urls

                # loop responsable to submit each data created by form_data variable
                # to correct collection`s URL 
                # and by pass token (collection identification) args & organism name
                # for url in urls:
                #     yield scrapy.FormRequest(
                #         url=url,
                #         method='POST',
                #         formdata=form_data,
                #         callback=save_csv_file,
                #         cb_kwargs=dict(token=token, organism=organism_name)
                #     )
