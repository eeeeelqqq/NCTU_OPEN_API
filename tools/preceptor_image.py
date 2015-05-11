import requests
import time
import json
fail = 0
def get(ID):
    global fail
    print(ID)
    try:
        c = {'PHPSESSID': 'fsu1uh1b1ap8r5pj894qm11m53'}
        d = {'SNo':ID, 'act':'course'}
        r = requests.post('https://preceptor.nctu.edu.tw/showStuInfo.php', verify=False, cookies=c, data=d)
        f = open('preceptor/info/'+ID+'.html', 'w')
        f.write(r.text.encode('latin1', 'ignore').decode('big5'))
        f.close()
        r = requests.post('https://preceptor.nctu.edu.tw/showpic.php?stdno_pic=-1', verify=False, cookies=c, stream=True)
        f = open('preceptor/info/'+ID+'.jpg', 'wb')
        f.write(r.raw.read())
        f.close()
        flai = 0
    except:
        time.sleep(10)
        fail += 1
        if fail >= 10:
            f = open('preceptor/info/fail', 'w')
            f.write(ID+'\n')
            f.close()
            fail = 0
            return
        get(ID)

if __name__ == '__main__':
    r = requests.get('http://localhost:8000/api/studentid/')
    s = json.loads(r.text)
    stop = 0
    for stu in s:
        ID = stu['id']
        if stop == 0:
            if ID == '0111279':
                get(ID)
                stop = 1
        else:
            get(ID)
