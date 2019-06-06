def is_isbn_or_key(word):
    """
    判断传入的是isbn还是关键字信息
    :param word:
    :return:
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        # q.isdigit() 判断q是否全为数字
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
