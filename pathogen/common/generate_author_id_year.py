from logging import debug


def get_author_id_year(token_list):
    # year variable receive last item from list
    year = token_list[-1]

    # ID variable receive first item from list and pass to str
    ID = token_list[0:1][0]

    # author variable receive second item from list
    author = token_list[1:2]

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
            # debug(f'It is not year ==>>{year}')
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
    # debug(f'DEBUG ===>>>>> YEAR = {year}')
    # debug(f'DEBUG ===>>>>> ID = {ID}')
    # debug(f'DEBUG ===>>>>> AUTHOR = {author}')

    return (author, ID, year)