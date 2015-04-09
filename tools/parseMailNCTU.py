from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


dormURL = [ 'http://mailsys.nctu.edu.tw/MailNotify/main.asp?dorm=' + '{0:03}'.format(i) for i in range(86,87)]
mailData = []
formatOfData = ['id','name','date','type']

for url in dormURL:
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read().decode('hkscs'))
    tables = None
    try:
        tables = soup.body.table.find_all('tr')
    except:
        continue
    if tables:
        dormName = soup.body.center.b.contents[0].replace('領信通知',' ').strip()
        tables = tables[1:]
        for t in tables:
            lines = t.find_all('font')
            tmpData = {'exist':True,'dorm':dormName}
            for index in range(0,4):
                tmpData[formatOfData[index]] = lines[index].contents[0].strip()
            mailData.append(tmpData)

print(mailData)

		

# mailData = [{'id','name','date','type','exist','dorm'}...]


	






