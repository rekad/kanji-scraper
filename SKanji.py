import mechanize
from bs4 import BeautifulSoup
import time
import re

# Enter your username, password and useragent here
USER = ""
PASSWORD = ""
USERAGENT = ""

class KanjiScraper(object):
    """ This class inplements a scraper to get kanji storys and readings from the 
    Reviewing the Kanji Website"""

    def __init__(self):
        """ Initializes the mechanize browser"""
        
        self.ua = USERAGENT
        self.br = mechanize.Browser()
        self.br.addheaders = [('User-Agent', self.ua)]
        print "Browser initialized with user agent"

        self.login()


    def login(self):
        """Login to the Reviewing the Kanji Website using the mechanize browser"""
        
        self.br.open("http://kanji.koohii.com/login")
        self.br.form = list(self.br.forms())[0]
        self.br["username"] = USER
        self.br["password"] = PASSWORD
        my_response = self.br.submit()
        print "Login successful"


    def get_kanji_data(self, kanji):
        """ Returns kanji, on reading and story as strings a given kanji """
        
        print "Fetching data for Kanji " + str(kanji)
        
        base_url = "http://kanji.koohii.com/study/kanji/"
        response = self.br.open(base_url + str(kanji))
        soup = BeautifulSoup(response.get_data(), "html.parser")

        # Extract the Kanji
        kanji = soup.find("span", {"class":"cj-k"}).contents[0]

        # Extract Keyword
        keyword = soup.find("span", {"class":"JSEditKeyword"}).contents[0]

        # Extract On Reading
        on = soup.findAll("span",{"class":"cj-k"})
        try:
            on = on[1].contents[0]
        except IndexError:
            on = "None"

        # Extract Story
        story = soup.find("div",{"id":"sv-textarea"})

        return [kanji, keyword, on, story]


    def get_raw_kanji_data(self, kanji):

        print "Fetching raw data for Kanji " + str(kanji)
        
        base_url = "http://kanji.koohii.com/study/kanji/"
        response = self.br.open(base_url + str(kanji))
        soup = BeautifulSoup(response.get_data(), "html.parser")

        # Extract the Kanji
        kanji = soup.find("span", {"class":"cj-k"})

        # Extract On Reading
        on = soup.findAll("span",{"class":"cj-k"})

        # Extract Story
        story = soup.find("div",{"id":"sv-textarea"})

        return [kanji, on, story]


    def get_all_kanji_data(self, start = 1, end = 20):
        """ Fetches the kanji data for a certain number of kanjis """

        data = []
        try:
            for kanji_index in range(start,end+1):
                data.append(self.get_kanji_data(kanji_index))
                time.sleep(1.5) # There is a cooldown on the website
        except Exception:
            print "Error when fetching Kanji data"
            self.write_data_to_file(data, "datadump.txt")

        return data

    def write_data_to_file(self, data, filename):

        filename = "output_files/" + filename
        print "Printing kanji data to " + filename
        with open(filename, "w") as out_file:
            for kanji in data:
                try:
                    out_file.write(kanji[0].encode('utf8'))
                    out_file.write('\n')
                    out_file.write(kanji[1].encode('utf8'))
                    out_file.write('\n')
                    out_file.write(kanji[2].encode('utf8'))
                    for element in kanji[3]:    # Story is a list of unicode strings
                        out_file.write(element.encode('utf8'))
                    out_file.write('\n\n')
                except UnicodeDecodeError:
                    out_file.write("Error\n\n")
                    continue


    def strip_tags_from_file(self, filename):

        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

        with open("output_files/" + filename,"r") as in_file:
            text = in_file.read()
            text_no_tags = tag_re.sub('', text)

        with open("output_files/" + filename.split('.')[0] + "no_tags.txt", "w") as out_file:
            out_file.write(text_no_tags)


if __name__ == '__main__':

    s = KanjiScraper()
    data = s.get_all_kanji_data(1,3030)
    s.write_data_to_file(data, "complete.txt")
    s.strip_tags_from_file("complete.txt")
    print "Finished!"




# Setup

# Save results to a file
# with open("kanjis.txt","w") as out_file:
#     out_file.write(str(kanji))
#     out_file.write("\n")
#     out_file.write(str(story))
#     out_file.write("\n")
#     out_file.write(str(on_reading))
#     out_file.write("\n")



# story = soup.find("div", {"class":"bookstyle"})
# print story.string.strip()

# divs = soup.find_all("div")
# if divs == None:
#     print "Nothing found!"
# else: 
#     for div in divs:
#         print div