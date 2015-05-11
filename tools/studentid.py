import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
def get(student_id):
    URL = "http://icdoor.nctu.edu.tw/enitorweb/EmpReg.aspx"
    print('start get')
    r = requests.get(URL)
    print('get')
    soup = BeautifulSoup(r.text)
    viewstate = soup.findAll("input", {"type": "hidden", "name": "__VIEWSTATE"})
    eventvalidation = soup.findAll("input", {"type": "hidden", "name": "__EVENTVALIDATION"})
    data = {'__EVENTVALIDATION': eventvalidation[0]['value'],
            '__VIEWSTATE': viewstate[0]['value'],
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'txtID': student_id,
            'btn_CheckPerson': '%E6%AA%A2%E6%9F%A5%E5%80%8B%E4%BA%BA%E8%B3%87%E6%96%99'}
    print('start post')
    r = requests.post(URL, data=data)
    print('post')
    soup = BeautifulSoup(r.text)
    name = soup.find(id="lbl_NameShow")
    return name.string


def get2(_id):
    try:
        name = get(_id)
    except:
        get2(_id)
        return
    print(time.time(), _id, name)
    f = open('id','a+')
    if name:
        f.write('%s %s\n'%(_id, name))
    f.close()

if __name__ == '__main__':
    for i in range(10**7):
        _id = '%07d'%i;
        get2(_id)
        #time.sleep(0.1)
