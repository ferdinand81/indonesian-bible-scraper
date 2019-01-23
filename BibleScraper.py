# Ferdinand Mudjialim 10/07/2018
# Parses Bible verses using Beautiful Soup and requests module
# Scrapes the site below to get Terjemahan Baru Indonesian Bible verses
# http://www.bibledbdata.org/onlinebibles/indonesian_tb/01_001.htm
import requests, bs4


def printVerses(book, chapterNumber, verseNumbers):

    bookIndList = ['kejadian', 'keluaran', 'imamat', 'bilangan', 'ulangan',
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
    bookEngList = ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy',
                    'joshua', 'judges', 'ruth', '1samuel', '2samuel', '1kings',
                    '2kings', '1chronicles', '2chronicles', 'ezra', 'nehemiah',
                    'esther', 'job', 'psalm', 'proverbs', 'ecclesiastes', 
                    'songofsongs', 'isaiah', 'jeremiah', 'lamentations', 
                    'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah', 
                    'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 
                    'haggai', 'zechariah', 'malachi', 'matthew', 'mark', 
                    'luke', 'john', 'acts', 'romans', '1corinthians', 
                    '2corinthians', 'galatians', 'ephesians', 'philippians', 
                    'colossians', '1thessalonians', '2thessalonians', 
                    '1timothy', '2timothy', 'titus', 'philemon', 'hebrews', 
                    'james', '1peter', '2peter', '1john', '2john', '3john', 
                    'jude', 'revelation']

    assert len(bookIndList) == len(bookEngList)  # make sure number of books =

    bookEncodings = ['0' + str(n) for n in range(1, 10)] \
                  + [str(m) for m in range(10, 67)]
    bookIndDict = dict(zip(bookIndList, bookEncodings))
    bookEngDict = dict(zip(bookEngList, bookEncodings))

    bookName = str(book.strip().lower())  # 2 digits format ex: 01
    chapter = str(chapterNumber.strip())  # 3 digits format ex: 001
    if len(chapter) <= 2:  # correct formatting for chapter numbers
        if len(chapter) == 1:
            chapter = '00' + chapter
        else:
            chapter = '0' + chapter
    verseInput = verseNumbers.strip()

    # If book name in Indonesian
    if bookName in bookIndList:
        bookNumber = bookIndDict[bookName]
    # If book name in English
    elif bookName in bookEngList:
        bookNumber = bookEngDict[bookName]
    else: 
        raise Exception(book)

    try: 
        res = requests.get('http://www.bibledbdata.org/onlinebibles/indonesian_tb/'
                           + str(bookNumber)  # book as number in URL string
                           + '_'
                           + str(chapter)  # chapter as number in URL string
                           + '.htm')
        res.raise_for_status()
    except Exception as e: 
        print("Error in book argument", e.args[0])

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
    temp += '\n' + bookName.title() + ' ' + chapter.lstrip('0') + '\n'
    for i in range(verseFrom, verseTo):
        temp += verseList[i] + '\n'
    return temp
    
def main(): 
    with open('input.txt') as fp:  # read from input.txt
        with open('output.txt', 'w') as out:  # write to output.txt
            line = fp.readline()
            while line != '':
                lineParseList = line.split()
                # If there are additional blank lines on the bottom
                if lineParseList == []:
                    break
                # Ignoring comment lines
                if lineParseList[0] == '#':
                    line = fp.readline()
                else:
                    out.write(printVerses(lineParseList[0], lineParseList[1],
                                          lineParseList[2]))
                    line = fp.readline()

if __name__ == '__main__':
    main()

