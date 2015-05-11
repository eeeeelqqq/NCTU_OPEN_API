import requests
import time
import json
fail = 0
def get(_id):
    global fail
    print(_id)
    try:
        c = {'PHPSESSID': 'fsu1uh1b1ap8r5pj894qm11m53'}
        d = {'act': 'score', 'SNo': str(_id)}
        r = requests.post('https://preceptor.nctu.edu.tw/showStuCourse.php',verify=False,cookies=c,data=d)
        text = r.text.encode('latin1', 'ignore').decode('big5')
        f = open('preceptor/score/'+str(_id), 'w')
        f.write(text)
        f.close()
        fail = 0
    except:
        fail += 1
        if fail >= 2:
            f = open('preceptor/score/fail', 'a')
            f.write(str(_id)+'\n')
            f.close()
            return
        time.sleep(10)
        get(_id)

if __name__ == '__main__':
    r = requests.get('http://localhost:8000/api/studentid/')
    s = json.loads(r.text)
    for stu in s:
        _id = stu['id']
        name = stu['name']
        get(_id)
