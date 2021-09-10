def create_book(item):
    try:
        title = item['volumeInfo']['title']
    except:
        title = 'missingValue'

    try:
        authors = ','.join(item['volumeInfo']['authors'])
    except:
        authors = 'missingValue'

    try:
        published = item['volumeInfo']['publishedDate']
    except:
        published = 'missingValue'

    try:
        isbn = item['volumeInfo']['industryIdentifiers'][0]['identifier']
    except:
        isbn = 'missingValue'

    try:
        pages = item['volumeInfo']['pageCount']
    except:
        pages = 'missingValue'

    try:
        thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
    except:
        thumbnail = 'missingValue'

    try:
        language = item['volumeInfo']['language']
    except:
        language = 'missingValue'

    return title, authors, published, isbn, pages, thumbnail, language