# Ferdinand Mudjialim 10/07/2018
# Parses Bible verses using Beautiful Soup and requests module
# Scrapes the site below to get Terjemahan Baru Indonesian Bible verses
# http://www.bibledbdata.org/onlinebibles/indonesian_tb/01_001.htm
import requests, bs4


def printVerses(bookName, chapterNumber, verseNumbers):

    bookList = ['kejadian', 'keluaran', 'imamat', 'bilangan', 'ulangan',
                'yosua', 'hakim-hakim', 'rut', '1samuel', '2samuel',
                '1raja-raja', '2raja-raja', '1tawarikh', '2tawarikh',
                'ezra', 'nehemia', 'ester', 'ayub', 'mazmur', 'amsal',
                'pengkhotbah', 'kidungagung', 'yesaya', 'yeremia', 'ratapan',
                'yehezkiel', 'daniel', 'hosea', 'yoel', 'amos', 'obaja',
                'yunus', 'mikha', 'nahum', 'habakuk', 'zefanya', 'hagai',
                'zakharia', 'maleakhi', 'matius', 'markus', 'lukas', 'yohanes',
                'kisahpararasul', 'roma', '1korintus', '2korintus',
                'galatia', 'efesus', 'filipi', 'kolose', '1tesalonika',
                '2tesalonika', '1timotius', '2timotius', 'titus', 'filemon',
                'ibrani', 'yakobus', '1petrus', '2petrus', '1yohanes',
                '2yohanes', '3yohanes', 'yudas', 'wahyu']
    bookNumbers = ['0' + str(n) for n in range(1, 10)] \
                  + [str(m) for m in range(10, 67)]
    bookDict = dict(zip(bookList, bookNumbers))

    book = str(bookName.strip().lower())  # 2 digits format ex: 01
    chapter = str(chapterNumber.strip())  # 3 digits format ex: 001
    if len(chapter) <= 2:  # correct formatting for chapter numbers
        if len(chapter) == 1:
            chapter = '00' + chapter
        else:
            chapter = '0' + chapter
    verseInput = verseNumbers.strip()


    res = requests.get('http://www.bibledbdata.org/onlinebibles/indonesian_tb/'
                       + str(bookDict[book])
                       + '_'
                       + str(chapter)
                       + '.htm')
    res.raise_for_status()

    bibleSoup = bs4.BeautifulSoup(res.text, "html.parser")
    bibleSoup = bibleSoup.select('blockquote')
    string = bibleSoup[0].getText()
    verseList = string.split('\n')
    verseList = [y for y in verseList if y != '']  # list of verses in order

    if verseInput == '*':  # prints all verseInput
        verseFrom = 0
        verseTo = len(verseList)
    else:
        parsedVerseNumbers = verseInput.split('-')
        # if verseInput in form 'int-'
        if verseInput[len(verseInput) - 1] == '-':
            verseFrom = int(parsedVerseNumbers[0]) - 1
            verseTo = len(verseList)
        # if verseInput in form '-int'
        elif verseInput[0] == '-':
            verseFrom = 0
            verseTo = int(parsedVerseNumbers[1])
        # if verseInput in form 'int' and '-' is not found
        elif parsedVerseNumbers[0].isdigit() and verseInput.find('-') == -1:
            verseFrom = int(parsedVerseNumbers[0]) - 1
            verseTo = verseFrom + 1
        # normal from-to format
        else:
            verseFrom = int(parsedVerseNumbers[0]) - 1
            verseTo = int(parsedVerseNumbers[1])

    temp = ''
    temp += '\n' + book.title() + ' ' + chapter.lstrip('0') + '\n'
    for i in range(verseFrom, verseTo):
        temp += verseList[i] + '\n'
    return temp


with open('input.txt') as fp:
    with open('output.txt', 'w') as out:
        line = fp.readline()
        while line != '':
            lineParseList = line.split()

            if lineParseList[0] == '#':
                line = fp.readline()
            else:
                out.write(printVerses(lineParseList[0], lineParseList[1],
                                      lineParseList[2]))
                line = fp.readline()
