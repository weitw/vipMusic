import requests
import os
import json
import re


class KuGou(object):
    def __init__(self):
        pass

    def download(self):
        print("\n", "{:^30}".format("正在使用酷狗VIP下载器"))
        while True:
            song_name = input("\n请输入歌名>>").strip()
            if song_name == '':
                continue
            elif song_name == 'q':
                print("\n退出酷狗音乐下载")
                break
            print("\n正在努力寻找资源......")
            url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407470964083509348_1534929985284&keyword={}&" \
                  "page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filte" \
                  "r=0&_=1534929985286".format(song_name)
            try:
                res = requests.get(url).text
                js = json.loads(res[res.index('(') + 1:-2])
                data = js['data']['lists']
            except TimeoutError:
                print("\n网络不佳，请重新下载")
                break
            except:
                print("未找到资源QAQ")
                break
            print("为你找到以下内容".center(30, '*'))
            print("{:6}{:30}".format("序号", "歌手  -  歌名"))
            try:
                for i in range(10):
                    print(str(i + 1) + "    " + str(data[i]['FileName']).replace('<em>', '').replace('</em>', ''))
                number = int(input("\n请选择歌曲序号>> "))
                if number <= 0:
                    print("请检查输入是否符合规范\n退出酷狗下载")
                    break
                try:
                    name = str(data[number - 1]['FileName']).replace('<em>', '').replace('</em>', '')
                    fhash = re.findall('"FileHash":"(.*?)"', res)[number - 1]
                    hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + fhash
                    hash_content = requests.get(hash_url)
                    play_url = ''.join(re.findall('"play_url":"(.*?)"', hash_content.text))
                    real_download_url = play_url.replace("\\", "")
                except TimeoutError:
                    print("网络不佳，请重新下载")
                    break
                try:
                    save_path = "./music/"+name+".mp3"
                    true_path = os.path.abspath(save_path)
                    print("下载中.....")
                    with open("./music/"+name+".mp3", "wb")as fp:
                        fp.write(requests.get(real_download_url).content)
                    print("{}已保存至{}".format(name, true_path))
                except:
                    print("未找到文件夹music\n退出酷狗下载")
            except:
                print("异常错误，请重新下载")


if __name__ == '__main__':
    kg_API = KuGou()
    print("{:^30}".format("欢迎使用VIP音乐破解"))
    if not os.path.exists("./music"):
        os.mkdir("./music/")
    while True:
        try:
            kg_API.download()
        except:
            print("请检查输入是否符合规范")
