# indonesian-bible-scraper
This Python program scrapes the online Terjemahan Baru Indonesian Bible from http://www.bibledbdata.org/onlinebibles/indonesian_tb and converts it into single output.txt file. The program takes input using custom syntax in the input.txt file. 

# Syntax for input.txt
[Name of book from bibleBooks.txt] <space> [Chapter #] <space> [Verse Range]
Verse range can be like "1", or "1-3", or "1-", or "-5", or "*" (not in quotes, of course)
Example: Mazmur 1 * (outputs all of Mazmur 1)
Example: Mazmur 1 -5 (outputs Mazmur 1: 1-5)
Example: Mazmur 2 10- (outputs Mazmur 2: 10-end)
Entries should be in separate newlines without extra blank spaces in between.
