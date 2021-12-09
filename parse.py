from bs4 import BeautifulSoup
import requests
import openpyxl

URL = 'https://aliexpress.ru/wholesale?catId=&SearchText=ноутбук'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61'
}

def parse():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='SearchProductFeed_HorizontalCard__card__102el SearchProductFeed_Preview__card__3zxie')
    comps = []
    wb = openpyxl.Workbook()
    sheet = wb.active
    
    for i in items:
        comps.append({
            'title': i.find('a', class_='SearchProductFeed_Link__link__sf54s SearchProductFeed_Link__darkGrey__sf54s SearchProductFeed_Link__size13__sf54s SearchProductFeed_Link__display-webkit__sf54s SearchProductFeed_Link__lineClamp__sf54s SearchProductFeed_HorizontalCard__title__102el').get_text(strip=True),
            'price': i.find('span', class_='SearchProductFeed_Price__titleWrapper__1jg3h').get_text(strip=True),
            'link': i.find('a', class_='SearchProductFeed_Link__link__sf54s SearchProductFeed_Link__darkGrey__sf54s SearchProductFeed_Link__size13__sf54s SearchProductFeed_Link__display-webkit__sf54s SearchProductFeed_Link__lineClamp__sf54s SearchProductFeed_HorizontalCard__title__102el').get('href'),
        })
            
    for i in range(len(comps)):
        sheet['A'+str(i+1)] = comps[i]['title']
        sheet['B'+str(i+1)] = comps[i]['price']
        sheet['C'+str(i+1)] = comps[i]['link']
    
    wb.save('table.xlsx')
    wb.close()

parse()