import csv

def getDocument():
    documents = []
    with open('categorized/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        first = 1
        for row in reader:
            if first == 0 and row[0] != '':
                # TODO:
                # Try with title only first
                # Try with text only next
                documents.append((cleanString(row[2])+' '+cleanString(row[3]),row[0]))
            first = 0
        return documents

def getAllWords(document):
    allWords = []
    for row in document:
        for word in row[0].split(' '):
            allWords.append(word)
    return allWords

def cleanString(words):
    # TODO: Try with ntlk stopwords
    excludedNoSpace = [',', '[', ']', '(', ')', '-', ';', '"', '\'', ':', '.']
    excludedSpace = [' ourselves ', ' hers ', ' between ', ' yourself ', ' but ', ' again ', ' about ', ' once ', ' during ', ' out ', ' very ', ' having ', ' with ', ' they ', ' own ', ' an ', ' be ', 'some', ' for ', ' do ', ' its ', ' yours ', ' such ', ' into ', ' of ', ' most ', ' itself ', ' other ', ' off ', ' s ', ' am ', ' or ', ' as ', ' from ', ' him ', ' each ', ' the ', ' themselves ', ' until ', ' below ', ' these ', ' your ', ' his ', ' through ', ' don ', ' nor ', ' me ', ' were ', ' her ', ' more ', ' himself ', ' this ', ' down ', ' our ', ' their ',
                ' while ', ' above ', ' both ', ' up ', ' to ', ' ours ', ' had ', ' she ', ' all ', ' no ', ' when ', ' at ', ' any ', ' before ', ' them ', ' same ', ' and ', ' been ', ' have ', ' in ', ' will ', ' on ', ' yourselves ', ' then ', ' that ', ' because ', ' over ', ' so ', ' not ', ' now ', ' under ', ' he ', ' you ', ' herself ', ' has ', ' just ', ' where ', ' too ', ' only ', ' myself ', ' which ', ' those ', ' i ', ' after ', ' few ', ' whom ', ' t ', ' being ', ' theirs ', ' my ', ' against ', ' a ', ' by ', ' doing ', ' it ', ' further ', ' was ', ' here ', ' than ']

    for e in excludedNoSpace:
        words = words.replace(e, '')

    for e in excludedSpace:
        words = words.replace(e, ' ')
    return words.lower()
