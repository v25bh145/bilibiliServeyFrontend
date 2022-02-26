import getopt, sys
import requests, json

headers={'cookie': '{}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'referer': 'https://www.bilibili.com/v/fashion/makeup/?spm_id_from=333.5.b_7375626e6176.2',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site'
         }

def getVideoByUp(up, pn, ps):
    url = 'https://api.bilibili.com/x/space/arc/search?mid=%s&pn=%s&ps=%s'%(up, pn, ps)
    response = requests.get(url,headers=headers).text
    result = json.loads(response)
    return result

def getFans(up):
    result = {}
    for i in range(1, 6):
        url = 'https://api.bilibili.com/x/relation/followers?vmid=%s&pn=%d&ps=50'%(up, i)
        response = requests.get(url,headers=headers).text
        data = json.loads(response)
        result[i] = data['data']
    return result

def getUpInfo(up):
    url = 'http://api.bilibili.com/x/web-interface/card?mid=%s&photo=false'%(up)
    response = requests.get(url,headers=headers).text
    result = json.loads(response)
    return result

def getVideoByDepartment(tid, pn, ps):
    url = 'http://api.bilibili.com/x/web-interface/dynamic/region?rid=%s&pn=%s&ps=%s'%(tid, pn, ps)
    response = requests.get(url,headers=headers).text
    result = json.loads(response)
    print(result)
    return result

def main():
    # 参数处理
    action = up = tid = pn = ps = ''
    opts, args = getopt.getopt(sys.argv[1:], '-a:-u:-t:', ['action=', 'up=', 'tid=', 'pn=', 'ps='])
    for opt_name, opt_value in opts:
        if opt_name in ('-a', '--action'):
            action = opt_value
        elif opt_name in ('-u', '--up'):
            up = opt_value
        elif opt_name in ('-t', '--tid'):
            tid = opt_value
        elif opt_name == '--pn':
            pn = opt_value
        elif opt_name == '--ps':
            ps = opt_value

    if action == 'getVideoByUp':
        print(getVideoByUp(up, pn, ps))
    elif action == 'getFans':
        print(getFans(up))
    elif action == 'getUpInfo':
        print(getUpInfo(up))
    elif action == 'getVideoByDepartment':
        print(getVideoByDepartment(tid, pn, ps))
    return 0

if __name__ == '__main__':
    main()