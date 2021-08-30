from logging import debug
import os


def generate_path(filename, id, author, year, organism, file_type=None):
        # method responsable to generate directory and file to be saved
        # :param str filename: pass filename from URL
        # :param str id: collection`s identification
        # :param str author: author name
        # :param str year: year or None
        
        # second_dir variable receive directory`s name patten
        second_dir = f'{id}_{author}_{year}_core'

        # check if year param has not data
        if not year:

            # update second_dir directory`s name to it does not has year on name
            second_dir = f'{id}_{author}_core'
        
        # init separator str variable
        separator = '-'

        # init separator_2 str variable
        separator_2 = '_'

        # partial_path variable receive formatted to list filename
        partial_path = filename.split(separator)

        # current_dir variable receive current directory`s name
        current_dir = os.getcwd()

        # first_dir variable receive second item to be first directory 
        # where going to be save the file
        first_dir = organism

        # file variable going to receive filename 
        # where going to be save the data
        # the name going to be created 
        # from last 2 items on list 
        # joined by underscore
        file = separator_2.join(partial_path[-2:])
        if file == 'public_genomes':
            first_dir = file

        #check if has file_type
        if file_type:
            file = f'{file}.{file_type}'

        # path concat directories`s name
        # it creating path to save data
        path = f'{current_dir}/pathogen/files/collections/{first_dir}/{second_dir}'
        
        # check if not exists path
        if not os.path.exists(path):
            # create directories 
            # recursive method
            os.makedirs(path)

        # return path and file created
        return f'{path}/{file}'