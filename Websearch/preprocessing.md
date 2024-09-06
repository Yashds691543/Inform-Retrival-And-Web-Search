

```python
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

# Function to get text from a webpage, ignoring SSL verification
def get_text(url):
    html_code_1 = requests.get(url, verify=False).text
    data = BeautifulSoup(html_code_1, 'html.parser')
    links = []
    '''Acquired all the links that are on the web page'''
    for link in data.find_all('a'):
        links.append(link.get('href'))
    '''Removed this link as we are not able to access this link'''
    links.remove('http://www.people.memphis.edu/%7Ejaffairs/')
    text = []
    for link in links:
        if link is not None:
            if ('http' or 'https') in link:
                print(link)
                html_code = requests.get(link, verify=False).text
                code_to_text = BeautifulSoup(html_code, 'html.parser').get_text()
                text.append(code_to_text)
    return text

# Function to get text from Yahoo News articles, ignoring SSL verification
def get_yahoo_news_test(urls):
    text = []
    for url in urls:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = ''
        for news_item in soup.find_all('div', class_='caas-body'):
            body = body + news_item.find('p').text + ' '
        text.append(body)
    return text

# Fetch stopwords, ignoring SSL verification
response = requests.get('https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt', verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
stop_words = soup.text.split('\n')

# Source: https://stackoverflow.com/a/47091490/4084039
def decontracted(phrase):
    # Specific contractions
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    
    # General contractions
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def preprocess(text):
    ps = PorterStemmer()
    for i in range(len(text)):
        # Decontraction
        text[i] = decontracted(text[i])
        # Remove digits
        text[i] = re.sub(r'[0-9]+', '', text[i])
        # Remove punctuation
        text[i] = re.sub(r'[^\w\s]', '', text[i])
        # Remove URLs
        text[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text[i])
        # Remove HTML-like strings
        text[i] = re.sub('<[^<]+?>', '', text[i])
        # Remove stopwords and convert to lower case, and stem words
        text[i] = ' '.join(ps.stem(e) for e in text[i].lower().split() if e not in stop_words)
    return text

if __name__ == '__main__':
    text1 = get_text('http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/')
    urls = [
        'https://news.yahoo.com/nevada-secretary-state-contender-pledges-002032329.html', 
        'https://news.yahoo.com/students-protest-ben-sasse-views-222719353.html', 
        'https://news.yahoo.com/astrazenecas-covid-vaccine-suffers-setback-230741535.html', 
        'https://www.yahoo.com/news/california-parking-space-law-aims-for-affordable-housing-and-climate-change-win-win-222640846.html', 
        'https://www.yahoo.com/news/is-it-a-mistake-to-rebuild-in-climate-danger-zones-201845727.html', 
        'https://news.yahoo.com/alzheimers-memory-loss-know-your-body-184013508.html', 
        'https://news.yahoo.com/uk-prosecutor-nurse-poisoned-2-152252482.html', 
        'https://news.yahoo.com/conservation-explosion-frog-numbers-mass-014005619.html', 
        'https://news.yahoo.com/celebration-women-science-tech-ending-013326319.html', 
        'https://news.yahoo.com/spacex-falcon-9-puts-spectacular-004613023.html'
    ]
    text2 = get_yahoo_news_test(urls)
    preprocessed_text = preprocess(text1 + text2)
    print('preprocessed_text: ', preprocessed_text)
    
    # Save the preprocessed text using pickle
    # Source: https://stackoverflow.com/a/11218504
    with open('preprocessed_text.pkl', 'wb') as handle:
        pickle.dump(preprocessed_text, handle, protocol=pickle.HIGHEST_PROTOCOL)

```

    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.cs.memphis.edu/~vrus


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://tartarus.org/~martin/PorterStemmer/


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tartarus.org'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tartarus.org'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    http://www.memphis.edu/registrar/calendars/exams/16f-final.php


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'news.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1043: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.yahoo.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(


    preprocessed_text:  ['inform retriev institut intellig systemsth univers memphi inform retriev web search prof vasil ru comppsyc fall announc inform schedul announc due date assign dec assign due date nov assign open check schedul tabl due sept assign open check schedul tabl due sept enrol level section phd student send topic present sept syllabu inform retriev web search inform retriev web search address major problem time today major problem lack inform inform intellig way organ vast amount inform fingertip effect search face inform overload problem inform retriev web search class present major challeng pose problem solut challeng introduc comput techniqu search inform static collect document dynam collect web student expos text process algorithm classic inform retriev model boolean vectori model web search techniqu close relat natur languag process catalog entri advanc current research topic databas inform manag emphasi nontradit data applic prerequisit comp permiss instructor lectur tth ampm fogelman classroom build prof vasil ru ta shrestha bidhya ta shrestha bidhya bshrsthamemphisedu offic hour prof tth ppm appt dh ta mw pm dunn hall web page httpwwwcsmemphiseduvrusteachingirwebsearch textbook baezay ribeironeto modern inform retriev requir man raghavan schutz introduct inform retriev recommend polici grade assign midterm quiz participationinteractionpresent submiss lectur late lectur plagiar lectur intellectu engag lectur announc class read page assign gener grade correct robust qualiti solut document style assign written code requir code shoud follow recommend standard code style standard recommend plagiarismch polici plagiar cheat behavior form uneth detriment proper educ toler work submit student project program assign lab assign quizz test expect student work plagiar incur part work pass proper credit list sourc work reader led effort student allow encourag discuss resourc literatur includ internet assign refer includ materi consult citat made materi verbatim plagiar cheat occur student receiv fail grade assign instructor discret fail grade courseth instructor decid forward incid univers judici affair offic disciplinari action inform code student conduct academ disciplin procedur refer httpwwwpeoplememphisedujaffair tent schedul find lectur assign lectur compil sourc includ person note textbook materi relat class inform retriev natur languag process famou univers primarili ut austin dr ray mooney unt dr rada mihalcea materi week session session read assign week introduct ppt introduct ppt chapter assign week introduct perl ppt introduct perl ppt perl tutori assign week ir model ppt ir model ppt week ir model ppt retriev evalu ppt week retriev evalu ppt queri languag ppt chapter assign week queri oper ppt text properti ppt chapter assign week text oper ppt index search ppt chapter week fall break web search intro review ppt chapter porter stemmer porter stemmer slide assign week midterm web search intro ppt chapter mapreduc paper week web search ppt web search ppt assign pagerank paper chapter week text categor ppt text categor ppt week text cluster ppt text cluster ppt chapter assign week advanc ir modelsppt thanksgiv assign week advanc ir modelsppt question answer ppt week review quiz present class studi day week final exam amam depart comput scienc univers memphi dunn hall room memphi tn phone fax page maintain', 'inform retriev institut intellig systemsth univers memphi inform retriev web search prof vasil ru comppsyc fall announc inform schedul announc due date assign dec assign due date nov assign open check schedul tabl due sept assign open check schedul tabl due sept enrol level section phd student send topic present sept syllabu inform retriev web search inform retriev web search address major problem time today major problem lack inform inform intellig way organ vast amount inform fingertip effect search face inform overload problem inform retriev web search class present major challeng pose problem solut challeng introduc comput techniqu search inform static collect document dynam collect web student expos text process algorithm classic inform retriev model boolean vectori model web search techniqu close relat natur languag process catalog entri advanc current research topic databas inform manag emphasi nontradit data applic prerequisit comp permiss instructor lectur tth ampm fogelman classroom build prof vasil ru ta shrestha bidhya ta shrestha bidhya bshrsthamemphisedu offic hour prof tth ppm appt dh ta mw pm dunn hall web page httpwwwcsmemphiseduvrusteachingirwebsearch textbook baezay ribeironeto modern inform retriev requir man raghavan schutz introduct inform retriev recommend polici grade assign midterm quiz participationinteractionpresent submiss lectur late lectur plagiar lectur intellectu engag lectur announc class read page assign gener grade correct robust qualiti solut document style assign written code requir code shoud follow recommend standard code style standard recommend plagiarismch polici plagiar cheat behavior form uneth detriment proper educ toler work submit student project program assign lab assign quizz test expect student work plagiar incur part work pass proper credit list sourc work reader led effort student allow encourag discuss resourc literatur includ internet assign refer includ materi consult citat made materi verbatim plagiar cheat occur student receiv fail grade assign instructor discret fail grade courseth instructor decid forward incid univers judici affair offic disciplinari action inform code student conduct academ disciplin procedur refer httpwwwpeoplememphisedujaffair tent schedul find lectur assign lectur compil sourc includ person note textbook materi relat class inform retriev natur languag process famou univers primarili ut austin dr ray mooney unt dr rada mihalcea materi week session session read assign week introduct ppt introduct ppt chapter assign week introduct perl ppt introduct perl ppt perl tutori assign week ir model ppt ir model ppt week ir model ppt retriev evalu ppt week retriev evalu ppt queri languag ppt chapter assign week queri oper ppt text properti ppt chapter assign week text oper ppt index search ppt chapter week fall break web search intro review ppt chapter porter stemmer porter stemmer slide assign week midterm web search intro ppt chapter mapreduc paper week web search ppt web search ppt assign pagerank paper chapter week text categor ppt text categor ppt week text cluster ppt text cluster ppt chapter assign week advanc ir modelsppt thanksgiv assign week advanc ir modelsppt question answer ppt week review quiz present class studi day week final exam amam depart comput scienc univers memphi dunn hall room memphi tn phone fax page maintain', 'inform retriev institut intellig systemsth univers memphi inform retriev web search prof vasil ru comppsyc fall announc inform schedul announc due date assign dec assign due date nov assign open check schedul tabl due sept assign open check schedul tabl due sept enrol level section phd student send topic present sept syllabu inform retriev web search inform retriev web search address major problem time today major problem lack inform inform intellig way organ vast amount inform fingertip effect search face inform overload problem inform retriev web search class present major challeng pose problem solut challeng introduc comput techniqu search inform static collect document dynam collect web student expos text process algorithm classic inform retriev model boolean vectori model web search techniqu close relat natur languag process catalog entri advanc current research topic databas inform manag emphasi nontradit data applic prerequisit comp permiss instructor lectur tth ampm fogelman classroom build prof vasil ru ta shrestha bidhya ta shrestha bidhya bshrsthamemphisedu offic hour prof tth ppm appt dh ta mw pm dunn hall web page httpwwwcsmemphiseduvrusteachingirwebsearch textbook baezay ribeironeto modern inform retriev requir man raghavan schutz introduct inform retriev recommend polici grade assign midterm quiz participationinteractionpresent submiss lectur late lectur plagiar lectur intellectu engag lectur announc class read page assign gener grade correct robust qualiti solut document style assign written code requir code shoud follow recommend standard code style standard recommend plagiarismch polici plagiar cheat behavior form uneth detriment proper educ toler work submit student project program assign lab assign quizz test expect student work plagiar incur part work pass proper credit list sourc work reader led effort student allow encourag discuss resourc literatur includ internet assign refer includ materi consult citat made materi verbatim plagiar cheat occur student receiv fail grade assign instructor discret fail grade courseth instructor decid forward incid univers judici affair offic disciplinari action inform code student conduct academ disciplin procedur refer httpwwwpeoplememphisedujaffair tent schedul find lectur assign lectur compil sourc includ person note textbook materi relat class inform retriev natur languag process famou univers primarili ut austin dr ray mooney unt dr rada mihalcea materi week session session read assign week introduct ppt introduct ppt chapter assign week introduct perl ppt introduct perl ppt perl tutori assign week ir model ppt ir model ppt week ir model ppt retriev evalu ppt week retriev evalu ppt queri languag ppt chapter assign week queri oper ppt text properti ppt chapter assign week text oper ppt index search ppt chapter week fall break web search intro review ppt chapter porter stemmer porter stemmer slide assign week midterm web search intro ppt chapter mapreduc paper week web search ppt web search ppt assign pagerank paper chapter week text categor ppt text categor ppt week text cluster ppt text cluster ppt chapter assign week advanc ir modelsppt thanksgiv assign week advanc ir modelsppt question answer ppt week review quiz present class studi day week final exam amam depart comput scienc univers memphi dunn hall room memphi tn phone fax page maintain', '', 'inform retriev institut intellig systemsth univers memphi inform retriev web search prof vasil ru comppsyc fall announc inform schedul announc due date assign dec assign due date nov assign open check schedul tabl due sept assign open check schedul tabl due sept enrol level section phd student send topic present sept syllabu inform retriev web search inform retriev web search address major problem time today major problem lack inform inform intellig way organ vast amount inform fingertip effect search face inform overload problem inform retriev web search class present major challeng pose problem solut challeng introduc comput techniqu search inform static collect document dynam collect web student expos text process algorithm classic inform retriev model boolean vectori model web search techniqu close relat natur languag process catalog entri advanc current research topic databas inform manag emphasi nontradit data applic prerequisit comp permiss instructor lectur tth ampm fogelman classroom build prof vasil ru ta shrestha bidhya ta shrestha bidhya bshrsthamemphisedu offic hour prof tth ppm appt dh ta mw pm dunn hall web page httpwwwcsmemphiseduvrusteachingirwebsearch textbook baezay ribeironeto modern inform retriev requir man raghavan schutz introduct inform retriev recommend polici grade assign midterm quiz participationinteractionpresent submiss lectur late lectur plagiar lectur intellectu engag lectur announc class read page assign gener grade correct robust qualiti solut document style assign written code requir code shoud follow recommend standard code style standard recommend plagiarismch polici plagiar cheat behavior form uneth detriment proper educ toler work submit student project program assign lab assign quizz test expect student work plagiar incur part work pass proper credit list sourc work reader led effort student allow encourag discuss resourc literatur includ internet assign refer includ materi consult citat made materi verbatim plagiar cheat occur student receiv fail grade assign instructor discret fail grade courseth instructor decid forward incid univers judici affair offic disciplinari action inform code student conduct academ disciplin procedur refer httpwwwpeoplememphisedujaffair tent schedul find lectur assign lectur compil sourc includ person note textbook materi relat class inform retriev natur languag process famou univers primarili ut austin dr ray mooney unt dr rada mihalcea materi week session session read assign week introduct ppt introduct ppt chapter assign week introduct perl ppt introduct perl ppt perl tutori assign week ir model ppt ir model ppt week ir model ppt retriev evalu ppt week retriev evalu ppt queri languag ppt chapter assign week queri oper ppt text properti ppt chapter assign week text oper ppt index search ppt chapter week fall break web search intro review ppt chapter porter stemmer porter stemmer slide assign week midterm web search intro ppt chapter mapreduc paper week web search ppt web search ppt assign pagerank paper chapter week text categor ppt text categor ppt week text cluster ppt text cluster ppt chapter assign week advanc ir modelsppt thanksgiv assign week advanc ir modelsppt question answer ppt week review quiz present class studi day week final exam amam depart comput scienc univers memphi dunn hall room memphi tn phone fax page maintain', 'porter stem algorithm porter stem algorithm page complet revis jan earlier edit offici home page distribut porter stem algorithm written maintain author martin porter porter stem algorithm porter stemmer process remov common morpholog inflexion end word english main part term normalis process set inform retriev system histori origin stem algorithm paper written comput laboratori cambridg england part larger ir project appear chapter final project report cj van rijsbergen se robertson mf porter model probabilist inform retriev london british librari british librari research develop report van rijsbergen encourag publish mf porter algorithm suffix strip program pp reprint karen sparck jone peter willet read inform retriev san francisco morgan kaufmann isbn origin stemmer written bcpl languag popular defunct year distribut bcpl form medium punch paper tape version languag began wide quot adapt numer variat function version web page set primarili put record straight establish definit version distribut encod ansi version head tabl equival origin bcpl version bcpl version differ minor point publish algorithm mark download ansi version discuss ansi version regard definit act definit algorithm origin publish paper year receiv encod worker present reason confid version correctli encod languag author affili receiv note ansi ansi thread safe java perl perl daniel van balen oct slightli faster python vivak gupta jan csharp andré hazelwood offici web guid sep csharp net compliant leif azzopardi univer paisley scotland nov csharp brad patton ratborgblogspotcom dec standard code brad csharp frank kolnick jan compact simplifi frank common lisp steven haflich franz mar rubi ray pereda wwwrayperedacom jan github link visual basic vb navonil mustafe brunel univers apr delphi jo rabin apr javascript andargor wwwandargorcom jul substanti revis bychristoph mckenzi visual basicvb net compliant christo attiko univers piraeu greec jan php richard hey wwwphpguruorg feb prolog philip brook univers georgia oct haskel dmitri antonyuk nov tsql keith lubel wwwatelierdevitrauxcom matlab juan carlo lopez california pacif medic centerresearch institut sep tcl ari theodorako ncsr demokrito nov daniel truemper humboldtuniversitaet zu berlin erlang erlang alden dima nation institut standard andtechnolog gaithersburg md usa sep rebol dale brearcliff apr scala ken faulkner sa antoin stpierr busi research apr plugin vim script mitchel bowden github link nodej jed parson jedparsonscom github link googl alex gonopolskiy oct github link awk gregori grefenstett dscomexalead jul clojur yushi wang mar bitbucket link rust nhat minh nanyang technolog univers aug github link vala serg huln sep mysql john carti enlighten job jan github link julia matãa guzmãn naranjo github link flex zalãn bodã³ babesbolyai univers oct zalan note mohit makkar indian institut technolog delhi nov groovi dhaval dave jun github link oorexx po jonsson jul sourceforg link xslt joey takeda feb github link lpa winprolog brian steel solanumorg apr gnu pspp fran houwel feb typescript max patiiuk github link encod algorithm free charg purpos question algorithm direct author martin porter author test program sampl vocabulari megabyt output email comment suggest queri point differ publish algorithm extra rule step logi log archaeolog equat archaeolog step rule abli replac bli ble possibl equat algorithm leav string length case string length unchang pass algorithm string length lose final differ present program publish algorithm deriv great distanc origin public difficult emphasis differ small compar variat observ encod algorithm statu porter stemmer regard frozen strictli defin amen modif stemmer slightli inferior snowbal english porter stemmer deriv subject occasion improv practic work snowbal stemmer recommend porter stemmer ir research work involv stem experi repeat common error histor shortcom found encod stem algorithm algorithm explain set rule type condit present rule appli longest match suffix word true rule succe fail replac rule simpli appli turn succe list run lead small error place step rule mement mment ment remov final ement ment ent properli argument stem argument longest match suffix ment stem argu measur equal ment remov end step rule appli turn suffix ent stem argum measur equal ent remov delic rule liabl misinterpret greater care requir explain tion ms tion mean take ion leav stem measur greater end mean take sion tion leav stem measur greater similar confus aris interpret rule reduc final doubl singl occasion cruder error test conson vowel set wrong round interest publish paper explain test string program switch letter encod fail techniqu make slower faq frequent ask question licens arrang softwar question popular recent period clear statment encod algorithm free charg purpos problem intellectu properti major issu formal statement expect restat softwar complet free purpos note head program text rare case note licens restrict bsd licens case softwar written martin porter licens arrang endors contributor unnecessari contributor confirm ask contributor employ proof distribut softwar take softwar snowbal websit posit similar simpler softwar issu bsd licens contribut written martin porter richard boulton ask author author employ proof distribut right stemmer produc proper word crude error stem algorithm leav real word remov stem purpos stem bring variant form word map word paradigm form connect error question form word stem expect stem import rememb stem algorithm achiev perfect balanc improv ir perform individu case make error matter suggest addit rule includ stemmer improv perform', 'file found', 'head coalit elect denier stand secretari state posit key battleground state made explicit threat power win novemb subvert democraci forc return donald trump white hous', 'week reveal presid univers florida uf republican senat ben sass met protest appear campu gainesvil monday', 'reuter attempt oxford univers research astrazeneca plc creat nasalspray version jointli develop covid shot suffer setback tuesday initi test human yield desir protect', 'california famou car cultur automot websit jalopnik dub environment skyhigh hous price effort lower cost construct cut car depend state recent adopt law prohibit local govern set minimum park requir build half mile transit hub rail station intersect bu line', 'show divers perspect day top stori debat', 'estim million american age live alzheim diseas progress diseas devast symptom rang memori loss seizur nation institut age nia', 'london ap hospit neonat nurs accus kill babi kill poison infant deliber insulin british prosecutor monday', '', '', 'run day late backtoback scrub spacex launch pair intelsat commun satellit cape canaver saturday even compani falcon launch day flight wednesday coast hour']



```python
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

def get_inverted_indices(preprocessed_text):
    preprocessed_text_dict = {'d'+str(i) : preprocessed_text[i] for i in range(len(preprocessed_text))}

    
    inverted_indices_dict = {}

    for document in preprocessed_text_dict:
      text = preprocessed_text_dict[document]
      tokens = text.strip().split()
      for token in tokens:
        try:
          inverted_indices_dict[(token, document)] += 1
        except:
          inverted_indices_dict[token, document] = 1
    return inverted_indices_dict
    

if __name__ == '__main__':
    with open('preprocessed_text', 'rb') as handle:
        preprocessed_text = pickle.load(handle)

    inverted_indices_dict = get_inverted_indices(preprocessed_text)
    print('inverted_indices_dict: ', inverted_indices_dict)
    
    # saving the inverted indices for future use
    with open('inverted_indices', 'wb') as handle:
        pickle.dump(inverted_indices_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
```

    inverted_indices_dict:  {('inform', 'd0'): 17, ('retriev', 'd0'): 11, ('institut', 'd0'): 1, ('intellig', 'd0'): 2, ('systemsth', 'd0'): 1, ('univers', 'd0'): 4, ('memphi', 'd0'): 3, ('web', 'd0'): 11, ('search', 'd0'): 12, ('prof', 'd0'): 3, ('vasil', 'd0'): 2, ('ru', 'd0'): 2, ('comppsyc', 'd0'): 1, ('fall', 'd0'): 2, ('announc', 'd0'): 3, ('schedul', 'd0'): 4, ('assign', 'd0'): 20, ('due', 'd0'): 3, ('oct', 'd0'): 1, ('open', 'd0'): 2, ('check', 'd0'): 2, ('tabl', 'd0'): 2, ('sept', 'd0'): 3, ('enrol', 'd0'): 1, ('level', 'd0'): 1, ('section', 'd0'): 1, ('phd', 'd0'): 1, ('student', 'd0'): 7, ('send', 'd0'): 1, ('topic', 'd0'): 2, ('present', 'd0'): 3, ('syllabu', 'd0'): 1, ('address', 'd0'): 1, ('major', 'd0'): 3, ('problem', 'd0'): 4, ('time', 'd0'): 1, ('today', 'd0'): 1, ('lack', 'd0'): 1, ('way', 'd0'): 1, ('organ', 'd0'): 1, ('vast', 'd0'): 1, ('amount', 'd0'): 1, ('fingertip', 'd0'): 1, ('effect', 'd0'): 1, ('face', 'd0'): 1, ('overload', 'd0'): 1, ('class', 'd0'): 3, ('challeng', 'd0'): 2, ('pose', 'd0'): 1, ('solut', 'd0'): 2, ('introduc', 'd0'): 1, ('comput', 'd0'): 2, ('techniqu', 'd0'): 2, ('static', 'd0'): 1, ('collect', 'd0'): 2, ('document', 'd0'): 2, ('dynam', 'd0'): 1, ('expos', 'd0'): 1, ('text', 'd0'): 7, ('process', 'd0'): 3, ('algorithm', 'd0'): 1, ('classic', 'd0'): 1, ('model', 'd0'): 5, ('boolean', 'd0'): 1, ('vectori', 'd0'): 1, ('close', 'd0'): 1, ('relat', 'd0'): 2, ('natur', 'd0'): 2, ('languag', 'd0'): 3, ('catalog', 'd0'): 1, ('entri', 'd0'): 1, ('advanc', 'd0'): 3, ('current', 'd0'): 1, ('research', 'd0'): 1, ('databas', 'd0'): 1, ('manag', 'd0'): 1, ('emphasi', 'd0'): 1, ('nontradit', 'd0'): 1, ('data', 'd0'): 1, ('applic', 'd0'): 1, ('prerequisit', 'd0'): 1, ('comp', 'd0'): 1, ('permiss', 'd0'): 1, ('instructor', 'd0'): 3, ('lectur', 'd0'): 7, ('tth', 'd0'): 2, ('ampm', 'd0'): 1, ('fogelman', 'd0'): 1, ('classroom', 'd0'): 1, ('build', 'd0'): 1, ('ta', 'd0'): 3, ('shrestha', 'd0'): 2, ('bidhya', 'd0'): 2, ('bshrsthamemphisedu', 'd0'): 1, ('offic', 'd0'): 2, ('hour', 'd0'): 1, ('ppm', 'd0'): 1, ('appt', 'd0'): 1, ('dh', 'd0'): 1, ('mw', 'd0'): 1, ('pm', 'd0'): 1, ('dunn', 'd0'): 2, ('hall', 'd0'): 2, ('page', 'd0'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd0'): 1, ('textbook', 'd0'): 2, ('baezay', 'd0'): 1, ('ribeironeto', 'd0'): 1, ('modern', 'd0'): 1, ('requir', 'd0'): 2, ('man', 'd0'): 1, ('raghavan', 'd0'): 1, ('schutz', 'd0'): 1, ('introduct', 'd0'): 5, ('recommend', 'd0'): 3, ('polici', 'd0'): 2, ('grade', 'd0'): 4, ('midterm', 'd0'): 2, ('quiz', 'd0'): 1, ('participationinteractionpresent', 'd0'): 1, ('submiss', 'd0'): 1, ('late', 'd0'): 1, ('plagiar', 'd0'): 4, ('intellectu', 'd0'): 1, ('engag', 'd0'): 1, ('read', 'd0'): 2, ('gener', 'd0'): 1, ('correct', 'd0'): 1, ('robust', 'd0'): 1, ('qualiti', 'd0'): 1, ('style', 'd0'): 2, ('written', 'd0'): 1, ('code', 'd0'): 4, ('shoud', 'd0'): 1, ('follow', 'd0'): 1, ('standard', 'd0'): 2, ('plagiarismch', 'd0'): 1, ('cheat', 'd0'): 2, ('behavior', 'd0'): 1, ('form', 'd0'): 1, ('uneth', 'd0'): 1, ('detriment', 'd0'): 1, ('proper', 'd0'): 2, ('educ', 'd0'): 1, ('toler', 'd0'): 1, ('work', 'd0'): 4, ('submit', 'd0'): 1, ('project', 'd0'): 2, ('program', 'd0'): 1, ('lab', 'd0'): 1, ('quizz', 'd0'): 1, ('test', 'd0'): 1, ('expect', 'd0'): 1, ('incur', 'd0'): 1, ('part', 'd0'): 1, ('pass', 'd0'): 1, ('credit', 'd0'): 1, ('list', 'd0'): 1, ('sourc', 'd0'): 2, ('reader', 'd0'): 1, ('led', 'd0'): 1, ('effort', 'd0'): 1, ('allow', 'd0'): 1, ('encourag', 'd0'): 1, ('discuss', 'd0'): 1, ('resourc', 'd0'): 1, ('literatur', 'd0'): 1, ('includ', 'd0'): 3, ('internet', 'd0'): 1, ('refer', 'd0'): 2, ('materi', 'd0'): 4, ('consult', 'd0'): 1, ('citat', 'd0'): 1, ('made', 'd0'): 1, ('verbatim', 'd0'): 1, ('occur', 'd0'): 1, ('receiv', 'd0'): 1, ('fail', 'd0'): 2, ('discret', 'd0'): 1, ('courseth', 'd0'): 1, ('decid', 'd0'): 1, ('forward', 'd0'): 1, ('incid', 'd0'): 1, ('judici', 'd0'): 1, ('affair', 'd0'): 1, ('disciplinari', 'd0'): 1, ('action', 'd0'): 1, ('conduct', 'd0'): 1, ('academ', 'd0'): 1, ('disciplin', 'd0'): 1, ('procedur', 'd0'): 1, ('httpwwwpeoplememphisedujaffair', 'd0'): 1, ('tent', 'd0'): 1, ('find', 'd0'): 1, ('compil', 'd0'): 1, ('person', 'd0'): 1, ('note', 'd0'): 1, ('famou', 'd0'): 1, ('primarili', 'd0'): 1, ('ut', 'd0'): 1, ('austin', 'd0'): 1, ('dr', 'd0'): 2, ('ray', 'd0'): 1, ('mooney', 'd0'): 1, ('unt', 'd0'): 1, ('rada', 'd0'): 1, ('mihalcea', 'd0'): 1, ('week', 'd0'): 17, ('half', 'd0'): 2, ('ppt', 'd0'): 23, ('chapter', 'd0'): 8, ('perl', 'd0'): 3, ('tutori', 'd0'): 1, ('ir', 'd0'): 5, ('evalu', 'd0'): 2, ('queri', 'd0'): 2, ('oper', 'd0'): 2, ('properti', 'd0'): 1, ('index', 'd0'): 1, ('break', 'd0'): 1, ('intro', 'd0'): 2, ('review', 'd0'): 3, ('porter', 'd0'): 2, ('stemmer', 'd0'): 2, ('slide', 'd0'): 1, ('mapreduc', 'd0'): 1, ('paper', 'd0'): 2, ('pagerank', 'd0'): 1, ('categor', 'd0'): 2, ('cluster', 'd0'): 2, ('modelsppt', 'd0'): 2, ('question', 'd0'): 1, ('answer', 'd0'): 1, ('thanksgiv', 'd0'): 1, ('final', 'd0'): 1, ('exam', 'd0'): 1, ('amam', 'd0'): 1, ('depart', 'd0'): 1, ('scienc', 'd0'): 1, ('room', 'd0'): 1, ('tn', 'd0'): 1, ('phone', 'd0'): 1, ('fax', 'd0'): 1, ('maintain', 'd0'): 1, ('inform', 'd1'): 17, ('retriev', 'd1'): 11, ('institut', 'd1'): 1, ('intellig', 'd1'): 2, ('systemsth', 'd1'): 1, ('univers', 'd1'): 4, ('memphi', 'd1'): 3, ('web', 'd1'): 11, ('search', 'd1'): 12, ('prof', 'd1'): 3, ('vasil', 'd1'): 2, ('ru', 'd1'): 2, ('comppsyc', 'd1'): 1, ('fall', 'd1'): 2, ('announc', 'd1'): 3, ('schedul', 'd1'): 4, ('assign', 'd1'): 20, ('due', 'd1'): 3, ('oct', 'd1'): 1, ('open', 'd1'): 2, ('check', 'd1'): 2, ('tabl', 'd1'): 2, ('sept', 'd1'): 3, ('enrol', 'd1'): 1, ('level', 'd1'): 1, ('section', 'd1'): 1, ('phd', 'd1'): 1, ('student', 'd1'): 7, ('send', 'd1'): 1, ('topic', 'd1'): 2, ('present', 'd1'): 3, ('syllabu', 'd1'): 1, ('address', 'd1'): 1, ('major', 'd1'): 3, ('problem', 'd1'): 4, ('time', 'd1'): 1, ('today', 'd1'): 1, ('lack', 'd1'): 1, ('way', 'd1'): 1, ('organ', 'd1'): 1, ('vast', 'd1'): 1, ('amount', 'd1'): 1, ('fingertip', 'd1'): 1, ('effect', 'd1'): 1, ('face', 'd1'): 1, ('overload', 'd1'): 1, ('class', 'd1'): 3, ('challeng', 'd1'): 2, ('pose', 'd1'): 1, ('solut', 'd1'): 2, ('introduc', 'd1'): 1, ('comput', 'd1'): 2, ('techniqu', 'd1'): 2, ('static', 'd1'): 1, ('collect', 'd1'): 2, ('document', 'd1'): 2, ('dynam', 'd1'): 1, ('expos', 'd1'): 1, ('text', 'd1'): 7, ('process', 'd1'): 3, ('algorithm', 'd1'): 1, ('classic', 'd1'): 1, ('model', 'd1'): 5, ('boolean', 'd1'): 1, ('vectori', 'd1'): 1, ('close', 'd1'): 1, ('relat', 'd1'): 2, ('natur', 'd1'): 2, ('languag', 'd1'): 3, ('catalog', 'd1'): 1, ('entri', 'd1'): 1, ('advanc', 'd1'): 3, ('current', 'd1'): 1, ('research', 'd1'): 1, ('databas', 'd1'): 1, ('manag', 'd1'): 1, ('emphasi', 'd1'): 1, ('nontradit', 'd1'): 1, ('data', 'd1'): 1, ('applic', 'd1'): 1, ('prerequisit', 'd1'): 1, ('comp', 'd1'): 1, ('permiss', 'd1'): 1, ('instructor', 'd1'): 3, ('lectur', 'd1'): 7, ('tth', 'd1'): 2, ('ampm', 'd1'): 1, ('fogelman', 'd1'): 1, ('classroom', 'd1'): 1, ('build', 'd1'): 1, ('ta', 'd1'): 3, ('shrestha', 'd1'): 2, ('bidhya', 'd1'): 2, ('bshrsthamemphisedu', 'd1'): 1, ('offic', 'd1'): 2, ('hour', 'd1'): 1, ('ppm', 'd1'): 1, ('appt', 'd1'): 1, ('dh', 'd1'): 1, ('mw', 'd1'): 1, ('pm', 'd1'): 1, ('dunn', 'd1'): 2, ('hall', 'd1'): 2, ('page', 'd1'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd1'): 1, ('textbook', 'd1'): 2, ('baezay', 'd1'): 1, ('ribeironeto', 'd1'): 1, ('modern', 'd1'): 1, ('requir', 'd1'): 2, ('man', 'd1'): 1, ('raghavan', 'd1'): 1, ('schutz', 'd1'): 1, ('introduct', 'd1'): 5, ('recommend', 'd1'): 3, ('polici', 'd1'): 2, ('grade', 'd1'): 4, ('midterm', 'd1'): 2, ('quiz', 'd1'): 1, ('participationinteractionpresent', 'd1'): 1, ('submiss', 'd1'): 1, ('late', 'd1'): 1, ('plagiar', 'd1'): 4, ('intellectu', 'd1'): 1, ('engag', 'd1'): 1, ('read', 'd1'): 2, ('gener', 'd1'): 1, ('correct', 'd1'): 1, ('robust', 'd1'): 1, ('qualiti', 'd1'): 1, ('style', 'd1'): 2, ('written', 'd1'): 1, ('code', 'd1'): 4, ('shoud', 'd1'): 1, ('follow', 'd1'): 1, ('standard', 'd1'): 2, ('plagiarismch', 'd1'): 1, ('cheat', 'd1'): 2, ('behavior', 'd1'): 1, ('form', 'd1'): 1, ('uneth', 'd1'): 1, ('detriment', 'd1'): 1, ('proper', 'd1'): 2, ('educ', 'd1'): 1, ('toler', 'd1'): 1, ('work', 'd1'): 4, ('submit', 'd1'): 1, ('project', 'd1'): 2, ('program', 'd1'): 1, ('lab', 'd1'): 1, ('quizz', 'd1'): 1, ('test', 'd1'): 1, ('expect', 'd1'): 1, ('incur', 'd1'): 1, ('part', 'd1'): 1, ('pass', 'd1'): 1, ('credit', 'd1'): 1, ('list', 'd1'): 1, ('sourc', 'd1'): 2, ('reader', 'd1'): 1, ('led', 'd1'): 1, ('effort', 'd1'): 1, ('allow', 'd1'): 1, ('encourag', 'd1'): 1, ('discuss', 'd1'): 1, ('resourc', 'd1'): 1, ('literatur', 'd1'): 1, ('includ', 'd1'): 3, ('internet', 'd1'): 1, ('refer', 'd1'): 2, ('materi', 'd1'): 4, ('consult', 'd1'): 1, ('citat', 'd1'): 1, ('made', 'd1'): 1, ('verbatim', 'd1'): 1, ('occur', 'd1'): 1, ('receiv', 'd1'): 1, ('fail', 'd1'): 2, ('discret', 'd1'): 1, ('courseth', 'd1'): 1, ('decid', 'd1'): 1, ('forward', 'd1'): 1, ('incid', 'd1'): 1, ('judici', 'd1'): 1, ('affair', 'd1'): 1, ('disciplinari', 'd1'): 1, ('action', 'd1'): 1, ('conduct', 'd1'): 1, ('academ', 'd1'): 1, ('disciplin', 'd1'): 1, ('procedur', 'd1'): 1, ('httpwwwpeoplememphisedujaffair', 'd1'): 1, ('tent', 'd1'): 1, ('find', 'd1'): 1, ('compil', 'd1'): 1, ('person', 'd1'): 1, ('note', 'd1'): 1, ('famou', 'd1'): 1, ('primarili', 'd1'): 1, ('ut', 'd1'): 1, ('austin', 'd1'): 1, ('dr', 'd1'): 2, ('ray', 'd1'): 1, ('mooney', 'd1'): 1, ('unt', 'd1'): 1, ('rada', 'd1'): 1, ('mihalcea', 'd1'): 1, ('week', 'd1'): 17, ('half', 'd1'): 2, ('ppt', 'd1'): 23, ('chapter', 'd1'): 8, ('perl', 'd1'): 3, ('tutori', 'd1'): 1, ('ir', 'd1'): 5, ('evalu', 'd1'): 2, ('queri', 'd1'): 2, ('oper', 'd1'): 2, ('properti', 'd1'): 1, ('index', 'd1'): 1, ('break', 'd1'): 1, ('intro', 'd1'): 2, ('review', 'd1'): 3, ('porter', 'd1'): 2, ('stemmer', 'd1'): 2, ('slide', 'd1'): 1, ('mapreduc', 'd1'): 1, ('paper', 'd1'): 2, ('pagerank', 'd1'): 1, ('categor', 'd1'): 2, ('cluster', 'd1'): 2, ('modelsppt', 'd1'): 2, ('question', 'd1'): 1, ('answer', 'd1'): 1, ('thanksgiv', 'd1'): 1, ('final', 'd1'): 1, ('exam', 'd1'): 1, ('amam', 'd1'): 1, ('depart', 'd1'): 1, ('scienc', 'd1'): 1, ('room', 'd1'): 1, ('tn', 'd1'): 1, ('phone', 'd1'): 1, ('fax', 'd1'): 1, ('maintain', 'd1'): 1, ('inform', 'd2'): 17, ('retriev', 'd2'): 11, ('institut', 'd2'): 1, ('intellig', 'd2'): 2, ('systemsth', 'd2'): 1, ('univers', 'd2'): 4, ('memphi', 'd2'): 3, ('web', 'd2'): 11, ('search', 'd2'): 12, ('prof', 'd2'): 3, ('vasil', 'd2'): 2, ('ru', 'd2'): 2, ('comppsyc', 'd2'): 1, ('fall', 'd2'): 2, ('announc', 'd2'): 3, ('schedul', 'd2'): 4, ('assign', 'd2'): 20, ('due', 'd2'): 3, ('oct', 'd2'): 1, ('open', 'd2'): 2, ('check', 'd2'): 2, ('tabl', 'd2'): 2, ('sept', 'd2'): 3, ('enrol', 'd2'): 1, ('level', 'd2'): 1, ('section', 'd2'): 1, ('phd', 'd2'): 1, ('student', 'd2'): 7, ('send', 'd2'): 1, ('topic', 'd2'): 2, ('present', 'd2'): 3, ('syllabu', 'd2'): 1, ('address', 'd2'): 1, ('major', 'd2'): 3, ('problem', 'd2'): 4, ('time', 'd2'): 1, ('today', 'd2'): 1, ('lack', 'd2'): 1, ('way', 'd2'): 1, ('organ', 'd2'): 1, ('vast', 'd2'): 1, ('amount', 'd2'): 1, ('fingertip', 'd2'): 1, ('effect', 'd2'): 1, ('face', 'd2'): 1, ('overload', 'd2'): 1, ('class', 'd2'): 3, ('challeng', 'd2'): 2, ('pose', 'd2'): 1, ('solut', 'd2'): 2, ('introduc', 'd2'): 1, ('comput', 'd2'): 2, ('techniqu', 'd2'): 2, ('static', 'd2'): 1, ('collect', 'd2'): 2, ('document', 'd2'): 2, ('dynam', 'd2'): 1, ('expos', 'd2'): 1, ('text', 'd2'): 7, ('process', 'd2'): 3, ('algorithm', 'd2'): 1, ('classic', 'd2'): 1, ('model', 'd2'): 5, ('boolean', 'd2'): 1, ('vectori', 'd2'): 1, ('close', 'd2'): 1, ('relat', 'd2'): 2, ('natur', 'd2'): 2, ('languag', 'd2'): 3, ('catalog', 'd2'): 1, ('entri', 'd2'): 1, ('advanc', 'd2'): 3, ('current', 'd2'): 1, ('research', 'd2'): 1, ('databas', 'd2'): 1, ('manag', 'd2'): 1, ('emphasi', 'd2'): 1, ('nontradit', 'd2'): 1, ('data', 'd2'): 1, ('applic', 'd2'): 1, ('prerequisit', 'd2'): 1, ('comp', 'd2'): 1, ('permiss', 'd2'): 1, ('instructor', 'd2'): 3, ('lectur', 'd2'): 7, ('tth', 'd2'): 2, ('ampm', 'd2'): 1, ('fogelman', 'd2'): 1, ('classroom', 'd2'): 1, ('build', 'd2'): 1, ('ta', 'd2'): 3, ('shrestha', 'd2'): 2, ('bidhya', 'd2'): 2, ('bshrsthamemphisedu', 'd2'): 1, ('offic', 'd2'): 2, ('hour', 'd2'): 1, ('ppm', 'd2'): 1, ('appt', 'd2'): 1, ('dh', 'd2'): 1, ('mw', 'd2'): 1, ('pm', 'd2'): 1, ('dunn', 'd2'): 2, ('hall', 'd2'): 2, ('page', 'd2'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd2'): 1, ('textbook', 'd2'): 2, ('baezay', 'd2'): 1, ('ribeironeto', 'd2'): 1, ('modern', 'd2'): 1, ('requir', 'd2'): 2, ('man', 'd2'): 1, ('raghavan', 'd2'): 1, ('schutz', 'd2'): 1, ('introduct', 'd2'): 5, ('recommend', 'd2'): 3, ('polici', 'd2'): 2, ('grade', 'd2'): 4, ('midterm', 'd2'): 2, ('quiz', 'd2'): 1, ('participationinteractionpresent', 'd2'): 1, ('submiss', 'd2'): 1, ('late', 'd2'): 1, ('plagiar', 'd2'): 4, ('intellectu', 'd2'): 1, ('engag', 'd2'): 1, ('read', 'd2'): 2, ('gener', 'd2'): 1, ('correct', 'd2'): 1, ('robust', 'd2'): 1, ('qualiti', 'd2'): 1, ('style', 'd2'): 2, ('written', 'd2'): 1, ('code', 'd2'): 4, ('shoud', 'd2'): 1, ('follow', 'd2'): 1, ('standard', 'd2'): 2, ('plagiarismch', 'd2'): 1, ('cheat', 'd2'): 2, ('behavior', 'd2'): 1, ('form', 'd2'): 1, ('uneth', 'd2'): 1, ('detriment', 'd2'): 1, ('proper', 'd2'): 2, ('educ', 'd2'): 1, ('toler', 'd2'): 1, ('work', 'd2'): 4, ('submit', 'd2'): 1, ('project', 'd2'): 2, ('program', 'd2'): 1, ('lab', 'd2'): 1, ('quizz', 'd2'): 1, ('test', 'd2'): 1, ('expect', 'd2'): 1, ('incur', 'd2'): 1, ('part', 'd2'): 1, ('pass', 'd2'): 1, ('credit', 'd2'): 1, ('list', 'd2'): 1, ('sourc', 'd2'): 2, ('reader', 'd2'): 1, ('led', 'd2'): 1, ('effort', 'd2'): 1, ('allow', 'd2'): 1, ('encourag', 'd2'): 1, ('discuss', 'd2'): 1, ('resourc', 'd2'): 1, ('literatur', 'd2'): 1, ('includ', 'd2'): 3, ('internet', 'd2'): 1, ('refer', 'd2'): 2, ('materi', 'd2'): 4, ('consult', 'd2'): 1, ('citat', 'd2'): 1, ('made', 'd2'): 1, ('verbatim', 'd2'): 1, ('occur', 'd2'): 1, ('receiv', 'd2'): 1, ('fail', 'd2'): 2, ('discret', 'd2'): 1, ('courseth', 'd2'): 1, ('decid', 'd2'): 1, ('forward', 'd2'): 1, ('incid', 'd2'): 1, ('judici', 'd2'): 1, ('affair', 'd2'): 1, ('disciplinari', 'd2'): 1, ('action', 'd2'): 1, ('conduct', 'd2'): 1, ('academ', 'd2'): 1, ('disciplin', 'd2'): 1, ('procedur', 'd2'): 1, ('httpwwwpeoplememphisedujaffair', 'd2'): 1, ('tent', 'd2'): 1, ('find', 'd2'): 1, ('compil', 'd2'): 1, ('person', 'd2'): 1, ('note', 'd2'): 1, ('famou', 'd2'): 1, ('primarili', 'd2'): 1, ('ut', 'd2'): 1, ('austin', 'd2'): 1, ('dr', 'd2'): 2, ('ray', 'd2'): 1, ('mooney', 'd2'): 1, ('unt', 'd2'): 1, ('rada', 'd2'): 1, ('mihalcea', 'd2'): 1, ('week', 'd2'): 17, ('half', 'd2'): 2, ('ppt', 'd2'): 23, ('chapter', 'd2'): 8, ('perl', 'd2'): 3, ('tutori', 'd2'): 1, ('ir', 'd2'): 5, ('evalu', 'd2'): 2, ('queri', 'd2'): 2, ('oper', 'd2'): 2, ('properti', 'd2'): 1, ('index', 'd2'): 1, ('break', 'd2'): 1, ('intro', 'd2'): 2, ('review', 'd2'): 3, ('porter', 'd2'): 2, ('stemmer', 'd2'): 2, ('slide', 'd2'): 1, ('mapreduc', 'd2'): 1, ('paper', 'd2'): 2, ('pagerank', 'd2'): 1, ('categor', 'd2'): 2, ('cluster', 'd2'): 2, ('modelsppt', 'd2'): 2, ('question', 'd2'): 1, ('answer', 'd2'): 1, ('thanksgiv', 'd2'): 1, ('final', 'd2'): 1, ('exam', 'd2'): 1, ('amam', 'd2'): 1, ('depart', 'd2'): 1, ('scienc', 'd2'): 1, ('room', 'd2'): 1, ('tn', 'd2'): 1, ('phone', 'd2'): 1, ('fax', 'd2'): 1, ('maintain', 'd2'): 1, ('inform', 'd4'): 17, ('retriev', 'd4'): 11, ('institut', 'd4'): 1, ('intellig', 'd4'): 2, ('systemsth', 'd4'): 1, ('univers', 'd4'): 4, ('memphi', 'd4'): 3, ('web', 'd4'): 11, ('search', 'd4'): 12, ('prof', 'd4'): 3, ('vasil', 'd4'): 2, ('ru', 'd4'): 2, ('comppsyc', 'd4'): 1, ('fall', 'd4'): 2, ('announc', 'd4'): 3, ('schedul', 'd4'): 4, ('assign', 'd4'): 20, ('due', 'd4'): 3, ('oct', 'd4'): 1, ('open', 'd4'): 2, ('check', 'd4'): 2, ('tabl', 'd4'): 2, ('sept', 'd4'): 3, ('enrol', 'd4'): 1, ('level', 'd4'): 1, ('section', 'd4'): 1, ('phd', 'd4'): 1, ('student', 'd4'): 7, ('send', 'd4'): 1, ('topic', 'd4'): 2, ('present', 'd4'): 3, ('syllabu', 'd4'): 1, ('address', 'd4'): 1, ('major', 'd4'): 3, ('problem', 'd4'): 4, ('time', 'd4'): 1, ('today', 'd4'): 1, ('lack', 'd4'): 1, ('way', 'd4'): 1, ('organ', 'd4'): 1, ('vast', 'd4'): 1, ('amount', 'd4'): 1, ('fingertip', 'd4'): 1, ('effect', 'd4'): 1, ('face', 'd4'): 1, ('overload', 'd4'): 1, ('class', 'd4'): 3, ('challeng', 'd4'): 2, ('pose', 'd4'): 1, ('solut', 'd4'): 2, ('introduc', 'd4'): 1, ('comput', 'd4'): 2, ('techniqu', 'd4'): 2, ('static', 'd4'): 1, ('collect', 'd4'): 2, ('document', 'd4'): 2, ('dynam', 'd4'): 1, ('expos', 'd4'): 1, ('text', 'd4'): 7, ('process', 'd4'): 3, ('algorithm', 'd4'): 1, ('classic', 'd4'): 1, ('model', 'd4'): 5, ('boolean', 'd4'): 1, ('vectori', 'd4'): 1, ('close', 'd4'): 1, ('relat', 'd4'): 2, ('natur', 'd4'): 2, ('languag', 'd4'): 3, ('catalog', 'd4'): 1, ('entri', 'd4'): 1, ('advanc', 'd4'): 3, ('current', 'd4'): 1, ('research', 'd4'): 1, ('databas', 'd4'): 1, ('manag', 'd4'): 1, ('emphasi', 'd4'): 1, ('nontradit', 'd4'): 1, ('data', 'd4'): 1, ('applic', 'd4'): 1, ('prerequisit', 'd4'): 1, ('comp', 'd4'): 1, ('permiss', 'd4'): 1, ('instructor', 'd4'): 3, ('lectur', 'd4'): 7, ('tth', 'd4'): 2, ('ampm', 'd4'): 1, ('fogelman', 'd4'): 1, ('classroom', 'd4'): 1, ('build', 'd4'): 1, ('ta', 'd4'): 3, ('shrestha', 'd4'): 2, ('bidhya', 'd4'): 2, ('bshrsthamemphisedu', 'd4'): 1, ('offic', 'd4'): 2, ('hour', 'd4'): 1, ('ppm', 'd4'): 1, ('appt', 'd4'): 1, ('dh', 'd4'): 1, ('mw', 'd4'): 1, ('pm', 'd4'): 1, ('dunn', 'd4'): 2, ('hall', 'd4'): 2, ('page', 'd4'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd4'): 1, ('textbook', 'd4'): 2, ('baezay', 'd4'): 1, ('ribeironeto', 'd4'): 1, ('modern', 'd4'): 1, ('requir', 'd4'): 2, ('man', 'd4'): 1, ('raghavan', 'd4'): 1, ('schutz', 'd4'): 1, ('introduct', 'd4'): 5, ('recommend', 'd4'): 3, ('polici', 'd4'): 2, ('grade', 'd4'): 4, ('midterm', 'd4'): 2, ('quiz', 'd4'): 1, ('participationinteractionpresent', 'd4'): 1, ('submiss', 'd4'): 1, ('late', 'd4'): 1, ('plagiar', 'd4'): 4, ('intellectu', 'd4'): 1, ('engag', 'd4'): 1, ('read', 'd4'): 2, ('gener', 'd4'): 1, ('correct', 'd4'): 1, ('robust', 'd4'): 1, ('qualiti', 'd4'): 1, ('style', 'd4'): 2, ('written', 'd4'): 1, ('code', 'd4'): 4, ('shoud', 'd4'): 1, ('follow', 'd4'): 1, ('standard', 'd4'): 2, ('plagiarismch', 'd4'): 1, ('cheat', 'd4'): 2, ('behavior', 'd4'): 1, ('form', 'd4'): 1, ('uneth', 'd4'): 1, ('detriment', 'd4'): 1, ('proper', 'd4'): 2, ('educ', 'd4'): 1, ('toler', 'd4'): 1, ('work', 'd4'): 4, ('submit', 'd4'): 1, ('project', 'd4'): 2, ('program', 'd4'): 1, ('lab', 'd4'): 1, ('quizz', 'd4'): 1, ('test', 'd4'): 1, ('expect', 'd4'): 1, ('incur', 'd4'): 1, ('part', 'd4'): 1, ('pass', 'd4'): 1, ('credit', 'd4'): 1, ('list', 'd4'): 1, ('sourc', 'd4'): 2, ('reader', 'd4'): 1, ('led', 'd4'): 1, ('effort', 'd4'): 1, ('allow', 'd4'): 1, ('encourag', 'd4'): 1, ('discuss', 'd4'): 1, ('resourc', 'd4'): 1, ('literatur', 'd4'): 1, ('includ', 'd4'): 3, ('internet', 'd4'): 1, ('refer', 'd4'): 2, ('materi', 'd4'): 4, ('consult', 'd4'): 1, ('citat', 'd4'): 1, ('made', 'd4'): 1, ('verbatim', 'd4'): 1, ('occur', 'd4'): 1, ('receiv', 'd4'): 1, ('fail', 'd4'): 2, ('discret', 'd4'): 1, ('courseth', 'd4'): 1, ('decid', 'd4'): 1, ('forward', 'd4'): 1, ('incid', 'd4'): 1, ('judici', 'd4'): 1, ('affair', 'd4'): 1, ('disciplinari', 'd4'): 1, ('action', 'd4'): 1, ('conduct', 'd4'): 1, ('academ', 'd4'): 1, ('disciplin', 'd4'): 1, ('procedur', 'd4'): 1, ('httpwwwpeoplememphisedujaffair', 'd4'): 1, ('tent', 'd4'): 1, ('find', 'd4'): 1, ('compil', 'd4'): 1, ('person', 'd4'): 1, ('note', 'd4'): 1, ('famou', 'd4'): 1, ('primarili', 'd4'): 1, ('ut', 'd4'): 1, ('austin', 'd4'): 1, ('dr', 'd4'): 2, ('ray', 'd4'): 1, ('mooney', 'd4'): 1, ('unt', 'd4'): 1, ('rada', 'd4'): 1, ('mihalcea', 'd4'): 1, ('week', 'd4'): 17, ('half', 'd4'): 2, ('ppt', 'd4'): 23, ('chapter', 'd4'): 8, ('perl', 'd4'): 3, ('tutori', 'd4'): 1, ('ir', 'd4'): 5, ('evalu', 'd4'): 2, ('queri', 'd4'): 2, ('oper', 'd4'): 2, ('properti', 'd4'): 1, ('index', 'd4'): 1, ('break', 'd4'): 1, ('intro', 'd4'): 2, ('review', 'd4'): 3, ('porter', 'd4'): 2, ('stemmer', 'd4'): 2, ('slide', 'd4'): 1, ('mapreduc', 'd4'): 1, ('paper', 'd4'): 2, ('pagerank', 'd4'): 1, ('categor', 'd4'): 2, ('cluster', 'd4'): 2, ('modelsppt', 'd4'): 2, ('question', 'd4'): 1, ('answer', 'd4'): 1, ('thanksgiv', 'd4'): 1, ('final', 'd4'): 1, ('exam', 'd4'): 1, ('amam', 'd4'): 1, ('depart', 'd4'): 1, ('scienc', 'd4'): 1, ('room', 'd4'): 1, ('tn', 'd4'): 1, ('phone', 'd4'): 1, ('fax', 'd4'): 1, ('maintain', 'd4'): 1, ('porter', 'd5'): 14, ('stem', 'd5'): 18, ('algorithm', 'd5'): 20, ('page', 'd5'): 3, ('complet', 'd5'): 2, ('revis', 'd5'): 2, ('jan', 'd5'): 6, ('earlier', 'd5'): 1, ('edit', 'd5'): 1, ('offici', 'd5'): 2, ('home', 'd5'): 1, ('distribut', 'd5'): 5, ('written', 'd5'): 5, ('maintain', 'd5'): 1, ('author', 'd5'): 6, ('martin', 'd5'): 4, ('stemmer', 'd5'): 9, ('process', 'd5'): 2, ('remov', 'd5'): 5, ('common', 'd5'): 3, ('morpholog', 'd5'): 1, ('inflexion', 'd5'): 1, ('end', 'd5'): 3, ('word', 'd5'): 7, ('english', 'd5'): 2, ('main', 'd5'): 1, ('part', 'd5'): 2, ('term', 'd5'): 1, ('normalis', 'd5'): 1, ('set', 'd5'): 4, ('inform', 'd5'): 3, ('retriev', 'd5'): 3, ('system', 'd5'): 1, ('histori', 'd5'): 1, ('origin', 'd5'): 5, ('paper', 'd5'): 4, ('comput', 'd5'): 1, ('laboratori', 'd5'): 1, ('cambridg', 'd5'): 1, ('england', 'd5'): 1, ('larger', 'd5'): 1, ('ir', 'd5'): 3, ('project', 'd5'): 2, ('appear', 'd5'): 1, ('chapter', 'd5'): 1, ('final', 'd5'): 4, ('report', 'd5'): 2, ('cj', 'd5'): 1, ('van', 'd5'): 3, ('rijsbergen', 'd5'): 2, ('se', 'd5'): 1, ('robertson', 'd5'): 1, ('mf', 'd5'): 2, ('model', 'd5'): 1, ('probabilist', 'd5'): 1, ('london', 'd5'): 1, ('british', 'd5'): 2, ('librari', 'd5'): 2, ('research', 'd5'): 3, ('develop', 'd5'): 1, ('encourag', 'd5'): 1, ('publish', 'd5'): 6, ('suffix', 'd5'): 4, ('strip', 'd5'): 1, ('program', 'd5'): 5, ('pp', 'd5'): 1, ('reprint', 'd5'): 1, ('karen', 'd5'): 1, ('sparck', 'd5'): 1, ('jone', 'd5'): 1, ('peter', 'd5'): 1, ('willet', 'd5'): 1, ('read', 'd5'): 1, ('san', 'd5'): 1, ('francisco', 'd5'): 1, ('morgan', 'd5'): 1, ('kaufmann', 'd5'): 1, ('isbn', 'd5'): 1, ('bcpl', 'd5'): 4, ('languag', 'd5'): 3, ('popular', 'd5'): 2, ('defunct', 'd5'): 1, ('year', 'd5'): 2, ('form', 'd5'): 4, ('medium', 'd5'): 1, ('punch', 'd5'): 1, ('tape', 'd5'): 1, ('version', 'd5'): 9, ('began', 'd5'): 1, ('wide', 'd5'): 1, ('quot', 'd5'): 1, ('adapt', 'd5'): 1, ('numer', 'd5'): 1, ('variat', 'd5'): 2, ('function', 'd5'): 1, ('web', 'd5'): 2, ('primarili', 'd5'): 1, ('put', 'd5'): 1, ('record', 'd5'): 1, ('straight', 'd5'): 1, ('establish', 'd5'): 1, ('definit', 'd5'): 3, ('encod', 'd5'): 8, ('ansi', 'd5'): 5, ('head', 'd5'): 2, ('tabl', 'd5'): 1, ('equival', 'd5'): 1, ('differ', 'd5'): 4, ('minor', 'd5'): 1, ('point', 'd5'): 2, ('mark', 'd5'): 1, ('download', 'd5'): 1, ('discuss', 'd5'): 1, ('regard', 'd5'): 2, ('act', 'd5'): 1, ('receiv', 'd5'): 2, ('worker', 'd5'): 1, ('present', 'd5'): 3, ('reason', 'd5'): 1, ('confid', 'd5'): 1, ('correctli', 'd5'): 1, ('affili', 'd5'): 1, ('note', 'd5'): 4, ('thread', 'd5'): 1, ('safe', 'd5'): 1, ('java', 'd5'): 1, ('perl', 'd5'): 2, ('daniel', 'd5'): 2, ('balen', 'd5'): 1, ('oct', 'd5'): 4, ('slightli', 'd5'): 2, ('faster', 'd5'): 1, ('python', 'd5'): 1, ('vivak', 'd5'): 1, ('gupta', 'd5'): 1, ('csharp', 'd5'): 4, ('andré', 'd5'): 1, ('hazelwood', 'd5'): 1, ('guid', 'd5'): 1, ('sep', 'd5'): 4, ('net', 'd5'): 2, ('compliant', 'd5'): 2, ('leif', 'd5'): 1, ('azzopardi', 'd5'): 1, ('univer', 'd5'): 1, ('paisley', 'd5'): 1, ('scotland', 'd5'): 1, ('nov', 'd5'): 4, ('brad', 'd5'): 2, ('patton', 'd5'): 1, ('ratborgblogspotcom', 'd5'): 1, ('dec', 'd5'): 1, ('standard', 'd5'): 2, ('code', 'd5'): 1, ('frank', 'd5'): 2, ('kolnick', 'd5'): 1, ('compact', 'd5'): 1, ('simplifi', 'd5'): 1, ('lisp', 'd5'): 1, ('steven', 'd5'): 1, ('haflich', 'd5'): 1, ('franz', 'd5'): 1, ('mar', 'd5'): 2, ('rubi', 'd5'): 1, ('ray', 'd5'): 1, ('pereda', 'd5'): 1, ('wwwrayperedacom', 'd5'): 1, ('github', 'd5'): 10, ('link', 'd5'): 12, ('visual', 'd5'): 2, ('basic', 'd5'): 1, ('vb', 'd5'): 1, ('navonil', 'd5'): 1, ('mustafe', 'd5'): 1, ('brunel', 'd5'): 1, ('univers', 'd5'): 5, ('apr', 'd5'): 5, ('delphi', 'd5'): 1, ('jo', 'd5'): 1, ('rabin', 'd5'): 1, ('javascript', 'd5'): 1, ('andargor', 'd5'): 1, ('wwwandargorcom', 'd5'): 1, ('jul', 'd5'): 3, ('substanti', 'd5'): 1, ('bychristoph', 'd5'): 1, ('mckenzi', 'd5'): 1, ('basicvb', 'd5'): 1, ('christo', 'd5'): 1, ('attiko', 'd5'): 1, ('piraeu', 'd5'): 1, ('greec', 'd5'): 1, ('php', 'd5'): 1, ('richard', 'd5'): 2, ('hey', 'd5'): 1, ('wwwphpguruorg', 'd5'): 1, ('feb', 'd5'): 3, ('prolog', 'd5'): 1, ('philip', 'd5'): 1, ('brook', 'd5'): 1, ('georgia', 'd5'): 1, ('haskel', 'd5'): 1, ('dmitri', 'd5'): 1, ('antonyuk', 'd5'): 1, ('tsql', 'd5'): 1, ('keith', 'd5'): 1, ('lubel', 'd5'): 1, ('wwwatelierdevitrauxcom', 'd5'): 1, ('matlab', 'd5'): 1, ('juan', 'd5'): 1, ('carlo', 'd5'): 1, ('lopez', 'd5'): 1, ('california', 'd5'): 1, ('pacif', 'd5'): 1, ('medic', 'd5'): 1, ('centerresearch', 'd5'): 1, ('institut', 'd5'): 3, ('tcl', 'd5'): 1, ('ari', 'd5'): 1, ('theodorako', 'd5'): 1, ('ncsr', 'd5'): 1, ('demokrito', 'd5'): 1, ('truemper', 'd5'): 1, ('humboldtuniversitaet', 'd5'): 1, ('zu', 'd5'): 1, ('berlin', 'd5'): 1, ('erlang', 'd5'): 2, ('alden', 'd5'): 1, ('dima', 'd5'): 1, ('nation', 'd5'): 1, ('andtechnolog', 'd5'): 1, ('gaithersburg', 'd5'): 1, ('md', 'd5'): 1, ('usa', 'd5'): 1, ('rebol', 'd5'): 1, ('dale', 'd5'): 1, ('brearcliff', 'd5'): 1, ('scala', 'd5'): 1, ('ken', 'd5'): 1, ('faulkner', 'd5'): 1, ('sa', 'd5'): 1, ('antoin', 'd5'): 1, ('stpierr', 'd5'): 1, ('busi', 'd5'): 1, ('plugin', 'd5'): 1, ('vim', 'd5'): 1, ('script', 'd5'): 1, ('mitchel', 'd5'): 1, ('bowden', 'd5'): 1, ('nodej', 'd5'): 1, ('jed', 'd5'): 1, ('parson', 'd5'): 1, ('jedparsonscom', 'd5'): 1, ('googl', 'd5'): 1, ('alex', 'd5'): 1, ('gonopolskiy', 'd5'): 1, ('awk', 'd5'): 1, ('gregori', 'd5'): 1, ('grefenstett', 'd5'): 1, ('dscomexalead', 'd5'): 1, ('clojur', 'd5'): 1, ('yushi', 'd5'): 1, ('wang', 'd5'): 1, ('bitbucket', 'd5'): 1, ('rust', 'd5'): 1, ('nhat', 'd5'): 1, ('minh', 'd5'): 1, ('nanyang', 'd5'): 1, ('technolog', 'd5'): 2, ('aug', 'd5'): 1, ('vala', 'd5'): 1, ('serg', 'd5'): 1, ('huln', 'd5'): 1, ('mysql', 'd5'): 1, ('john', 'd5'): 1, ('carti', 'd5'): 1, ('enlighten', 'd5'): 1, ('job', 'd5'): 1, ('julia', 'd5'): 1, ('matãa', 'd5'): 1, ('guzmãn', 'd5'): 1, ('naranjo', 'd5'): 1, ('flex', 'd5'): 1, ('zalãn', 'd5'): 1, ('bodã³', 'd5'): 1, ('babesbolyai', 'd5'): 1, ('zalan', 'd5'): 1, ('mohit', 'd5'): 1, ('makkar', 'd5'): 1, ('indian', 'd5'): 1, ('delhi', 'd5'): 1, ('groovi', 'd5'): 1, ('dhaval', 'd5'): 1, ('dave', 'd5'): 1, ('jun', 'd5'): 1, ('oorexx', 'd5'): 1, ('po', 'd5'): 1, ('jonsson', 'd5'): 1, ('sourceforg', 'd5'): 1, ('xslt', 'd5'): 1, ('joey', 'd5'): 1, ('takeda', 'd5'): 1, ('lpa', 'd5'): 1, ('winprolog', 'd5'): 1, ('brian', 'd5'): 1, ('steel', 'd5'): 1, ('solanumorg', 'd5'): 1, ('gnu', 'd5'): 1, ('pspp', 'd5'): 1, ('fran', 'd5'): 1, ('houwel', 'd5'): 1, ('typescript', 'd5'): 1, ('max', 'd5'): 1, ('patiiuk', 'd5'): 1, ('free', 'd5'): 3, ('charg', 'd5'): 2, ('purpos', 'd5'): 4, ('question', 'd5'): 4, ('direct', 'd5'): 1, ('test', 'd5'): 3, ('sampl', 'd5'): 1, ('vocabulari', 'd5'): 1, ('megabyt', 'd5'): 1, ('output', 'd5'): 1, ('email', 'd5'): 1, ('comment', 'd5'): 1, ('suggest', 'd5'): 2, ('queri', 'd5'): 1, ('extra', 'd5'): 1, ('rule', 'd5'): 11, ('step', 'd5'): 4, ('logi', 'd5'): 1, ('log', 'd5'): 1, ('archaeolog', 'd5'): 2, ('equat', 'd5'): 2, ('abli', 'd5'): 1, ('replac', 'd5'): 2, ('bli', 'd5'): 1, ('ble', 'd5'): 1, ('possibl', 'd5'): 1, ('leav', 'd5'): 4, ('string', 'd5'): 4, ('length', 'd5'): 3, ('case', 'd5'): 4, ('unchang', 'd5'): 1, ('pass', 'd5'): 1, ('lose', 'd5'): 1, ('deriv', 'd5'): 2, ('great', 'd5'): 1, ('distanc', 'd5'): 1, ('public', 'd5'): 1, ('difficult', 'd5'): 1, ('emphasis', 'd5'): 1, ('small', 'd5'): 2, ('compar', 'd5'): 1, ('observ', 'd5'): 1, ('statu', 'd5'): 1, ('frozen', 'd5'): 1, ('strictli', 'd5'): 1, ('defin', 'd5'): 1, ('amen', 'd5'): 1, ('modif', 'd5'): 1, ('inferior', 'd5'): 1, ('snowbal', 'd5'): 3, ('subject', 'd5'): 1, ('occasion', 'd5'): 2, ('improv', 'd5'): 3, ('practic', 'd5'): 1, ('work', 'd5'): 2, ('recommend', 'd5'): 1, ('involv', 'd5'): 1, ('experi', 'd5'): 1, ('repeat', 'd5'): 1, ('error', 'd5'): 6, ('histor', 'd5'): 1, ('shortcom', 'd5'): 1, ('found', 'd5'): 1, ('explain', 'd5'): 3, ('type', 'd5'): 1, ('condit', 'd5'): 1, ('appli', 'd5'): 3, ('longest', 'd5'): 2, ('match', 'd5'): 2, ('true', 'd5'): 1, ('succe', 'd5'): 2, ('fail', 'd5'): 2, ('simpli', 'd5'): 1, ('turn', 'd5'): 2, ('list', 'd5'): 1, ('run', 'd5'): 1, ('lead', 'd5'): 1, ('place', 'd5'): 1, ('mement', 'd5'): 1, ('mment', 'd5'): 1, ('ment', 'd5'): 4, ('ement', 'd5'): 1, ('ent', 'd5'): 3, ('properli', 'd5'): 1, ('argument', 'd5'): 2, ('argu', 'd5'): 1, ('measur', 'd5'): 4, ('equal', 'd5'): 2, ('argum', 'd5'): 1, ('delic', 'd5'): 1, ('liabl', 'd5'): 1, ('misinterpret', 'd5'): 1, ('greater', 'd5'): 3, ('care', 'd5'): 1, ('requir', 'd5'): 1, ('tion', 'd5'): 3, ('ms', 'd5'): 1, ('mean', 'd5'): 2, ('take', 'd5'): 3, ('ion', 'd5'): 1, ('sion', 'd5'): 1, ('similar', 'd5'): 2, ('confus', 'd5'): 1, ('aris', 'd5'): 1, ('interpret', 'd5'): 1, ('reduc', 'd5'): 1, ('doubl', 'd5'): 1, ('singl', 'd5'): 1, ('cruder', 'd5'): 1, ('conson', 'd5'): 1, ('vowel', 'd5'): 1, ('wrong', 'd5'): 1, ('round', 'd5'): 1, ('interest', 'd5'): 1, ('switch', 'd5'): 1, ('letter', 'd5'): 1, ('techniqu', 'd5'): 1, ('make', 'd5'): 2, ('slower', 'd5'): 1, ('faq', 'd5'): 1, ('frequent', 'd5'): 1, ('ask', 'd5'): 3, ('licens', 'd5'): 5, ('arrang', 'd5'): 2, ('softwar', 'd5'): 6, ('recent', 'd5'): 1, ('period', 'd5'): 1, ('clear', 'd5'): 1, ('statment', 'd5'): 1, ('problem', 'd5'): 1, ('intellectu', 'd5'): 1, ('properti', 'd5'): 1, ('major', 'd5'): 1, ('issu', 'd5'): 2, ('formal', 'd5'): 1, ('statement', 'd5'): 1, ('expect', 'd5'): 2, ('restat', 'd5'): 1, ('text', 'd5'): 1, ('rare', 'd5'): 1, ('restrict', 'd5'): 1, ('bsd', 'd5'): 2, ('endors', 'd5'): 1, ('contributor', 'd5'): 3, ('unnecessari', 'd5'): 1, ('confirm', 'd5'): 1, ('employ', 'd5'): 2, ('proof', 'd5'): 2, ('websit', 'd5'): 1, ('posit', 'd5'): 1, ('simpler', 'd5'): 1, ('contribut', 'd5'): 1, ('boulton', 'd5'): 1, ('right', 'd5'): 1, ('produc', 'd5'): 1, ('proper', 'd5'): 1, ('crude', 'd5'): 1, ('real', 'd5'): 1, ('bring', 'd5'): 1, ('variant', 'd5'): 1, ('map', 'd5'): 1, ('paradigm', 'd5'): 1, ('connect', 'd5'): 1, ('import', 'd5'): 1, ('rememb', 'd5'): 1, ('achiev', 'd5'): 1, ('perfect', 'd5'): 1, ('balanc', 'd5'): 1, ('perform', 'd5'): 2, ('individu', 'd5'): 1, ('matter', 'd5'): 1, ('addit', 'd5'): 1, ('includ', 'd5'): 1, ('file', 'd6'): 1, ('found', 'd6'): 1, ('relationship', 'd7'): 1, ('secretari', 'd9'): 1, ('transport', 'd9'): 1, ('pete', 'd9'): 1, ('buttigieg', 'd9'): 1, ('candid', 'd9'): 1, ('recent', 'd9'): 1, ('visit', 'd9'): 1, ('late', 'd9'): 1, ('show', 'd9'): 1, ('stephen', 'd9'): 1, ('colbert', 'd9'): 1, ('speaker', 'd9'): 2, ('mike', 'd9'): 1, ('johnson', 'd9'): 2, ('unknown', 'd9'): 1, ('republican', 'd9'): 1, ('louisiana', 'd9'): 1, ('lawmak', 'd9'): 1, ('elect', 'd9'): 1, ('california', 'd9'): 1, ('rep', 'd9'): 1, ('kevin', 'd9'): 1, ('mccarthi', 'd9'): 1, ('oust', 'd9'): 1, ('doubl', 'd9'): 1, ('highlight', 'd9'): 1, ('extrem', 'd9'): 1, ('view', 'd9'): 1, ('appear', 'd9'): 1, ('cnn', 'd9'): 1, ('friday', 'd9'): 1, ('dont', 'd11'): 1, ('realiz', 'd11'): 1, ('power', 'd11'): 1, ('white', 'd11'): 1, ('christian', 'd11'): 1, ('evangel', 'd11'): 1, ('taylor', 'd12'): 1, ('swift', 'd12'): 1, ('absent', 'd12'): 1, ('kansa', 'd12'): 1, ('citi', 'd12'): 1, ('chief', 'd12'): 1, ('game', 'd12'): 1, ('germani', 'd12'): 1, ('morn', 'd12'): 1, ('fan', 'd12'): 1, ('mock', 'd12'): 1, ('travi', 'd12'): 1, ('kelc', 'd12'): 1, ('perform', 'd12'): 1, ('month', 'd13'): 1, ('quietli', 'd13'): 1, ('signal', 'd13'): 1, ('support', 'd13'): 1, ('ron', 'd13'): 1, ('desanti', 'd13'): 1, ('iowa', 'd13'): 1, ('gov', 'd13'): 1, ('kim', 'd13'): 1, ('reynold', 'd13'): 1, ('formal', 'd13'): 1, ('endors', 'd13'): 1, ('florida', 'd13'): 1, ('governor', 'd13'): 1, ('presid', 'd13'): 1, ('de', 'd13'): 2, ('moin', 'd13'): 2, ('ralli', 'd13'): 1, ('monday', 'd13'): 1, ('sourc', 'd13'): 1, ('close', 'd13'): 1, ('confirm', 'd13'): 1, ('regist', 'd13'): 1, ('purchas', 'd14'): 1, ('independ', 'd14'): 1, ('review', 'd14'): 1, ('product', 'd14'): 1, ('servic', 'd14'): 1, ('link', 'd14'): 1, ('websit', 'd14'): 1, ('sheknow', 'd14'): 1, ('receiv', 'd14'): 1, ('affili', 'd14'): 1, ('commiss', 'd14'): 1, ('sylvest', 'd15'): 1, ('stallon', 'd15'): 1, ('reflect', 'd15'): 1, ('relationship', 'd15'): 1, ('late', 'd15'): 1, ('son', 'd15'): 1, ('netflix', 'd15'): 1, ('documentari', 'd15'): 1, ('sli', 'd15'): 1, ('roseann', 'd16'): 1, ('barr', 'd16'): 1, ('call', 'd16'): 1, ('fan', 'd16'): 1, ('refer', 'd16'): 1, ('presid', 'd16'): 3, ('donald', 'd16'): 1, ('trump', 'd16'): 1, ('twiceelect', 'd16'): 1, ('elect', 'd16'): 1}



```python
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

def get_inverted_indices(preprocessed_text):
    # Creating a dictionary with document identifiers (d1, d2, etc.) as keys
    preprocessed_text_dict = {'d' + str(i): preprocessed_text[i] for i in range(len(preprocessed_text))}
    inverted_indices_dict = {}

    # Iterating over each document and its associated text
    for document in preprocessed_text_dict:
        text = preprocessed_text_dict[document]
        tokens = text.strip().split()

        # Building the inverted index
        for token in tokens:
            try:
                inverted_indices_dict[(token, document)] += 1
            except KeyError:
                inverted_indices_dict[(token, document)] = 1

    return inverted_indices_dict

if __name__ == '__main__':
    # Load preprocessed text from file
    with open('preprocessed_text', 'rb') as handle:
        preprocessed_text = pickle.load(handle)

    # Generate inverted indices
    inverted_indices_dict = get_inverted_indices(preprocessed_text)
    print('Inverted Indices Dictionary: ', inverted_indices_dict)

    # Save the inverted indices dictionary for future use
    with open('inverted_indices', 'wb') as handle:
        pickle.dump(inverted_indices_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

```

    Inverted Indices Dictionary:  {('inform', 'd0'): 17, ('retriev', 'd0'): 11, ('institut', 'd0'): 1, ('intellig', 'd0'): 2, ('systemsth', 'd0'): 1, ('univers', 'd0'): 4, ('memphi', 'd0'): 3, ('web', 'd0'): 11, ('search', 'd0'): 12, ('prof', 'd0'): 3, ('vasil', 'd0'): 2, ('ru', 'd0'): 2, ('comppsyc', 'd0'): 1, ('fall', 'd0'): 2, ('announc', 'd0'): 3, ('schedul', 'd0'): 4, ('assign', 'd0'): 20, ('due', 'd0'): 3, ('oct', 'd0'): 1, ('open', 'd0'): 2, ('check', 'd0'): 2, ('tabl', 'd0'): 2, ('sept', 'd0'): 3, ('enrol', 'd0'): 1, ('level', 'd0'): 1, ('section', 'd0'): 1, ('phd', 'd0'): 1, ('student', 'd0'): 7, ('send', 'd0'): 1, ('topic', 'd0'): 2, ('present', 'd0'): 3, ('syllabu', 'd0'): 1, ('address', 'd0'): 1, ('major', 'd0'): 3, ('problem', 'd0'): 4, ('time', 'd0'): 1, ('today', 'd0'): 1, ('lack', 'd0'): 1, ('way', 'd0'): 1, ('organ', 'd0'): 1, ('vast', 'd0'): 1, ('amount', 'd0'): 1, ('fingertip', 'd0'): 1, ('effect', 'd0'): 1, ('face', 'd0'): 1, ('overload', 'd0'): 1, ('class', 'd0'): 3, ('challeng', 'd0'): 2, ('pose', 'd0'): 1, ('solut', 'd0'): 2, ('introduc', 'd0'): 1, ('comput', 'd0'): 2, ('techniqu', 'd0'): 2, ('static', 'd0'): 1, ('collect', 'd0'): 2, ('document', 'd0'): 2, ('dynam', 'd0'): 1, ('expos', 'd0'): 1, ('text', 'd0'): 7, ('process', 'd0'): 3, ('algorithm', 'd0'): 1, ('classic', 'd0'): 1, ('model', 'd0'): 5, ('boolean', 'd0'): 1, ('vectori', 'd0'): 1, ('close', 'd0'): 1, ('relat', 'd0'): 2, ('natur', 'd0'): 2, ('languag', 'd0'): 3, ('catalog', 'd0'): 1, ('entri', 'd0'): 1, ('advanc', 'd0'): 3, ('current', 'd0'): 1, ('research', 'd0'): 1, ('databas', 'd0'): 1, ('manag', 'd0'): 1, ('emphasi', 'd0'): 1, ('nontradit', 'd0'): 1, ('data', 'd0'): 1, ('applic', 'd0'): 1, ('prerequisit', 'd0'): 1, ('comp', 'd0'): 1, ('permiss', 'd0'): 1, ('instructor', 'd0'): 3, ('lectur', 'd0'): 7, ('tth', 'd0'): 2, ('ampm', 'd0'): 1, ('fogelman', 'd0'): 1, ('classroom', 'd0'): 1, ('build', 'd0'): 1, ('ta', 'd0'): 3, ('shrestha', 'd0'): 2, ('bidhya', 'd0'): 2, ('bshrsthamemphisedu', 'd0'): 1, ('offic', 'd0'): 2, ('hour', 'd0'): 1, ('ppm', 'd0'): 1, ('appt', 'd0'): 1, ('dh', 'd0'): 1, ('mw', 'd0'): 1, ('pm', 'd0'): 1, ('dunn', 'd0'): 2, ('hall', 'd0'): 2, ('page', 'd0'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd0'): 1, ('textbook', 'd0'): 2, ('baezay', 'd0'): 1, ('ribeironeto', 'd0'): 1, ('modern', 'd0'): 1, ('requir', 'd0'): 2, ('man', 'd0'): 1, ('raghavan', 'd0'): 1, ('schutz', 'd0'): 1, ('introduct', 'd0'): 5, ('recommend', 'd0'): 3, ('polici', 'd0'): 2, ('grade', 'd0'): 4, ('midterm', 'd0'): 2, ('quiz', 'd0'): 1, ('participationinteractionpresent', 'd0'): 1, ('submiss', 'd0'): 1, ('late', 'd0'): 1, ('plagiar', 'd0'): 4, ('intellectu', 'd0'): 1, ('engag', 'd0'): 1, ('read', 'd0'): 2, ('gener', 'd0'): 1, ('correct', 'd0'): 1, ('robust', 'd0'): 1, ('qualiti', 'd0'): 1, ('style', 'd0'): 2, ('written', 'd0'): 1, ('code', 'd0'): 4, ('shoud', 'd0'): 1, ('follow', 'd0'): 1, ('standard', 'd0'): 2, ('plagiarismch', 'd0'): 1, ('cheat', 'd0'): 2, ('behavior', 'd0'): 1, ('form', 'd0'): 1, ('uneth', 'd0'): 1, ('detriment', 'd0'): 1, ('proper', 'd0'): 2, ('educ', 'd0'): 1, ('toler', 'd0'): 1, ('work', 'd0'): 4, ('submit', 'd0'): 1, ('project', 'd0'): 2, ('program', 'd0'): 1, ('lab', 'd0'): 1, ('quizz', 'd0'): 1, ('test', 'd0'): 1, ('expect', 'd0'): 1, ('incur', 'd0'): 1, ('part', 'd0'): 1, ('pass', 'd0'): 1, ('credit', 'd0'): 1, ('list', 'd0'): 1, ('sourc', 'd0'): 2, ('reader', 'd0'): 1, ('led', 'd0'): 1, ('effort', 'd0'): 1, ('allow', 'd0'): 1, ('encourag', 'd0'): 1, ('discuss', 'd0'): 1, ('resourc', 'd0'): 1, ('literatur', 'd0'): 1, ('includ', 'd0'): 3, ('internet', 'd0'): 1, ('refer', 'd0'): 2, ('materi', 'd0'): 4, ('consult', 'd0'): 1, ('citat', 'd0'): 1, ('made', 'd0'): 1, ('verbatim', 'd0'): 1, ('occur', 'd0'): 1, ('receiv', 'd0'): 1, ('fail', 'd0'): 2, ('discret', 'd0'): 1, ('courseth', 'd0'): 1, ('decid', 'd0'): 1, ('forward', 'd0'): 1, ('incid', 'd0'): 1, ('judici', 'd0'): 1, ('affair', 'd0'): 1, ('disciplinari', 'd0'): 1, ('action', 'd0'): 1, ('conduct', 'd0'): 1, ('academ', 'd0'): 1, ('disciplin', 'd0'): 1, ('procedur', 'd0'): 1, ('httpwwwpeoplememphisedujaffair', 'd0'): 1, ('tent', 'd0'): 1, ('find', 'd0'): 1, ('compil', 'd0'): 1, ('person', 'd0'): 1, ('note', 'd0'): 1, ('famou', 'd0'): 1, ('primarili', 'd0'): 1, ('ut', 'd0'): 1, ('austin', 'd0'): 1, ('dr', 'd0'): 2, ('ray', 'd0'): 1, ('mooney', 'd0'): 1, ('unt', 'd0'): 1, ('rada', 'd0'): 1, ('mihalcea', 'd0'): 1, ('week', 'd0'): 17, ('half', 'd0'): 2, ('ppt', 'd0'): 23, ('chapter', 'd0'): 8, ('perl', 'd0'): 3, ('tutori', 'd0'): 1, ('ir', 'd0'): 5, ('evalu', 'd0'): 2, ('queri', 'd0'): 2, ('oper', 'd0'): 2, ('properti', 'd0'): 1, ('index', 'd0'): 1, ('break', 'd0'): 1, ('intro', 'd0'): 2, ('review', 'd0'): 3, ('porter', 'd0'): 2, ('stemmer', 'd0'): 2, ('slide', 'd0'): 1, ('mapreduc', 'd0'): 1, ('paper', 'd0'): 2, ('pagerank', 'd0'): 1, ('categor', 'd0'): 2, ('cluster', 'd0'): 2, ('modelsppt', 'd0'): 2, ('question', 'd0'): 1, ('answer', 'd0'): 1, ('thanksgiv', 'd0'): 1, ('final', 'd0'): 1, ('exam', 'd0'): 1, ('amam', 'd0'): 1, ('depart', 'd0'): 1, ('scienc', 'd0'): 1, ('room', 'd0'): 1, ('tn', 'd0'): 1, ('phone', 'd0'): 1, ('fax', 'd0'): 1, ('maintain', 'd0'): 1, ('inform', 'd1'): 17, ('retriev', 'd1'): 11, ('institut', 'd1'): 1, ('intellig', 'd1'): 2, ('systemsth', 'd1'): 1, ('univers', 'd1'): 4, ('memphi', 'd1'): 3, ('web', 'd1'): 11, ('search', 'd1'): 12, ('prof', 'd1'): 3, ('vasil', 'd1'): 2, ('ru', 'd1'): 2, ('comppsyc', 'd1'): 1, ('fall', 'd1'): 2, ('announc', 'd1'): 3, ('schedul', 'd1'): 4, ('assign', 'd1'): 20, ('due', 'd1'): 3, ('oct', 'd1'): 1, ('open', 'd1'): 2, ('check', 'd1'): 2, ('tabl', 'd1'): 2, ('sept', 'd1'): 3, ('enrol', 'd1'): 1, ('level', 'd1'): 1, ('section', 'd1'): 1, ('phd', 'd1'): 1, ('student', 'd1'): 7, ('send', 'd1'): 1, ('topic', 'd1'): 2, ('present', 'd1'): 3, ('syllabu', 'd1'): 1, ('address', 'd1'): 1, ('major', 'd1'): 3, ('problem', 'd1'): 4, ('time', 'd1'): 1, ('today', 'd1'): 1, ('lack', 'd1'): 1, ('way', 'd1'): 1, ('organ', 'd1'): 1, ('vast', 'd1'): 1, ('amount', 'd1'): 1, ('fingertip', 'd1'): 1, ('effect', 'd1'): 1, ('face', 'd1'): 1, ('overload', 'd1'): 1, ('class', 'd1'): 3, ('challeng', 'd1'): 2, ('pose', 'd1'): 1, ('solut', 'd1'): 2, ('introduc', 'd1'): 1, ('comput', 'd1'): 2, ('techniqu', 'd1'): 2, ('static', 'd1'): 1, ('collect', 'd1'): 2, ('document', 'd1'): 2, ('dynam', 'd1'): 1, ('expos', 'd1'): 1, ('text', 'd1'): 7, ('process', 'd1'): 3, ('algorithm', 'd1'): 1, ('classic', 'd1'): 1, ('model', 'd1'): 5, ('boolean', 'd1'): 1, ('vectori', 'd1'): 1, ('close', 'd1'): 1, ('relat', 'd1'): 2, ('natur', 'd1'): 2, ('languag', 'd1'): 3, ('catalog', 'd1'): 1, ('entri', 'd1'): 1, ('advanc', 'd1'): 3, ('current', 'd1'): 1, ('research', 'd1'): 1, ('databas', 'd1'): 1, ('manag', 'd1'): 1, ('emphasi', 'd1'): 1, ('nontradit', 'd1'): 1, ('data', 'd1'): 1, ('applic', 'd1'): 1, ('prerequisit', 'd1'): 1, ('comp', 'd1'): 1, ('permiss', 'd1'): 1, ('instructor', 'd1'): 3, ('lectur', 'd1'): 7, ('tth', 'd1'): 2, ('ampm', 'd1'): 1, ('fogelman', 'd1'): 1, ('classroom', 'd1'): 1, ('build', 'd1'): 1, ('ta', 'd1'): 3, ('shrestha', 'd1'): 2, ('bidhya', 'd1'): 2, ('bshrsthamemphisedu', 'd1'): 1, ('offic', 'd1'): 2, ('hour', 'd1'): 1, ('ppm', 'd1'): 1, ('appt', 'd1'): 1, ('dh', 'd1'): 1, ('mw', 'd1'): 1, ('pm', 'd1'): 1, ('dunn', 'd1'): 2, ('hall', 'd1'): 2, ('page', 'd1'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd1'): 1, ('textbook', 'd1'): 2, ('baezay', 'd1'): 1, ('ribeironeto', 'd1'): 1, ('modern', 'd1'): 1, ('requir', 'd1'): 2, ('man', 'd1'): 1, ('raghavan', 'd1'): 1, ('schutz', 'd1'): 1, ('introduct', 'd1'): 5, ('recommend', 'd1'): 3, ('polici', 'd1'): 2, ('grade', 'd1'): 4, ('midterm', 'd1'): 2, ('quiz', 'd1'): 1, ('participationinteractionpresent', 'd1'): 1, ('submiss', 'd1'): 1, ('late', 'd1'): 1, ('plagiar', 'd1'): 4, ('intellectu', 'd1'): 1, ('engag', 'd1'): 1, ('read', 'd1'): 2, ('gener', 'd1'): 1, ('correct', 'd1'): 1, ('robust', 'd1'): 1, ('qualiti', 'd1'): 1, ('style', 'd1'): 2, ('written', 'd1'): 1, ('code', 'd1'): 4, ('shoud', 'd1'): 1, ('follow', 'd1'): 1, ('standard', 'd1'): 2, ('plagiarismch', 'd1'): 1, ('cheat', 'd1'): 2, ('behavior', 'd1'): 1, ('form', 'd1'): 1, ('uneth', 'd1'): 1, ('detriment', 'd1'): 1, ('proper', 'd1'): 2, ('educ', 'd1'): 1, ('toler', 'd1'): 1, ('work', 'd1'): 4, ('submit', 'd1'): 1, ('project', 'd1'): 2, ('program', 'd1'): 1, ('lab', 'd1'): 1, ('quizz', 'd1'): 1, ('test', 'd1'): 1, ('expect', 'd1'): 1, ('incur', 'd1'): 1, ('part', 'd1'): 1, ('pass', 'd1'): 1, ('credit', 'd1'): 1, ('list', 'd1'): 1, ('sourc', 'd1'): 2, ('reader', 'd1'): 1, ('led', 'd1'): 1, ('effort', 'd1'): 1, ('allow', 'd1'): 1, ('encourag', 'd1'): 1, ('discuss', 'd1'): 1, ('resourc', 'd1'): 1, ('literatur', 'd1'): 1, ('includ', 'd1'): 3, ('internet', 'd1'): 1, ('refer', 'd1'): 2, ('materi', 'd1'): 4, ('consult', 'd1'): 1, ('citat', 'd1'): 1, ('made', 'd1'): 1, ('verbatim', 'd1'): 1, ('occur', 'd1'): 1, ('receiv', 'd1'): 1, ('fail', 'd1'): 2, ('discret', 'd1'): 1, ('courseth', 'd1'): 1, ('decid', 'd1'): 1, ('forward', 'd1'): 1, ('incid', 'd1'): 1, ('judici', 'd1'): 1, ('affair', 'd1'): 1, ('disciplinari', 'd1'): 1, ('action', 'd1'): 1, ('conduct', 'd1'): 1, ('academ', 'd1'): 1, ('disciplin', 'd1'): 1, ('procedur', 'd1'): 1, ('httpwwwpeoplememphisedujaffair', 'd1'): 1, ('tent', 'd1'): 1, ('find', 'd1'): 1, ('compil', 'd1'): 1, ('person', 'd1'): 1, ('note', 'd1'): 1, ('famou', 'd1'): 1, ('primarili', 'd1'): 1, ('ut', 'd1'): 1, ('austin', 'd1'): 1, ('dr', 'd1'): 2, ('ray', 'd1'): 1, ('mooney', 'd1'): 1, ('unt', 'd1'): 1, ('rada', 'd1'): 1, ('mihalcea', 'd1'): 1, ('week', 'd1'): 17, ('half', 'd1'): 2, ('ppt', 'd1'): 23, ('chapter', 'd1'): 8, ('perl', 'd1'): 3, ('tutori', 'd1'): 1, ('ir', 'd1'): 5, ('evalu', 'd1'): 2, ('queri', 'd1'): 2, ('oper', 'd1'): 2, ('properti', 'd1'): 1, ('index', 'd1'): 1, ('break', 'd1'): 1, ('intro', 'd1'): 2, ('review', 'd1'): 3, ('porter', 'd1'): 2, ('stemmer', 'd1'): 2, ('slide', 'd1'): 1, ('mapreduc', 'd1'): 1, ('paper', 'd1'): 2, ('pagerank', 'd1'): 1, ('categor', 'd1'): 2, ('cluster', 'd1'): 2, ('modelsppt', 'd1'): 2, ('question', 'd1'): 1, ('answer', 'd1'): 1, ('thanksgiv', 'd1'): 1, ('final', 'd1'): 1, ('exam', 'd1'): 1, ('amam', 'd1'): 1, ('depart', 'd1'): 1, ('scienc', 'd1'): 1, ('room', 'd1'): 1, ('tn', 'd1'): 1, ('phone', 'd1'): 1, ('fax', 'd1'): 1, ('maintain', 'd1'): 1, ('inform', 'd2'): 17, ('retriev', 'd2'): 11, ('institut', 'd2'): 1, ('intellig', 'd2'): 2, ('systemsth', 'd2'): 1, ('univers', 'd2'): 4, ('memphi', 'd2'): 3, ('web', 'd2'): 11, ('search', 'd2'): 12, ('prof', 'd2'): 3, ('vasil', 'd2'): 2, ('ru', 'd2'): 2, ('comppsyc', 'd2'): 1, ('fall', 'd2'): 2, ('announc', 'd2'): 3, ('schedul', 'd2'): 4, ('assign', 'd2'): 20, ('due', 'd2'): 3, ('oct', 'd2'): 1, ('open', 'd2'): 2, ('check', 'd2'): 2, ('tabl', 'd2'): 2, ('sept', 'd2'): 3, ('enrol', 'd2'): 1, ('level', 'd2'): 1, ('section', 'd2'): 1, ('phd', 'd2'): 1, ('student', 'd2'): 7, ('send', 'd2'): 1, ('topic', 'd2'): 2, ('present', 'd2'): 3, ('syllabu', 'd2'): 1, ('address', 'd2'): 1, ('major', 'd2'): 3, ('problem', 'd2'): 4, ('time', 'd2'): 1, ('today', 'd2'): 1, ('lack', 'd2'): 1, ('way', 'd2'): 1, ('organ', 'd2'): 1, ('vast', 'd2'): 1, ('amount', 'd2'): 1, ('fingertip', 'd2'): 1, ('effect', 'd2'): 1, ('face', 'd2'): 1, ('overload', 'd2'): 1, ('class', 'd2'): 3, ('challeng', 'd2'): 2, ('pose', 'd2'): 1, ('solut', 'd2'): 2, ('introduc', 'd2'): 1, ('comput', 'd2'): 2, ('techniqu', 'd2'): 2, ('static', 'd2'): 1, ('collect', 'd2'): 2, ('document', 'd2'): 2, ('dynam', 'd2'): 1, ('expos', 'd2'): 1, ('text', 'd2'): 7, ('process', 'd2'): 3, ('algorithm', 'd2'): 1, ('classic', 'd2'): 1, ('model', 'd2'): 5, ('boolean', 'd2'): 1, ('vectori', 'd2'): 1, ('close', 'd2'): 1, ('relat', 'd2'): 2, ('natur', 'd2'): 2, ('languag', 'd2'): 3, ('catalog', 'd2'): 1, ('entri', 'd2'): 1, ('advanc', 'd2'): 3, ('current', 'd2'): 1, ('research', 'd2'): 1, ('databas', 'd2'): 1, ('manag', 'd2'): 1, ('emphasi', 'd2'): 1, ('nontradit', 'd2'): 1, ('data', 'd2'): 1, ('applic', 'd2'): 1, ('prerequisit', 'd2'): 1, ('comp', 'd2'): 1, ('permiss', 'd2'): 1, ('instructor', 'd2'): 3, ('lectur', 'd2'): 7, ('tth', 'd2'): 2, ('ampm', 'd2'): 1, ('fogelman', 'd2'): 1, ('classroom', 'd2'): 1, ('build', 'd2'): 1, ('ta', 'd2'): 3, ('shrestha', 'd2'): 2, ('bidhya', 'd2'): 2, ('bshrsthamemphisedu', 'd2'): 1, ('offic', 'd2'): 2, ('hour', 'd2'): 1, ('ppm', 'd2'): 1, ('appt', 'd2'): 1, ('dh', 'd2'): 1, ('mw', 'd2'): 1, ('pm', 'd2'): 1, ('dunn', 'd2'): 2, ('hall', 'd2'): 2, ('page', 'd2'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd2'): 1, ('textbook', 'd2'): 2, ('baezay', 'd2'): 1, ('ribeironeto', 'd2'): 1, ('modern', 'd2'): 1, ('requir', 'd2'): 2, ('man', 'd2'): 1, ('raghavan', 'd2'): 1, ('schutz', 'd2'): 1, ('introduct', 'd2'): 5, ('recommend', 'd2'): 3, ('polici', 'd2'): 2, ('grade', 'd2'): 4, ('midterm', 'd2'): 2, ('quiz', 'd2'): 1, ('participationinteractionpresent', 'd2'): 1, ('submiss', 'd2'): 1, ('late', 'd2'): 1, ('plagiar', 'd2'): 4, ('intellectu', 'd2'): 1, ('engag', 'd2'): 1, ('read', 'd2'): 2, ('gener', 'd2'): 1, ('correct', 'd2'): 1, ('robust', 'd2'): 1, ('qualiti', 'd2'): 1, ('style', 'd2'): 2, ('written', 'd2'): 1, ('code', 'd2'): 4, ('shoud', 'd2'): 1, ('follow', 'd2'): 1, ('standard', 'd2'): 2, ('plagiarismch', 'd2'): 1, ('cheat', 'd2'): 2, ('behavior', 'd2'): 1, ('form', 'd2'): 1, ('uneth', 'd2'): 1, ('detriment', 'd2'): 1, ('proper', 'd2'): 2, ('educ', 'd2'): 1, ('toler', 'd2'): 1, ('work', 'd2'): 4, ('submit', 'd2'): 1, ('project', 'd2'): 2, ('program', 'd2'): 1, ('lab', 'd2'): 1, ('quizz', 'd2'): 1, ('test', 'd2'): 1, ('expect', 'd2'): 1, ('incur', 'd2'): 1, ('part', 'd2'): 1, ('pass', 'd2'): 1, ('credit', 'd2'): 1, ('list', 'd2'): 1, ('sourc', 'd2'): 2, ('reader', 'd2'): 1, ('led', 'd2'): 1, ('effort', 'd2'): 1, ('allow', 'd2'): 1, ('encourag', 'd2'): 1, ('discuss', 'd2'): 1, ('resourc', 'd2'): 1, ('literatur', 'd2'): 1, ('includ', 'd2'): 3, ('internet', 'd2'): 1, ('refer', 'd2'): 2, ('materi', 'd2'): 4, ('consult', 'd2'): 1, ('citat', 'd2'): 1, ('made', 'd2'): 1, ('verbatim', 'd2'): 1, ('occur', 'd2'): 1, ('receiv', 'd2'): 1, ('fail', 'd2'): 2, ('discret', 'd2'): 1, ('courseth', 'd2'): 1, ('decid', 'd2'): 1, ('forward', 'd2'): 1, ('incid', 'd2'): 1, ('judici', 'd2'): 1, ('affair', 'd2'): 1, ('disciplinari', 'd2'): 1, ('action', 'd2'): 1, ('conduct', 'd2'): 1, ('academ', 'd2'): 1, ('disciplin', 'd2'): 1, ('procedur', 'd2'): 1, ('httpwwwpeoplememphisedujaffair', 'd2'): 1, ('tent', 'd2'): 1, ('find', 'd2'): 1, ('compil', 'd2'): 1, ('person', 'd2'): 1, ('note', 'd2'): 1, ('famou', 'd2'): 1, ('primarili', 'd2'): 1, ('ut', 'd2'): 1, ('austin', 'd2'): 1, ('dr', 'd2'): 2, ('ray', 'd2'): 1, ('mooney', 'd2'): 1, ('unt', 'd2'): 1, ('rada', 'd2'): 1, ('mihalcea', 'd2'): 1, ('week', 'd2'): 17, ('half', 'd2'): 2, ('ppt', 'd2'): 23, ('chapter', 'd2'): 8, ('perl', 'd2'): 3, ('tutori', 'd2'): 1, ('ir', 'd2'): 5, ('evalu', 'd2'): 2, ('queri', 'd2'): 2, ('oper', 'd2'): 2, ('properti', 'd2'): 1, ('index', 'd2'): 1, ('break', 'd2'): 1, ('intro', 'd2'): 2, ('review', 'd2'): 3, ('porter', 'd2'): 2, ('stemmer', 'd2'): 2, ('slide', 'd2'): 1, ('mapreduc', 'd2'): 1, ('paper', 'd2'): 2, ('pagerank', 'd2'): 1, ('categor', 'd2'): 2, ('cluster', 'd2'): 2, ('modelsppt', 'd2'): 2, ('question', 'd2'): 1, ('answer', 'd2'): 1, ('thanksgiv', 'd2'): 1, ('final', 'd2'): 1, ('exam', 'd2'): 1, ('amam', 'd2'): 1, ('depart', 'd2'): 1, ('scienc', 'd2'): 1, ('room', 'd2'): 1, ('tn', 'd2'): 1, ('phone', 'd2'): 1, ('fax', 'd2'): 1, ('maintain', 'd2'): 1, ('inform', 'd4'): 17, ('retriev', 'd4'): 11, ('institut', 'd4'): 1, ('intellig', 'd4'): 2, ('systemsth', 'd4'): 1, ('univers', 'd4'): 4, ('memphi', 'd4'): 3, ('web', 'd4'): 11, ('search', 'd4'): 12, ('prof', 'd4'): 3, ('vasil', 'd4'): 2, ('ru', 'd4'): 2, ('comppsyc', 'd4'): 1, ('fall', 'd4'): 2, ('announc', 'd4'): 3, ('schedul', 'd4'): 4, ('assign', 'd4'): 20, ('due', 'd4'): 3, ('oct', 'd4'): 1, ('open', 'd4'): 2, ('check', 'd4'): 2, ('tabl', 'd4'): 2, ('sept', 'd4'): 3, ('enrol', 'd4'): 1, ('level', 'd4'): 1, ('section', 'd4'): 1, ('phd', 'd4'): 1, ('student', 'd4'): 7, ('send', 'd4'): 1, ('topic', 'd4'): 2, ('present', 'd4'): 3, ('syllabu', 'd4'): 1, ('address', 'd4'): 1, ('major', 'd4'): 3, ('problem', 'd4'): 4, ('time', 'd4'): 1, ('today', 'd4'): 1, ('lack', 'd4'): 1, ('way', 'd4'): 1, ('organ', 'd4'): 1, ('vast', 'd4'): 1, ('amount', 'd4'): 1, ('fingertip', 'd4'): 1, ('effect', 'd4'): 1, ('face', 'd4'): 1, ('overload', 'd4'): 1, ('class', 'd4'): 3, ('challeng', 'd4'): 2, ('pose', 'd4'): 1, ('solut', 'd4'): 2, ('introduc', 'd4'): 1, ('comput', 'd4'): 2, ('techniqu', 'd4'): 2, ('static', 'd4'): 1, ('collect', 'd4'): 2, ('document', 'd4'): 2, ('dynam', 'd4'): 1, ('expos', 'd4'): 1, ('text', 'd4'): 7, ('process', 'd4'): 3, ('algorithm', 'd4'): 1, ('classic', 'd4'): 1, ('model', 'd4'): 5, ('boolean', 'd4'): 1, ('vectori', 'd4'): 1, ('close', 'd4'): 1, ('relat', 'd4'): 2, ('natur', 'd4'): 2, ('languag', 'd4'): 3, ('catalog', 'd4'): 1, ('entri', 'd4'): 1, ('advanc', 'd4'): 3, ('current', 'd4'): 1, ('research', 'd4'): 1, ('databas', 'd4'): 1, ('manag', 'd4'): 1, ('emphasi', 'd4'): 1, ('nontradit', 'd4'): 1, ('data', 'd4'): 1, ('applic', 'd4'): 1, ('prerequisit', 'd4'): 1, ('comp', 'd4'): 1, ('permiss', 'd4'): 1, ('instructor', 'd4'): 3, ('lectur', 'd4'): 7, ('tth', 'd4'): 2, ('ampm', 'd4'): 1, ('fogelman', 'd4'): 1, ('classroom', 'd4'): 1, ('build', 'd4'): 1, ('ta', 'd4'): 3, ('shrestha', 'd4'): 2, ('bidhya', 'd4'): 2, ('bshrsthamemphisedu', 'd4'): 1, ('offic', 'd4'): 2, ('hour', 'd4'): 1, ('ppm', 'd4'): 1, ('appt', 'd4'): 1, ('dh', 'd4'): 1, ('mw', 'd4'): 1, ('pm', 'd4'): 1, ('dunn', 'd4'): 2, ('hall', 'd4'): 2, ('page', 'd4'): 3, ('httpwwwcsmemphiseduvrusteachingirwebsearch', 'd4'): 1, ('textbook', 'd4'): 2, ('baezay', 'd4'): 1, ('ribeironeto', 'd4'): 1, ('modern', 'd4'): 1, ('requir', 'd4'): 2, ('man', 'd4'): 1, ('raghavan', 'd4'): 1, ('schutz', 'd4'): 1, ('introduct', 'd4'): 5, ('recommend', 'd4'): 3, ('polici', 'd4'): 2, ('grade', 'd4'): 4, ('midterm', 'd4'): 2, ('quiz', 'd4'): 1, ('participationinteractionpresent', 'd4'): 1, ('submiss', 'd4'): 1, ('late', 'd4'): 1, ('plagiar', 'd4'): 4, ('intellectu', 'd4'): 1, ('engag', 'd4'): 1, ('read', 'd4'): 2, ('gener', 'd4'): 1, ('correct', 'd4'): 1, ('robust', 'd4'): 1, ('qualiti', 'd4'): 1, ('style', 'd4'): 2, ('written', 'd4'): 1, ('code', 'd4'): 4, ('shoud', 'd4'): 1, ('follow', 'd4'): 1, ('standard', 'd4'): 2, ('plagiarismch', 'd4'): 1, ('cheat', 'd4'): 2, ('behavior', 'd4'): 1, ('form', 'd4'): 1, ('uneth', 'd4'): 1, ('detriment', 'd4'): 1, ('proper', 'd4'): 2, ('educ', 'd4'): 1, ('toler', 'd4'): 1, ('work', 'd4'): 4, ('submit', 'd4'): 1, ('project', 'd4'): 2, ('program', 'd4'): 1, ('lab', 'd4'): 1, ('quizz', 'd4'): 1, ('test', 'd4'): 1, ('expect', 'd4'): 1, ('incur', 'd4'): 1, ('part', 'd4'): 1, ('pass', 'd4'): 1, ('credit', 'd4'): 1, ('list', 'd4'): 1, ('sourc', 'd4'): 2, ('reader', 'd4'): 1, ('led', 'd4'): 1, ('effort', 'd4'): 1, ('allow', 'd4'): 1, ('encourag', 'd4'): 1, ('discuss', 'd4'): 1, ('resourc', 'd4'): 1, ('literatur', 'd4'): 1, ('includ', 'd4'): 3, ('internet', 'd4'): 1, ('refer', 'd4'): 2, ('materi', 'd4'): 4, ('consult', 'd4'): 1, ('citat', 'd4'): 1, ('made', 'd4'): 1, ('verbatim', 'd4'): 1, ('occur', 'd4'): 1, ('receiv', 'd4'): 1, ('fail', 'd4'): 2, ('discret', 'd4'): 1, ('courseth', 'd4'): 1, ('decid', 'd4'): 1, ('forward', 'd4'): 1, ('incid', 'd4'): 1, ('judici', 'd4'): 1, ('affair', 'd4'): 1, ('disciplinari', 'd4'): 1, ('action', 'd4'): 1, ('conduct', 'd4'): 1, ('academ', 'd4'): 1, ('disciplin', 'd4'): 1, ('procedur', 'd4'): 1, ('httpwwwpeoplememphisedujaffair', 'd4'): 1, ('tent', 'd4'): 1, ('find', 'd4'): 1, ('compil', 'd4'): 1, ('person', 'd4'): 1, ('note', 'd4'): 1, ('famou', 'd4'): 1, ('primarili', 'd4'): 1, ('ut', 'd4'): 1, ('austin', 'd4'): 1, ('dr', 'd4'): 2, ('ray', 'd4'): 1, ('mooney', 'd4'): 1, ('unt', 'd4'): 1, ('rada', 'd4'): 1, ('mihalcea', 'd4'): 1, ('week', 'd4'): 17, ('half', 'd4'): 2, ('ppt', 'd4'): 23, ('chapter', 'd4'): 8, ('perl', 'd4'): 3, ('tutori', 'd4'): 1, ('ir', 'd4'): 5, ('evalu', 'd4'): 2, ('queri', 'd4'): 2, ('oper', 'd4'): 2, ('properti', 'd4'): 1, ('index', 'd4'): 1, ('break', 'd4'): 1, ('intro', 'd4'): 2, ('review', 'd4'): 3, ('porter', 'd4'): 2, ('stemmer', 'd4'): 2, ('slide', 'd4'): 1, ('mapreduc', 'd4'): 1, ('paper', 'd4'): 2, ('pagerank', 'd4'): 1, ('categor', 'd4'): 2, ('cluster', 'd4'): 2, ('modelsppt', 'd4'): 2, ('question', 'd4'): 1, ('answer', 'd4'): 1, ('thanksgiv', 'd4'): 1, ('final', 'd4'): 1, ('exam', 'd4'): 1, ('amam', 'd4'): 1, ('depart', 'd4'): 1, ('scienc', 'd4'): 1, ('room', 'd4'): 1, ('tn', 'd4'): 1, ('phone', 'd4'): 1, ('fax', 'd4'): 1, ('maintain', 'd4'): 1, ('porter', 'd5'): 14, ('stem', 'd5'): 18, ('algorithm', 'd5'): 20, ('page', 'd5'): 3, ('complet', 'd5'): 2, ('revis', 'd5'): 2, ('jan', 'd5'): 6, ('earlier', 'd5'): 1, ('edit', 'd5'): 1, ('offici', 'd5'): 2, ('home', 'd5'): 1, ('distribut', 'd5'): 5, ('written', 'd5'): 5, ('maintain', 'd5'): 1, ('author', 'd5'): 6, ('martin', 'd5'): 4, ('stemmer', 'd5'): 9, ('process', 'd5'): 2, ('remov', 'd5'): 5, ('common', 'd5'): 3, ('morpholog', 'd5'): 1, ('inflexion', 'd5'): 1, ('end', 'd5'): 3, ('word', 'd5'): 7, ('english', 'd5'): 2, ('main', 'd5'): 1, ('part', 'd5'): 2, ('term', 'd5'): 1, ('normalis', 'd5'): 1, ('set', 'd5'): 4, ('inform', 'd5'): 3, ('retriev', 'd5'): 3, ('system', 'd5'): 1, ('histori', 'd5'): 1, ('origin', 'd5'): 5, ('paper', 'd5'): 4, ('comput', 'd5'): 1, ('laboratori', 'd5'): 1, ('cambridg', 'd5'): 1, ('england', 'd5'): 1, ('larger', 'd5'): 1, ('ir', 'd5'): 3, ('project', 'd5'): 2, ('appear', 'd5'): 1, ('chapter', 'd5'): 1, ('final', 'd5'): 4, ('report', 'd5'): 2, ('cj', 'd5'): 1, ('van', 'd5'): 3, ('rijsbergen', 'd5'): 2, ('se', 'd5'): 1, ('robertson', 'd5'): 1, ('mf', 'd5'): 2, ('model', 'd5'): 1, ('probabilist', 'd5'): 1, ('london', 'd5'): 1, ('british', 'd5'): 2, ('librari', 'd5'): 2, ('research', 'd5'): 3, ('develop', 'd5'): 1, ('encourag', 'd5'): 1, ('publish', 'd5'): 6, ('suffix', 'd5'): 4, ('strip', 'd5'): 1, ('program', 'd5'): 5, ('pp', 'd5'): 1, ('reprint', 'd5'): 1, ('karen', 'd5'): 1, ('sparck', 'd5'): 1, ('jone', 'd5'): 1, ('peter', 'd5'): 1, ('willet', 'd5'): 1, ('read', 'd5'): 1, ('san', 'd5'): 1, ('francisco', 'd5'): 1, ('morgan', 'd5'): 1, ('kaufmann', 'd5'): 1, ('isbn', 'd5'): 1, ('bcpl', 'd5'): 4, ('languag', 'd5'): 3, ('popular', 'd5'): 2, ('defunct', 'd5'): 1, ('year', 'd5'): 2, ('form', 'd5'): 4, ('medium', 'd5'): 1, ('punch', 'd5'): 1, ('tape', 'd5'): 1, ('version', 'd5'): 9, ('began', 'd5'): 1, ('wide', 'd5'): 1, ('quot', 'd5'): 1, ('adapt', 'd5'): 1, ('numer', 'd5'): 1, ('variat', 'd5'): 2, ('function', 'd5'): 1, ('web', 'd5'): 2, ('primarili', 'd5'): 1, ('put', 'd5'): 1, ('record', 'd5'): 1, ('straight', 'd5'): 1, ('establish', 'd5'): 1, ('definit', 'd5'): 3, ('encod', 'd5'): 8, ('ansi', 'd5'): 5, ('head', 'd5'): 2, ('tabl', 'd5'): 1, ('equival', 'd5'): 1, ('differ', 'd5'): 4, ('minor', 'd5'): 1, ('point', 'd5'): 2, ('mark', 'd5'): 1, ('download', 'd5'): 1, ('discuss', 'd5'): 1, ('regard', 'd5'): 2, ('act', 'd5'): 1, ('receiv', 'd5'): 2, ('worker', 'd5'): 1, ('present', 'd5'): 3, ('reason', 'd5'): 1, ('confid', 'd5'): 1, ('correctli', 'd5'): 1, ('affili', 'd5'): 1, ('note', 'd5'): 4, ('thread', 'd5'): 1, ('safe', 'd5'): 1, ('java', 'd5'): 1, ('perl', 'd5'): 2, ('daniel', 'd5'): 2, ('balen', 'd5'): 1, ('oct', 'd5'): 4, ('slightli', 'd5'): 2, ('faster', 'd5'): 1, ('python', 'd5'): 1, ('vivak', 'd5'): 1, ('gupta', 'd5'): 1, ('csharp', 'd5'): 4, ('andré', 'd5'): 1, ('hazelwood', 'd5'): 1, ('guid', 'd5'): 1, ('sep', 'd5'): 4, ('net', 'd5'): 2, ('compliant', 'd5'): 2, ('leif', 'd5'): 1, ('azzopardi', 'd5'): 1, ('univer', 'd5'): 1, ('paisley', 'd5'): 1, ('scotland', 'd5'): 1, ('nov', 'd5'): 4, ('brad', 'd5'): 2, ('patton', 'd5'): 1, ('ratborgblogspotcom', 'd5'): 1, ('dec', 'd5'): 1, ('standard', 'd5'): 2, ('code', 'd5'): 1, ('frank', 'd5'): 2, ('kolnick', 'd5'): 1, ('compact', 'd5'): 1, ('simplifi', 'd5'): 1, ('lisp', 'd5'): 1, ('steven', 'd5'): 1, ('haflich', 'd5'): 1, ('franz', 'd5'): 1, ('mar', 'd5'): 2, ('rubi', 'd5'): 1, ('ray', 'd5'): 1, ('pereda', 'd5'): 1, ('wwwrayperedacom', 'd5'): 1, ('github', 'd5'): 10, ('link', 'd5'): 12, ('visual', 'd5'): 2, ('basic', 'd5'): 1, ('vb', 'd5'): 1, ('navonil', 'd5'): 1, ('mustafe', 'd5'): 1, ('brunel', 'd5'): 1, ('univers', 'd5'): 5, ('apr', 'd5'): 5, ('delphi', 'd5'): 1, ('jo', 'd5'): 1, ('rabin', 'd5'): 1, ('javascript', 'd5'): 1, ('andargor', 'd5'): 1, ('wwwandargorcom', 'd5'): 1, ('jul', 'd5'): 3, ('substanti', 'd5'): 1, ('bychristoph', 'd5'): 1, ('mckenzi', 'd5'): 1, ('basicvb', 'd5'): 1, ('christo', 'd5'): 1, ('attiko', 'd5'): 1, ('piraeu', 'd5'): 1, ('greec', 'd5'): 1, ('php', 'd5'): 1, ('richard', 'd5'): 2, ('hey', 'd5'): 1, ('wwwphpguruorg', 'd5'): 1, ('feb', 'd5'): 3, ('prolog', 'd5'): 1, ('philip', 'd5'): 1, ('brook', 'd5'): 1, ('georgia', 'd5'): 1, ('haskel', 'd5'): 1, ('dmitri', 'd5'): 1, ('antonyuk', 'd5'): 1, ('tsql', 'd5'): 1, ('keith', 'd5'): 1, ('lubel', 'd5'): 1, ('wwwatelierdevitrauxcom', 'd5'): 1, ('matlab', 'd5'): 1, ('juan', 'd5'): 1, ('carlo', 'd5'): 1, ('lopez', 'd5'): 1, ('california', 'd5'): 1, ('pacif', 'd5'): 1, ('medic', 'd5'): 1, ('centerresearch', 'd5'): 1, ('institut', 'd5'): 3, ('tcl', 'd5'): 1, ('ari', 'd5'): 1, ('theodorako', 'd5'): 1, ('ncsr', 'd5'): 1, ('demokrito', 'd5'): 1, ('truemper', 'd5'): 1, ('humboldtuniversitaet', 'd5'): 1, ('zu', 'd5'): 1, ('berlin', 'd5'): 1, ('erlang', 'd5'): 2, ('alden', 'd5'): 1, ('dima', 'd5'): 1, ('nation', 'd5'): 1, ('andtechnolog', 'd5'): 1, ('gaithersburg', 'd5'): 1, ('md', 'd5'): 1, ('usa', 'd5'): 1, ('rebol', 'd5'): 1, ('dale', 'd5'): 1, ('brearcliff', 'd5'): 1, ('scala', 'd5'): 1, ('ken', 'd5'): 1, ('faulkner', 'd5'): 1, ('sa', 'd5'): 1, ('antoin', 'd5'): 1, ('stpierr', 'd5'): 1, ('busi', 'd5'): 1, ('plugin', 'd5'): 1, ('vim', 'd5'): 1, ('script', 'd5'): 1, ('mitchel', 'd5'): 1, ('bowden', 'd5'): 1, ('nodej', 'd5'): 1, ('jed', 'd5'): 1, ('parson', 'd5'): 1, ('jedparsonscom', 'd5'): 1, ('googl', 'd5'): 1, ('alex', 'd5'): 1, ('gonopolskiy', 'd5'): 1, ('awk', 'd5'): 1, ('gregori', 'd5'): 1, ('grefenstett', 'd5'): 1, ('dscomexalead', 'd5'): 1, ('clojur', 'd5'): 1, ('yushi', 'd5'): 1, ('wang', 'd5'): 1, ('bitbucket', 'd5'): 1, ('rust', 'd5'): 1, ('nhat', 'd5'): 1, ('minh', 'd5'): 1, ('nanyang', 'd5'): 1, ('technolog', 'd5'): 2, ('aug', 'd5'): 1, ('vala', 'd5'): 1, ('serg', 'd5'): 1, ('huln', 'd5'): 1, ('mysql', 'd5'): 1, ('john', 'd5'): 1, ('carti', 'd5'): 1, ('enlighten', 'd5'): 1, ('job', 'd5'): 1, ('julia', 'd5'): 1, ('matãa', 'd5'): 1, ('guzmãn', 'd5'): 1, ('naranjo', 'd5'): 1, ('flex', 'd5'): 1, ('zalãn', 'd5'): 1, ('bodã³', 'd5'): 1, ('babesbolyai', 'd5'): 1, ('zalan', 'd5'): 1, ('mohit', 'd5'): 1, ('makkar', 'd5'): 1, ('indian', 'd5'): 1, ('delhi', 'd5'): 1, ('groovi', 'd5'): 1, ('dhaval', 'd5'): 1, ('dave', 'd5'): 1, ('jun', 'd5'): 1, ('oorexx', 'd5'): 1, ('po', 'd5'): 1, ('jonsson', 'd5'): 1, ('sourceforg', 'd5'): 1, ('xslt', 'd5'): 1, ('joey', 'd5'): 1, ('takeda', 'd5'): 1, ('lpa', 'd5'): 1, ('winprolog', 'd5'): 1, ('brian', 'd5'): 1, ('steel', 'd5'): 1, ('solanumorg', 'd5'): 1, ('gnu', 'd5'): 1, ('pspp', 'd5'): 1, ('fran', 'd5'): 1, ('houwel', 'd5'): 1, ('typescript', 'd5'): 1, ('max', 'd5'): 1, ('patiiuk', 'd5'): 1, ('free', 'd5'): 3, ('charg', 'd5'): 2, ('purpos', 'd5'): 4, ('question', 'd5'): 4, ('direct', 'd5'): 1, ('test', 'd5'): 3, ('sampl', 'd5'): 1, ('vocabulari', 'd5'): 1, ('megabyt', 'd5'): 1, ('output', 'd5'): 1, ('email', 'd5'): 1, ('comment', 'd5'): 1, ('suggest', 'd5'): 2, ('queri', 'd5'): 1, ('extra', 'd5'): 1, ('rule', 'd5'): 11, ('step', 'd5'): 4, ('logi', 'd5'): 1, ('log', 'd5'): 1, ('archaeolog', 'd5'): 2, ('equat', 'd5'): 2, ('abli', 'd5'): 1, ('replac', 'd5'): 2, ('bli', 'd5'): 1, ('ble', 'd5'): 1, ('possibl', 'd5'): 1, ('leav', 'd5'): 4, ('string', 'd5'): 4, ('length', 'd5'): 3, ('case', 'd5'): 4, ('unchang', 'd5'): 1, ('pass', 'd5'): 1, ('lose', 'd5'): 1, ('deriv', 'd5'): 2, ('great', 'd5'): 1, ('distanc', 'd5'): 1, ('public', 'd5'): 1, ('difficult', 'd5'): 1, ('emphasis', 'd5'): 1, ('small', 'd5'): 2, ('compar', 'd5'): 1, ('observ', 'd5'): 1, ('statu', 'd5'): 1, ('frozen', 'd5'): 1, ('strictli', 'd5'): 1, ('defin', 'd5'): 1, ('amen', 'd5'): 1, ('modif', 'd5'): 1, ('inferior', 'd5'): 1, ('snowbal', 'd5'): 3, ('subject', 'd5'): 1, ('occasion', 'd5'): 2, ('improv', 'd5'): 3, ('practic', 'd5'): 1, ('work', 'd5'): 2, ('recommend', 'd5'): 1, ('involv', 'd5'): 1, ('experi', 'd5'): 1, ('repeat', 'd5'): 1, ('error', 'd5'): 6, ('histor', 'd5'): 1, ('shortcom', 'd5'): 1, ('found', 'd5'): 1, ('explain', 'd5'): 3, ('type', 'd5'): 1, ('condit', 'd5'): 1, ('appli', 'd5'): 3, ('longest', 'd5'): 2, ('match', 'd5'): 2, ('true', 'd5'): 1, ('succe', 'd5'): 2, ('fail', 'd5'): 2, ('simpli', 'd5'): 1, ('turn', 'd5'): 2, ('list', 'd5'): 1, ('run', 'd5'): 1, ('lead', 'd5'): 1, ('place', 'd5'): 1, ('mement', 'd5'): 1, ('mment', 'd5'): 1, ('ment', 'd5'): 4, ('ement', 'd5'): 1, ('ent', 'd5'): 3, ('properli', 'd5'): 1, ('argument', 'd5'): 2, ('argu', 'd5'): 1, ('measur', 'd5'): 4, ('equal', 'd5'): 2, ('argum', 'd5'): 1, ('delic', 'd5'): 1, ('liabl', 'd5'): 1, ('misinterpret', 'd5'): 1, ('greater', 'd5'): 3, ('care', 'd5'): 1, ('requir', 'd5'): 1, ('tion', 'd5'): 3, ('ms', 'd5'): 1, ('mean', 'd5'): 2, ('take', 'd5'): 3, ('ion', 'd5'): 1, ('sion', 'd5'): 1, ('similar', 'd5'): 2, ('confus', 'd5'): 1, ('aris', 'd5'): 1, ('interpret', 'd5'): 1, ('reduc', 'd5'): 1, ('doubl', 'd5'): 1, ('singl', 'd5'): 1, ('cruder', 'd5'): 1, ('conson', 'd5'): 1, ('vowel', 'd5'): 1, ('wrong', 'd5'): 1, ('round', 'd5'): 1, ('interest', 'd5'): 1, ('switch', 'd5'): 1, ('letter', 'd5'): 1, ('techniqu', 'd5'): 1, ('make', 'd5'): 2, ('slower', 'd5'): 1, ('faq', 'd5'): 1, ('frequent', 'd5'): 1, ('ask', 'd5'): 3, ('licens', 'd5'): 5, ('arrang', 'd5'): 2, ('softwar', 'd5'): 6, ('recent', 'd5'): 1, ('period', 'd5'): 1, ('clear', 'd5'): 1, ('statment', 'd5'): 1, ('problem', 'd5'): 1, ('intellectu', 'd5'): 1, ('properti', 'd5'): 1, ('major', 'd5'): 1, ('issu', 'd5'): 2, ('formal', 'd5'): 1, ('statement', 'd5'): 1, ('expect', 'd5'): 2, ('restat', 'd5'): 1, ('text', 'd5'): 1, ('rare', 'd5'): 1, ('restrict', 'd5'): 1, ('bsd', 'd5'): 2, ('endors', 'd5'): 1, ('contributor', 'd5'): 3, ('unnecessari', 'd5'): 1, ('confirm', 'd5'): 1, ('employ', 'd5'): 2, ('proof', 'd5'): 2, ('websit', 'd5'): 1, ('posit', 'd5'): 1, ('simpler', 'd5'): 1, ('contribut', 'd5'): 1, ('boulton', 'd5'): 1, ('right', 'd5'): 1, ('produc', 'd5'): 1, ('proper', 'd5'): 1, ('crude', 'd5'): 1, ('real', 'd5'): 1, ('bring', 'd5'): 1, ('variant', 'd5'): 1, ('map', 'd5'): 1, ('paradigm', 'd5'): 1, ('connect', 'd5'): 1, ('import', 'd5'): 1, ('rememb', 'd5'): 1, ('achiev', 'd5'): 1, ('perfect', 'd5'): 1, ('balanc', 'd5'): 1, ('perform', 'd5'): 2, ('individu', 'd5'): 1, ('matter', 'd5'): 1, ('addit', 'd5'): 1, ('includ', 'd5'): 1, ('file', 'd6'): 1, ('found', 'd6'): 1, ('relationship', 'd7'): 1, ('secretari', 'd9'): 1, ('transport', 'd9'): 1, ('pete', 'd9'): 1, ('buttigieg', 'd9'): 1, ('candid', 'd9'): 1, ('recent', 'd9'): 1, ('visit', 'd9'): 1, ('late', 'd9'): 1, ('show', 'd9'): 1, ('stephen', 'd9'): 1, ('colbert', 'd9'): 1, ('speaker', 'd9'): 2, ('mike', 'd9'): 1, ('johnson', 'd9'): 2, ('unknown', 'd9'): 1, ('republican', 'd9'): 1, ('louisiana', 'd9'): 1, ('lawmak', 'd9'): 1, ('elect', 'd9'): 1, ('california', 'd9'): 1, ('rep', 'd9'): 1, ('kevin', 'd9'): 1, ('mccarthi', 'd9'): 1, ('oust', 'd9'): 1, ('doubl', 'd9'): 1, ('highlight', 'd9'): 1, ('extrem', 'd9'): 1, ('view', 'd9'): 1, ('appear', 'd9'): 1, ('cnn', 'd9'): 1, ('friday', 'd9'): 1, ('dont', 'd11'): 1, ('realiz', 'd11'): 1, ('power', 'd11'): 1, ('white', 'd11'): 1, ('christian', 'd11'): 1, ('evangel', 'd11'): 1, ('taylor', 'd12'): 1, ('swift', 'd12'): 1, ('absent', 'd12'): 1, ('kansa', 'd12'): 1, ('citi', 'd12'): 1, ('chief', 'd12'): 1, ('game', 'd12'): 1, ('germani', 'd12'): 1, ('morn', 'd12'): 1, ('fan', 'd12'): 1, ('mock', 'd12'): 1, ('travi', 'd12'): 1, ('kelc', 'd12'): 1, ('perform', 'd12'): 1, ('month', 'd13'): 1, ('quietli', 'd13'): 1, ('signal', 'd13'): 1, ('support', 'd13'): 1, ('ron', 'd13'): 1, ('desanti', 'd13'): 1, ('iowa', 'd13'): 1, ('gov', 'd13'): 1, ('kim', 'd13'): 1, ('reynold', 'd13'): 1, ('formal', 'd13'): 1, ('endors', 'd13'): 1, ('florida', 'd13'): 1, ('governor', 'd13'): 1, ('presid', 'd13'): 1, ('de', 'd13'): 2, ('moin', 'd13'): 2, ('ralli', 'd13'): 1, ('monday', 'd13'): 1, ('sourc', 'd13'): 1, ('close', 'd13'): 1, ('confirm', 'd13'): 1, ('regist', 'd13'): 1, ('purchas', 'd14'): 1, ('independ', 'd14'): 1, ('review', 'd14'): 1, ('product', 'd14'): 1, ('servic', 'd14'): 1, ('link', 'd14'): 1, ('websit', 'd14'): 1, ('sheknow', 'd14'): 1, ('receiv', 'd14'): 1, ('affili', 'd14'): 1, ('commiss', 'd14'): 1, ('sylvest', 'd15'): 1, ('stallon', 'd15'): 1, ('reflect', 'd15'): 1, ('relationship', 'd15'): 1, ('late', 'd15'): 1, ('son', 'd15'): 1, ('netflix', 'd15'): 1, ('documentari', 'd15'): 1, ('sli', 'd15'): 1, ('roseann', 'd16'): 1, ('barr', 'd16'): 1, ('call', 'd16'): 1, ('fan', 'd16'): 1, ('refer', 'd16'): 1, ('presid', 'd16'): 3, ('donald', 'd16'): 1, ('trump', 'd16'): 1, ('twiceelect', 'd16'): 1, ('elect', 'd16'): 1}



```python

```


```python


import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader  
from io import BytesIO


# Create an SSL context that does not verify certificates
ssl_context = ssl._create_unverified_context()

# Load stopwords with SSL verification disabled
stopWords = urlopen("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt", context=ssl_context).read()
stopWordsContent = BeautifulSoup(stopWords, features="html.parser")
stopwordsdata = stopWordsContent.get_text().split("\n")
# Set the main URL and retrieve its content
url = "https://www.memphis.edu/"
page = requests.get(url, stream=True)
soup = BeautifulSoup(page.content, "html.parser")

count = 0
linksData = set()

# Process each link found on the main page
for link in soup.findAll('a'):
    url = link.get('href')
    if url:
        linksData.add(url)
        text = []
        tokens = []
        
        if ".pdf" in url:
            print(f"Processing PDF: {url}")
            response = requests.get(url)
            raw_text = response.content
            with BytesIO(raw_text) as data:
                reader = PdfReader(data)  # Updated to PdfReader
                for page in reader.pages:
                    text.append(page.extract_text())
            if text:
                text_content = text[0].replace("\n", " ")
                tokens = text_content.split()

        elif ".txt" in url:
            print(f"Processing TXT: {url}")
            response = requests.get(url)
            text_content = response.text.replace("\n", " ")
            tokens = text_content.split()

        elif ".php" in url or ".html" in url:
            print(f"Processing PHP/HTML: {url}")
            response = requests.get(url)
            page_soup = BeautifulSoup(response.content, 'html5lib')
            body_text = ''.join(page_soup.findAll(text=True))
            text_content = body_text.replace("\n", " ")
            tokens = text_content.split()

        # Save the processed tokens to text files in chunks of 50 words
        for i in range(0, len(tokens) - 50, 50):
            chunk = tokens[i:i + 50]
            filename = f'file{count}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(chunk))
            count += 1

# Save all processed links to a text file
with open('links.txt', 'w') as file:
    file.write("\n".join(linksData))

# List of specific website links to process
websiteLinks = [
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://cs.memphis.edu/~vrus/teaching/ir-websearch/",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html",
    "https://sites.google.com/view/dr-vasile-rus/home",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule"
]

# Process and save the content of each specific link
for webLink in websiteLinks:
    print(f"Processing Website Link: {webLink}")
    response = requests.get(webLink, verify=False)
    page_soup = BeautifulSoup(response.content, 'html5lib')
    body_text = ''.join(page_soup.findAll(text=True))
    text_content = body_text.replace("\n", " ")
    tokens = text_content.split()

    # Save the processed tokens in chunks of 50 words
    for i in range(0, len(tokens) - 50, 50):
        chunk = tokens[i:i + 50]
        filename = f'file{count}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(chunk))
        count += 1

```

    Processing PHP/HTML: https://www.memphis.edu/web-directory/index.php


    /var/folders/j5/xztrhdhn3qlgj7zqy616yj7m0000gn/T/ipykernel_3388/1434099465.py:53: DeprecationWarning: The 'text' argument to find()-type methods is deprecated. Use 'string' instead.
      body_text = ''.join(page_soup.findAll(text=True))


    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/index.php
    Processing PHP/HTML: https://www.memphis.edu/safety/index.php
    Processing PHP/HTML: https://www.memphis.edu/development/index.php
    Processing PHP/HTML: https://www.memphis.edu/contact/index.php
    Processing PHP/HTML: https://www.memphis.edu/safety/index.php
    Processing PHP/HTML: https://www.memphis.edu/prospective/index.php
    Processing PHP/HTML: https://www.memphis.edu/academicsuccess/index.php
    Processing PHP/HTML: https://www.memphis.edu/umparents/index.php
    Processing PHP/HTML: https://www.memphis.edu/veterans/index.php
    Processing PHP/HTML: https://www.memphis.edu/fac_staff/index.php
    Processing PHP/HTML: https://www.memphis.edu/academics/index.php
    Processing PHP/HTML: https://www.memphis.edu/academics/colleges-schools.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/index.php
    Processing PHP/HTML: https://www.memphis.edu/lambuth/index.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/calendars/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/transfer.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/virtualtour.php
    Processing PHP/HTML: https://www.memphis.edu/usbs/fees/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/researchers/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/industry/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/facilities/centers_institutes.php
    Processing PHP/HTML: https://www.memphis.edu/fedex/index.php
    Processing PHP/HTML: https://www.memphis.edu/oir/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/special-collections/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/help/askalibrarian.php
    Processing PHP/HTML: https://www.memphis.edu/athletics/index.php
    Processing PHP/HTML: https://www.memphis.edu/campusrec/sports/index.php
    Processing PHP/HTML: https://www.memphis.edu/campusrec/index.php
    Processing PHP/HTML: https://www.memphis.edu/tsf/index.php
    Processing PHP/HTML: https://www.memphis.edu/development/index.php
    Processing PHP/HTML: https://www.memphis.edu/tsf/index.php
    Processing PHP/HTML: https://www.memphis.edu/cfr/index.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/programs/jd-mba.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/esl.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/index.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/sociology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/aal.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/crwr.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/laln.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/lit.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/prwr.php
    Processing PHP/HTML: https://www.memphis.edu/history/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/intl/curriculum/index.php
    Processing PHP/HTML: https://www.memphis.edu/anthropology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cjustice/programs/undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/socialwork/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/biology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/bs-chem.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/bs-biochem.php
    Processing PHP/HTML: https://www.memphis.edu/earthsciences/programs/undergraduate/undergraduate-courses.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/bs_conc_cyber_security.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/msci/research/stat.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/mfa/creative_writing.php
    Processing PHP/HTML: https://www.memphis.edu/polisci/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/sociology/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/padm/mpa/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/ma/esl.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/graduate/phd-course-requirements.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/graduate/master.php
    Processing PHP/HTML: https://www.memphis.edu/anthropology/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cjustice/programs/graduate.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/schabout.php
    Processing PHP/HTML: https://www.memphis.edu/planning/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/clinabout.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/msgpabout.php
    Processing PHP/HTML: https://www.memphis.edu/socialwork/graduate/licensure-program-requirements.php
    Processing PHP/HTML: https://www.memphis.edu/earthsciences/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/bioinformatics/index.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/phd.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/masters.php
    Processing PHP/HTML: https://www.memphis.edu/physics/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/phd_computer_science.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/ms_computer_science.php
    Processing PHP/HTML: https://www.memphis.edu/msci/grad/phdmath.php
    Processing PHP/HTML: https://www.memphis.edu/msci/grad/msprogram.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/art-education-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/global-art-histories-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/photography-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/studio-arts-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/global-art-histories-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/architecture/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/pr.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/news.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/creative.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/advertising.php
    Processing PDF: https://www.memphis.edu/architecture/docs/pos.bfa.inar.pdf
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfadance.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfaperformance.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfamt.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfadesign.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/ug_fvp.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/dancescience.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/popular_studies.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/jazz.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/jazz.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/performance.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mus_bus.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/engineering.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/comp-theory.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mushist.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/comm_studies.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/ug_fvp.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mused.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/general-art-history-graduate.php
    Processing PHP/HTML: https://www.memphis.edu/communication/graduate/ma_program/ma_comm.php
    Processing PHP/HTML: https://www.memphis.edu/architecture/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/mfaintheatre.php
    Processing PHP/HTML: https://www.memphis.edu/communication/graduate/phd.php
    Processing PHP/HTML: https://www.memphis.edu/icl/integrative_studies/degrees/sec_math_bsed.php
    Processing PHP/HTML: https://www.memphis.edu/_archive/cepr/counseling/admissions.php
    Processing PHP/HTML: https://www.memphis.edu/lead/hiad/degrees_and_certificates/edd_higher_adult_education.php
    Processing PHP/HTML: https://www.memphis.edu/lead/ldps/degrees_and_certificates/ms_school_admin_supervision.php
    Processing PHP/HTML: https://www.memphis.edu/_archive/icl/advising/edd_advising.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/counseling/degrees_and_certificates/index.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/masters.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/pete.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/sport-coaching.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/exercise-sport-movement-sciences.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/dietetics.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/health-sciences.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/healthcare-leadership.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/medical_assisting.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/nutrition-health-wellness-minor.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/clinicalnutrition.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/exercisenutrition-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/exercise-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/environmental-nutrition-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/lifestyle-medicine-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/nutrition-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/nutrition-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/physical-education-teacher-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/applied-biomechanics-phd.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/applied-physiology-nutrition-phd.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/honors/opportunities/child_development_and_family_studies.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/padm/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/index.php
    Processing PHP/HTML: https://www.memphis.edu/finance/index.php
    Processing PHP/HTML: https://www.memphis.edu/finance/index.php
    Processing PHP/HTML: https://www.memphis.edu/management/index.php
    Processing PDF: https://www.memphis.edu/fcbeusso/pdfs/majors/2018/scm_2018.pdf
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/fcbe/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/professionalmba/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/mis/index.php
    Processing PHP/HTML: https://www.memphis.edu/bme/index.php
    Processing PHP/HTML: https://www.memphis.edu/herff/departments/civil.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/et/future/index.php
    Processing PHP/HTML: https://www.memphis.edu/me/index.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/masters.php
    Processing PHP/HTML: https://www.memphis.edu/et/current/grad.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/phd.php
    Processing PHP/HTML: https://www.memphis.edu/wilson/sport/slm_bsed.php
    Processing PHP/HTML: https://www.memphis.edu/wilson/sport/slm_ms.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/bsn/updatedbsn.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/phd/phdprogram.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/msn/msnprograms.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/audamissions.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/slpadmissions.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/phdgoals.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/bsph.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/mha.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/emha.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/dual-mph.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/ms-biostat.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/phd-epibio.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/phd-sbs.php
    Processing PHP/HTML: https://www.memphis.edu/driven-by-doing/tellyourstory.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/apply/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/index.php
    Processing PHP/HTML: https://www.memphis.edu/scholarships/index.php
    Processing PHP/HTML: https://www.memphis.edu/financialaid/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/learn-more/request.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/about/request-information.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/experience/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/apply/index.php
    Processing PHP/HTML: https://www.memphis.edu/gradschool/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/int-apply.php
    Processing PHP/HTML: https://www.memphis.edu/law/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/uofm-faculty-cross-100-million-in-research-awards.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/eric-research-hub-opens-at-uofm.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/uofm-police-services-introduces-ucic.php
    Processing PHP/HTML: https://www.memphis.edu/calendar/index.php
    Processing PHP/HTML: https://www.memphis.edu/calendar/event-submission/index.php
    Processing PHP/HTML: https://www.memphis.edu/studentinvolvement/studentengagement/join.php
    Processing PHP/HTML: https://www.memphis.edu/academicsuccess/index.php
    Processing PHP/HTML: https://www.memphis.edu/service/index.php
    Processing PHP/HTML: https://www.memphis.edu/reslife/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/usbs/fees/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/faq.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/virtualtour.php
    Processing PHP/HTML: https://www.memphis.edu/aa/index.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/students/records/transcript-official.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/register/classes.php
    Processing PHP/HTML: https://www.memphis.edu/research/researchers/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/facilities/centers_institutes.php
    Processing PHP/HTML: https://www.memphis.edu/accounting/gc.php
    Processing PHP/HTML: https://www.memphis.edu/development/supportum.php
    Processing PHP/HTML: https://www.memphis.edu/cfr/index.php
    Processing PHP/HTML: https://www.memphis.edu/president/index.php
    Processing PHP/HTML: https://www.memphis.edu/aa/index.php
    Processing PHP/HTML: https://www.memphis.edu/notice/index.php#copyright
    Processing PHP/HTML: https://www.memphis.edu/notice/index.php
    Processing PHP/HTML: https://www.memphis.edu/oie/eo-aa/eo.php
    Processing PHP/HTML: https://www.memphis.edu/oie/title9/index.php
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html


    /var/folders/j5/xztrhdhn3qlgj7zqy616yj7m0000gn/T/ipykernel_3388/1434099465.py:86: DeprecationWarning: The 'text' argument to find()-type methods is deprecated. Use 'string' instead.
      body_text = ''.join(page_soup.findAll(text=True))


    Processing Website Link: https://cs.memphis.edu/~vrus/teaching/ir-websearch/
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html
    Processing Website Link: https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html
    Processing Website Link: https://sites.google.com/view/dr-vasile-rus/home
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule



```python
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import PyPDF2
from io import BytesIO
import re

import ssl
from PyPDF2 import PdfReader  





# Create an SSL context that does not verify certificates
ssl_context = ssl._create_unverified_context()

# Load stopwords with SSL verification disabled
stopWords = urlopen("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt", context=ssl_context).read()
stopWordsContent = BeautifulSoup(stopWords, features="html.parser")
stopwordsdata = stopWordsContent.get_text().split("\n")
# Set the main URL and retrieve its content
url = "https://www.memphis.edu/"
page = requests.get(url, stream=True)
soup = BeautifulSoup(page.content, "html.parser")

count = 0
linksData = set()

# Decontract function to expand contractions in text
def decontracted(phrase):
    # Handle specific contractions
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # General contractions
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

# Preprocess text: remove numbers, punctuation, URLs, and apply stemming
def preprocess(text):
    ps = PorterStemmer()
    for i in range(len(text)):
        text[i] = decontracted(text[i])
        text[i] = re.sub(r'[0-9]+', '', text[i])  # Remove digits
        text[i] = re.sub(r'[^\w\s]', '', text[i])  # Remove punctuation
        text[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text[i])  # Remove URLs
        text[i] = re.sub('<[^<]+?>', '', text[i])  # Remove HTML tags
        # Remove stopwords and apply stemming
        text[i] = ' '.join(ps.stem(word) for word in text[i].lower().split() if word not in stopwordsdata)
    return text

# Process links from the page
for link in soup.findAll('a'):
    text = []
    url = link.get('href')
    
    if url:  # Check if the link is valid
        linksData.add(url)  # Add link to processed links set
        
        if ".pdf" in url:
            print(f"Processing PDF: {url}")
            response = requests.get(url)
            raw_text = response.content
            with BytesIO(raw_text) as data:
                pdf_reader = PyPDF2.PdfReader(data)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            cleanText = preprocess(text)
            text1 = cleanText[0].replace("\n", " ")
            tokens = text1.split()

        elif ".txt" in url:
            print(f"Processing TXT: {url}")
            text = requests.get(url).text
            cleanText = preprocess([text])
            text1 = cleanText[0].replace("\n", " ")
            tokens = text1.split()

        elif ".php" in url or ".html" in url:
            print(f"Processing PHP/HTML: {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]
            cleanText = preprocess(obj)
            text = cleanText[0].replace("\n", " ")
            tokens = text.split()

        # Save tokens in chunks of 50 to text files
        for i in range(0, len(tokens) - 50, 50):
            response_data = tokens[i:i + 50]
            filename = f'file{count}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(response_data))
            count += 1

# Save the processed links into a file
with open('links.txt', 'w') as file:
    file.write("\n".join(linksData))

# Additional list of specific website links to process
websiteLinks = [
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://cs.memphis.edu/~vrus/teaching/ir-websearch/",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html",
    "https://sites.google.com/view/dr-vasile-rus/home",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule"
]

# Process the additional website links
for webLink in websiteLinks:
    print(f"Processing Website Link: {webLink}")
    response = requests.get(webLink, verify=False)
    soup = BeautifulSoup(response.content, 'html5lib')
    obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]
    cleanText = preprocess(obj)
    text = cleanText[0].replace("\n", " ")
    tokens = text.split()

    # Save the processed tokens to text files
    for i in range(0, len(tokens) - 50, 50):
        response_data = tokens[i:i + 50]
        filename = f'file{count}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(response_data))
        count += 1

```

    Processing PHP/HTML: https://www.memphis.edu/web-directory/index.php


    /var/folders/j5/xztrhdhn3qlgj7zqy616yj7m0000gn/T/ipykernel_3388/2336911841.py:92: DeprecationWarning: The 'text' argument to find()-type methods is deprecated. Use 'string' instead.
      obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]


    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/index.php
    Processing PHP/HTML: https://www.memphis.edu/safety/index.php
    Processing PHP/HTML: https://www.memphis.edu/development/index.php
    Processing PHP/HTML: https://www.memphis.edu/contact/index.php
    Processing PHP/HTML: https://www.memphis.edu/safety/index.php
    Processing PHP/HTML: https://www.memphis.edu/prospective/index.php
    Processing PHP/HTML: https://www.memphis.edu/academicsuccess/index.php
    Processing PHP/HTML: https://www.memphis.edu/umparents/index.php
    Processing PHP/HTML: https://www.memphis.edu/veterans/index.php
    Processing PHP/HTML: https://www.memphis.edu/fac_staff/index.php
    Processing PHP/HTML: https://www.memphis.edu/academics/index.php
    Processing PHP/HTML: https://www.memphis.edu/academics/colleges-schools.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/index.php
    Processing PHP/HTML: https://www.memphis.edu/lambuth/index.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/calendars/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/transfer.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/virtualtour.php
    Processing PHP/HTML: https://www.memphis.edu/usbs/fees/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/researchers/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/industry/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/facilities/centers_institutes.php
    Processing PHP/HTML: https://www.memphis.edu/fedex/index.php
    Processing PHP/HTML: https://www.memphis.edu/oir/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/special-collections/index.php
    Processing PHP/HTML: https://www.memphis.edu/libraries/help/askalibrarian.php
    Processing PHP/HTML: https://www.memphis.edu/athletics/index.php
    Processing PHP/HTML: https://www.memphis.edu/campusrec/sports/index.php
    Processing PHP/HTML: https://www.memphis.edu/campusrec/index.php
    Processing PHP/HTML: https://www.memphis.edu/tsf/index.php
    Processing PHP/HTML: https://www.memphis.edu/development/index.php
    Processing PHP/HTML: https://www.memphis.edu/tsf/index.php
    Processing PHP/HTML: https://www.memphis.edu/cfr/index.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/programs/jd-mba.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/esl.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/index.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/sociology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/aal.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/crwr.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/laln.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/lit.php
    Processing PHP/HTML: https://www.memphis.edu/english/undergraduates/concentrations/prwr.php
    Processing PHP/HTML: https://www.memphis.edu/history/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/intl/curriculum/index.php
    Processing PHP/HTML: https://www.memphis.edu/anthropology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cjustice/programs/undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/socialwork/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/biology/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/bs-chem.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/bs-biochem.php
    Processing PHP/HTML: https://www.memphis.edu/earthsciences/programs/undergraduate/undergraduate-courses.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/physics/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/bs_conc_cyber_security.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/msci/research/stat.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/mfa/creative_writing.php
    Processing PHP/HTML: https://www.memphis.edu/polisci/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/sociology/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/padm/mpa/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/english/graduate/ma/esl.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/graduate/phd-course-requirements.php
    Processing PHP/HTML: https://www.memphis.edu/philosophy/graduate/master.php
    Processing PHP/HTML: https://www.memphis.edu/anthropology/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cjustice/programs/graduate.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/schabout.php
    Processing PHP/HTML: https://www.memphis.edu/planning/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/clinabout.php
    Processing PHP/HTML: https://www.memphis.edu/psychology/graduate/msgpabout.php
    Processing PHP/HTML: https://www.memphis.edu/socialwork/graduate/licensure-program-requirements.php
    Processing PHP/HTML: https://www.memphis.edu/earthsciences/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/bioinformatics/index.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/phd.php
    Processing PHP/HTML: https://www.memphis.edu/chem/programs/masters.php
    Processing PHP/HTML: https://www.memphis.edu/physics/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/phd_computer_science.php
    Processing PHP/HTML: https://www.memphis.edu/cs/programs/ms_computer_science.php
    Processing PHP/HTML: https://www.memphis.edu/msci/grad/phdmath.php
    Processing PHP/HTML: https://www.memphis.edu/msci/grad/msprogram.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/art-education-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/global-art-histories-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/photography-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/studio-arts-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/global-art-histories-undergraduate.php
    Processing PHP/HTML: https://www.memphis.edu/architecture/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/pr.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/news.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/creative.php
    Processing PHP/HTML: https://www.memphis.edu/jrsm/undergraduate_programs/advertising.php
    Processing PDF: https://www.memphis.edu/architecture/docs/pos.bfa.inar.pdf
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfadance.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfaperformance.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfamt.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/bfadesign.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/ug_fvp.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/dancescience.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/popular_studies.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/jazz.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/jazz.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/performance.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mus_bus.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/engineering.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/comp-theory.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mushist.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/comm_studies.php
    Processing PHP/HTML: https://www.memphis.edu/communication/undergraduate/ug_fvp.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/mused.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/music/academics/degreeplans.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/general-art-history-graduate.php
    Processing PHP/HTML: https://www.memphis.edu/communication/graduate/ma_program/ma_comm.php
    Processing PHP/HTML: https://www.memphis.edu/architecture/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/artanddesign/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/theatre/academicprograms/mfaintheatre.php
    Processing PHP/HTML: https://www.memphis.edu/communication/graduate/phd.php
    Processing PHP/HTML: https://www.memphis.edu/icl/integrative_studies/degrees/sec_math_bsed.php
    Processing PHP/HTML: https://www.memphis.edu/_archive/cepr/counseling/admissions.php
    Processing PHP/HTML: https://www.memphis.edu/lead/hiad/degrees_and_certificates/edd_higher_adult_education.php
    Processing PHP/HTML: https://www.memphis.edu/lead/ldps/degrees_and_certificates/ms_school_admin_supervision.php
    Processing PHP/HTML: https://www.memphis.edu/_archive/icl/advising/edd_advising.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/counseling/degrees_and_certificates/index.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/masters.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/cepr/edpr/degrees_and_certifications/doctorate.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/pete.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/sport-coaching.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/exercise-sport-movement-sciences.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/dietetics.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/health-sciences.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/healthcare-leadership.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/medical_assisting.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/undergraduate/nutrition-health-wellness-minor.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/clinicalnutrition.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/exercisenutrition-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/exercise-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/environmental-nutrition-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/lifestyle-medicine-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/nutrition-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/nutrition-science-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/physical-education-teacher-ms.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/applied-biomechanics-phd.php
    Processing PHP/HTML: https://www.memphis.edu/healthsciences/graduate/applied-physiology-nutrition-phd.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/honors/opportunities/child_development_and_family_studies.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/padm/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/undergraduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/cpls/graduate/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/index.php
    Processing PHP/HTML: https://www.memphis.edu/finance/index.php
    Processing PHP/HTML: https://www.memphis.edu/finance/index.php
    Processing PHP/HTML: https://www.memphis.edu/management/index.php
    Processing PDF: https://www.memphis.edu/fcbeusso/pdfs/majors/2018/scm_2018.pdf
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/economics/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/fcbe/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/professionalmba/index.php
    Processing PHP/HTML: https://www.memphis.edu/accountancy/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/mis/index.php
    Processing PHP/HTML: https://www.memphis.edu/bme/index.php
    Processing PHP/HTML: https://www.memphis.edu/herff/departments/civil.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/index.php
    Processing PHP/HTML: https://www.memphis.edu/et/future/index.php
    Processing PHP/HTML: https://www.memphis.edu/me/index.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/masters.php
    Processing PHP/HTML: https://www.memphis.edu/et/current/grad.php
    Processing PHP/HTML: https://www.memphis.edu/eece/programs/phd.php
    Processing PHP/HTML: https://www.memphis.edu/wilson/sport/slm_bsed.php
    Processing PHP/HTML: https://www.memphis.edu/wilson/sport/slm_ms.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/bsn/updatedbsn.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/phd/phdprogram.php
    Processing PHP/HTML: https://www.memphis.edu/nursing/program-admit/msn/msnprograms.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/audamissions.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/slpadmissions.php
    Processing PHP/HTML: https://www.memphis.edu/csd/programs/phdgoals.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/bsph.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/mha.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/emha.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/dual-mph.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/ms-biostat.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/phd-epibio.php
    Processing PHP/HTML: https://www.memphis.edu/publichealth/programs/phd-sbs.php
    Processing PHP/HTML: https://www.memphis.edu/driven-by-doing/tellyourstory.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/apply/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/index.php
    Processing PHP/HTML: https://www.memphis.edu/scholarships/index.php
    Processing PHP/HTML: https://www.memphis.edu/financialaid/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/learn-more/request.php
    Processing PHP/HTML: https://www.memphis.edu/uofmglobal/about/request-information.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/experience/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/apply/index.php
    Processing PHP/HTML: https://www.memphis.edu/gradschool/index.php
    Processing PHP/HTML: https://www.memphis.edu/graduateadmissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/int-apply.php
    Processing PHP/HTML: https://www.memphis.edu/law/index.php
    Processing PHP/HTML: https://www.memphis.edu/law/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/uofm-faculty-cross-100-million-in-research-awards.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/eric-research-hub-opens-at-uofm.php
    Processing PHP/HTML: https://www.memphis.edu/mediaroom/releases/2024/september/uofm-police-services-introduces-ucic.php
    Processing PHP/HTML: https://www.memphis.edu/calendar/index.php
    Processing PHP/HTML: https://www.memphis.edu/calendar/event-submission/index.php
    Processing PHP/HTML: https://www.memphis.edu/studentinvolvement/studentengagement/join.php
    Processing PHP/HTML: https://www.memphis.edu/academicsuccess/index.php
    Processing PHP/HTML: https://www.memphis.edu/service/index.php
    Processing PHP/HTML: https://www.memphis.edu/reslife/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/basics/international.php
    Processing PHP/HTML: https://www.memphis.edu/usbs/fees/index.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/faq.php
    Processing PHP/HTML: https://www.memphis.edu/admissions/visit/virtualtour.php
    Processing PHP/HTML: https://www.memphis.edu/aa/index.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/students/records/transcript-official.php
    Processing PHP/HTML: https://www.memphis.edu/registrar/register/classes.php
    Processing PHP/HTML: https://www.memphis.edu/research/researchers/index.php
    Processing PHP/HTML: https://www.memphis.edu/research/facilities/centers_institutes.php
    Processing PHP/HTML: https://www.memphis.edu/accounting/gc.php
    Processing PHP/HTML: https://www.memphis.edu/development/supportum.php
    Processing PHP/HTML: https://www.memphis.edu/cfr/index.php
    Processing PHP/HTML: https://www.memphis.edu/president/index.php
    Processing PHP/HTML: https://www.memphis.edu/aa/index.php
    Processing PHP/HTML: https://www.memphis.edu/notice/index.php#copyright
    Processing PHP/HTML: https://www.memphis.edu/notice/index.php
    Processing PHP/HTML: https://www.memphis.edu/oie/eo-aa/eo.php
    Processing PHP/HTML: https://www.memphis.edu/oie/title9/index.php
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html


    /var/folders/j5/xztrhdhn3qlgj7zqy616yj7m0000gn/T/ipykernel_3388/2336911841.py:126: DeprecationWarning: The 'text' argument to find()-type methods is deprecated. Use 'string' instead.
      obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]


    Processing Website Link: https://cs.memphis.edu/~vrus/teaching/ir-websearch/
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html
    Processing Website Link: https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html
    Processing Website Link: https://sites.google.com/view/dr-vasile-rus/home
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo
    Processing Website Link: https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule



```python
import requests
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
import nltk
nltk.download('punkt_tab')

from numpy.linalg import norm
import os
from flask import Flask, render_template, request
import ssl
import logging
import traceback

import requests as requests
from flask import Flask, request, render_template
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
from numpy.linalg import norm
import os
ssl._create_default_https_context = ssl._create_unverified_context


searchengine = Flask(__name__)

response = requests.get('https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt', verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
stop_words = soup.text.split('\n')

directory = '/Users/yashds/Downloads/Inform Retrival Project/files'


def query_term_freq_inverted_index(text):
    qurey_text = [text]

    index_vector = TfidfVectorizer(input='content', encoding='utf-8', analyzer='word', tokenizer=nltk.word_tokenize,
                                   stop_words=stop_words, ngram_range=(1, 2), use_idf=True,
                                   norm='l2')

    tfidf = index_vector.fit_transform(qurey_text)

    return tfidf.toarray()

def doc_term_freq_inverted_index():
    documentsList = []
    preprocessed_files_list = []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        preprocessed_files_list.append(file)
        with open(filepath, 'r', newline='', encoding="utf-8", errors='replace') as processingfile:
            data = processingfile.read()
            documentsList.append(data)

    index_vector = TfidfVectorizer(input='content', encoding='utf-8', analyzer='word', tokenizer=nltk.word_tokenize,
                                       stop_words=stop_words, ngram_range=(1, 2), use_idf=True,
                                       norm='l2')

    tfidf = index_vector.fit_transform(documentsList)
    return tfidf.toarray(), preprocessed_files_list


@searchengine.route('/')
def initial_load():
    return render_template('index.html')


@searchengine.route('/', methods=['POST'])


    
def output():
    text = request.form.get('input-data')
    words_list = [text]
    words_list = [i for i in words_list if i]
    if len(words_list) == 0:
        return render_template('index.html')
    
    with open('/Users/yashds/Downloads/Inform Retrival Project/links.txt', 'r', newline='', encoding='utf-8') as file:
        links = file.read().split()
    
    query_vector = query_term_freq_inverted_index(text)
    document_vector, filenames = doc_term_freq_inverted_index()

    cosinesimilarity = {}
    for i in range(len(document_vector)):
        query = np.concatenate([query_vector[0], np.ones(len(document_vector[i]) - len(query_vector[0]))])
        x = np.dot(query, document_vector[i]) / (norm(query) * norm(document_vector[i]))
        cosinesimilarity[str(i)] = x

    sorted_cosine_list = sorted(cosinesimilarity.items(), key=lambda x: x[1], reverse=True)
    cosine_sorted_dict = dict(sorted_cosine_list)

    filename_sorted = []
    filelink_sorted = []

    for key, value in cosine_sorted_dict.items():
        index = int(key)
        if index < len(filenames) and index < len(links):
            filename_sorted.append(filenames[index])
            filelink_sorted.append(links[index])
        

    return render_template('output.html', length=len(filelink_sorted), file=filename_sorted, link=filelink_sorted)


if __name__ == '__main__':
    searchengine.run(port=5002) 

```

    [nltk_data] Downloading package punkt to /Users/yashds/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!
    [nltk_data] Downloading package punkt_tab to
    [nltk_data]     /Users/yashds/nltk_data...
    [nltk_data]   Package punkt_tab is already up-to-date!
    [nltk_data] Downloading package punkt to /Users/yashds/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!


     * Serving Flask app '__main__'
     * Debug mode: off


    /opt/anaconda3/lib/python3.9/site-packages/urllib3/connectionpool.py:1063: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cs.memphis.edu'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
      warnings.warn(
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5002
    Press CTRL+C to quit
    127.0.0.1 - - [05/Sep/2024 13:26:10] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [05/Sep/2024 13:26:10] "GET /favicon.ico HTTP/1.1" 404 -

