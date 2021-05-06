from logging import debug
from newick import loads, dump
from .generate_file import generate_path
from .generate_author_id_year import get_author_id_year


def save_nwk_file(response, token, tree, organism):
    # method responsable fro save tree file
    # and getting token and tree
    # :param str token: collection`s identification
    # :param str tree: newick data

    # filename variable receive URL collection page
    # splitted by slash, question mark and equals
    # to get filename from URL
    filename = response.url.split('/')[-1].split('?')[-1].split('=')[-1]

    # split token to get separated year, name and identification
    author, ID, year = get_author_id_year(token.split('-'))

    # path variable receive generated path to save file
    path = generate_path(filename, ID, author, year, organism, file_type='nwk')

    # parsed_tree variable receive tree node list 
    # from newick data in at str type
    parsed_tree = loads(tree)

    # open created file to write newick data
    with open(path, 'w') as f:

        # write parsed newick data on file
        dump(parsed_tree, f)
