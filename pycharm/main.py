import requests
import re
import json



def getOldinfo(input):
    # 先解决 config.captcha中的内容
    temp=re.findall(r"oldInfo: ({[\s|\S]*}),[\s]*tipMsg",input)
    return temp

def getDef(input):
    temp = re.findall(r"def = ({[\s|\S]*});[\s]*var vm", input)
    return temp

def gethasFlag(input):
    temp = re.findall(r"hasFlag: '([\s|\S]*)',[\s]*setting", input)
    return temp

def valid(info):
    if info['sfjcbh']==0:
        info['jcbhlx']=''
        info['jcbhrq']=''

    if info['sfcyglq']==0:
        info['gllx'] = ''
        info['glksrq'] = ''

    if info['sfcxtz'] == 0:
        info['sfyyjc'] = 0

    if info['sfyyjc'] == 0:
        info['jcjgqr'] = 0
        info['jcjg'] = ''

    if info['sfcxzysx'] == 0:
        info['qksm'] = ''

    if info['sfzgn'] == 1:
        info['szcs'] = ''
        info['szgj'] = ''

    if info['sfjxhsjc'] != 1:
        info['hsjcrq'] = ''
        info['hsjcdd'] = ''
        info['hsjcjg'] = 0

    if info['sfjxhsjc'] != 1:
        info['szxqmc'] = ''
    else:
        info['bzxyy'] = ''

    if info['sfjzdezxgym'] != 1:
        info['jzdezxgymrq'] = ''

    if info['sfjzxgym'] != 1:
        info['jzxgymrq'] = ''



if __name__ == '__main__':
    loginheader={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7'
    }

    getcookies={
        'eai-sess' : 'o8tpte3v2cbeu2694scvtl6bc4',
        'UUkey' : '4b950f3152a81996e837685c7d04228f',
        'Hm_lvt_48b682d4885d22a90111e46b972e3268' : '1629463788, 1629477294',
        'Hm_lpvt_48b682d4885d22a90111e46b972e3268' : '1629477478'
    }
    geturl='https://wfw.scu.edu.cn/ncov/wap/default/index'
    r=requests.get(geturl,headers=loginheader,cookies=getcookies);
    if r.status_code == requests.codes.ok:
        hasFlag=gethasFlag(r.text)[0]
        if hasFlag=='1':
            print('\n已经完成过打卡，每天只能打卡一次\n')
        else:
            print("\nget result is \n"+r.text)
            #getOldinfo
            oldInfo=getOldinfo(r.text)
            oldInfo=json.loads(oldInfo[0])
            print("\n oldinfo is :\n")
            print(oldInfo)

            defInfo=getDef(r.text)
            defInfo=json.loads(defInfo[0])
            print("\n definfo is :\n")
            print(defInfo)

            #构成打卡信息
            uploadinfo=defInfo.update({'szgjcs': ''})
            uploadinfo['geo_api_info']=oldInfo['geo_api_info']
            uploadinfo['address']=oldInfo['geo_api_info']['formattedAddress']
            uploadinfo['province']=oldInfo['geo_api_info']['addressComponent']['province']
            uploadinfo['city']=oldInfo['geo_api_info']['addressComponent']['city']
            uploadinfo['area']=uploadinfo['province']+' '+uploadinfo['city']+' '+oldInfo['geo_api_info']['addressComponent']['district']

            valid(uploadinfo)
            uploadurl=''
            r=requests.post(uploadurl,json=json.dumps(uploadinfo),cookies=getcookies)
            if r.status_code==requests.codes.ok:
                print('\n提交信息成功！\n')
        



