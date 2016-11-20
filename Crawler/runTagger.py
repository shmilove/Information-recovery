#encoding:utf-8
import urllib

from bgutags_new import *


def call_meni(text):
    text_encoded = text
    params = urllib.urlencode({'text': text_encoded})
    didnt_got_tags=True
    while didnt_got_tags:
        try:
            f = urllib.urlopen("HTTP://127.0.0.1:8086/bm", params)
            words = f.readlines()
            for word in words:
                if 'http error' in word.lower():
                    print 'error'
                    continue
            didnt_got_tags = False
        except:
            print 'meni error ???!?!'
    lemmas = []
    for word in words:
        if not word == '\n' and not word == '\r\n':
            splt = word.split('\t')

            lemmatized = splt
            pos = tostring1(int(splt[1])).split(',')[0].split(':')[1].split('-')[0]
            lemmas.append((splt[0], lemmatized, pos))

    stemming_string = []
    for word in lemmas:
        if word[1][2].__contains__("^"):
            stemming_string.append(word[1][2].split("^")[1])
        else:
            stemming_string.append(word[1][2])
    return " ".join(stemming_string).decode('utf-8')


# lemmas = call_meni("אני חולמת ועושה תכניות כאילו לא אירע כלום בעולם;  כאילו אין מלחמה והרס, אין אלפי מתים יום יום, אין מטוסים ומפציצים, וגרמניה, אנגליה, איטליה ויוון אינן משמידות זו את זו.  רק בארץ-ישראל הקטנה שלנו, שאף היא נתונה בסכנה ושעתידה אולי להימצא במרכז חזית המלחמה – בה כאילו שקט ושלווה.  ואני יושבת בתוכה וחושבת על העתיד.  ומה אני חושבת על העתיד הפרטי שלי?  – אחת התכניות היפות:  להיות מדריכה ללול במושבים, לנסוע ממקום למקום, לעבור במשקים, לייעץ ולעזור, לארגן, להנהיג רישום, לפתח את הענף.  בערב לתת סמינריון קצר לאנשי המושב וללמדם את הדברים החשובים בענף.  ודרך אגב, להכיר את האנשים, את חייהם, להסתובב קצת בארץ.")
# # file  = open("test.txt", "w")
# for word in lemmas:
#     print word[1][2]
#     # file.write(word[1][2])
# # file.close()
# input_var = input("Enter something: ")
# print ("you entered " + input_var)
