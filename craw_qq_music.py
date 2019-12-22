import requests
import os
import json


class QQMusic(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7'
                             '1.0.3578.80 Safari/537.36'}

    def __init__(self):
        pass

    def get_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                return None
        except TimeoutError:
            print("网络不佳，请重新下载")
            return None
        except Exception as err:
            print("请求出错：", err)
            return None

    def download(self, data, sing_name):
        try:
            save_path = 'music/'+sing_name+'.m4a'
            true_path = os.path.abspath(save_path)
            try:
                print("下载中.....")
                with open(save_path, 'wb') as f:
                    f.write(data)
                print("{}已下载至{}".format(sing_name, true_path))
            except Exception as err:
                print("文件写入出错:", err)
                return None
        except Exception as er:
            print("文件music找不到\n请重新下载", er)
            return None

    def qq_music_api(self):
        print("\n", "{:^30}".format("正在使用QQ音乐VIP下载器"))
        while True:
            song_name = input("\n请输入歌名>>").strip()
            print("正在努力寻找资源.........")
            if song_name == '':
                continue
            elif song_name == 'q':
                print("退出QQ音乐下载")
                break
            url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1' \
                   '&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=' + song_name
            try:
                rest1 = self.get_request(url1)
                js_of_rest1 = json.loads(rest1.text.strip('callback()[]'))
                js_of_rest1 = js_of_rest1['data']['song']['list']
            except TimeoutError:
                print("网络异常，请重新下载")
                continue
            except:
                print("检测到异常，请重新下载")
                continue
            medias = []
            song_mid = []
            src = []
            song_names = []
            singers = []
            for rest in js_of_rest1:
                try:
                    medias.append(rest['media_mid'])
                    song_mid.append(rest['songmid'])
                    song_names.append(rest['songname'])
                    singers.append(rest['singer'][0]['name'])
                except :
                    print('检测到错误，资源可能与您预期不符')
                    index = input("\n退出下载请按q，继续下载请直接回车>>").strip()
                    if index == 'q':
                        return
                    elif index == '':
                        continue
                    else:
                        print("输入不规范，请重新下载")
                        return

            for n in range(0, len(medias)):
                try:
                    url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=' \
                           '205361747&songmid=' + song_mid[n] + '&filename=C400' + medias[n] + '.m4a&guid=6612300644'
                    rest2 = self.get_request(url2)
                    js_of_rest2 = json.loads(rest2.text)
                    vkey = js_of_rest2['data']['items'][0]['vkey']
                    src.append(
                        'http://dl.stream.qqmusic.qq.com/C400' + medias[n] + '.m4a?vkey=' + vkey + '&guid=6612300644&uin=0&fromtag=66')
                except TimeoutError:
                    print("网络不佳，请重新下载")
                except:
                    print("检测到异常，请重新下载")
                    break
            print("为你找到以下内容".center(30, '*'))
            print("序号      ", "歌手    -     歌名")
            for m in range(0, len(src)):
                print(str(m + 1) + '    ' + song_names[m] + ' - ' + singers[m] + '.m4a')
            song_index = int(input("请选择序号>>").strip())
            if song_index < 0:
                print("退出QQ音乐下载")
                break
            try:
                song_data = self.get_request(src[song_index - 1])
                data = song_data.content
                self.download(data, song_names[song_index-1])
            except Exception as er:
                print("检测到异常，请重新下载 ", er)


if __name__ == '__main__':
    qq_API = QQMusic()
    print("{:^30}".format("欢迎使用VIP音乐破解"))
    if not os.path.exists("./music"):
        os.mkdir("./music/")
    while True:
        try:
            qq_API.qq_music_api()
        except:
            print("请检查输入是否符合规范")
