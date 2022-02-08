import csv
import searching_html as searchHtml
import searching_text as searchText

BASE_URL = 'BASE_URL'

PARAMS = {
    BASE_URL: 'https://www.waterfordcouncil.ie/council/councillors/',
}

KEY_WORDS = [
    "comeragh/", "dungarvan-lismore/", "metropolitan/", "metropolitan/"
]

HEADERS = ['Name', 'Party', 'Email', 'Position', 'Address']

BASE_EXCEL_PATH = 'excel'
BASE_WEBPAGE_PATH = 'web_page'

def main():

    #TODO Add params to make more dynamic

    with open('%s/Waterford_City_and_County_Council.csv' % BASE_EXCEL_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()

        web_page = searchHtml.from_sting_webpage_contain('https://www.waterfordcouncil.ie/council/councillors/index.htm')
        for key_word in KEY_WORDS:
            councilors = web_page.xpath('//li/a[contains(@href,"%s")]/@href' % key_word)
            for council in councilors:
                councilURL = PARAMS[BASE_URL] + council
                print("DEBUG: Councilor Page [%s]" % councilURL)
                councilPage = searchHtml.to_sting_webpage_contain(councilURL)
                print("DEBUG: Councilor Page [%s]" % councilPage)
                nameRegex1 = '<strong>([^\s]+\s[^\s<]+\s[^\s<]+)|<strong>([^\s]+\s[^\s<]+)'
                nameRegex2 = '<strong>(?=Councillor\s([^\s]+\s[^\s<]+))|<strong>(?=Councillor\s([^\s]+\s[^\s<]+))'
                name = searchText.regex_search(nameRegex2, councilPage)
                if not name:
                    name = searchText.regex_search(nameRegex1, councilPage)
                name = list(filter(None, name[0]))
                party = searchText.regex_search('\<br\>([^*<]+)\<br\>', councilPage)
                email = searchText.regex_search('mailto:([^\s\"]+)', councilPage)
                # address = searchText.regex_search('Address:([^\<]+)', councilPage)
                position = 'Councilor'

                print("DEBUG: Name: %s, Party: %s, Email: %s, Position: %s" % (name[0], party[0], email[0], position))
                #FIXME use headers instead of hard coding
                writer.writerow({'Name': name[0],
                                 'Party': party[0],
                                 'Email': email[0],
                                 'Position': position
                                 })

            print("DEBUG: Councilors %s" % councilors)

if __name__ == '__main__':
    main()