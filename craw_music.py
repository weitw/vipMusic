# --*-- coding:utf-8 --*--
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 输入框回车
from selenium.webdriver.common.by import By  # 与下面的2个都是等待时要用到
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 异常处理
from selenium.webdriver.chrome.options import Options
import re
import os
import json


class NetEaseCloud(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def __init__(self):
        pass
        # self.download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)

    def get_html(self, request_url):  # 得到页面的html
        try:
            response = requests.get(request_url, headers=NetEaseCloud.headers, timeout=20)
            if response.status_code == 200:
                return response
        except TimeoutError:
            print("请求超时！")
            return None
        except Exception as er:
            print("其他错误：", er)
            return None

    def get_id(self):
        try:
            song_id = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//body/div[@class="g-bd"]/div/div[2]/div[2]/div/div/div[*]/div[2]/div/div/a')))
            title = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//body/div[@class="g-bd"]/div/div[2]/div[2]/div/div/div[*]/div[2]/div/div/a/b')))
            author = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//body/div[@class="g-bd"]/div/div[2]/div[2]/div/div/div[*]/div[4]/div/a')))
            ids = []
            titles = []
            authors = []
            num = 1
            print("为你找到以下内容".center(30, '*'))
            print("序号     ", "歌名                              ", "         歌手", "        歌曲链接")
            for i in range(0, len(song_id)):
                try:
                    ids.append(song_id[i].get_attribute("href"))   # 这儿是歌曲的id
                    titles.append(title[i].get_attribute('title'))  # 这是歌名
                    authors.append(author[i].get_attribute('textContent'))  # 这是歌手
                    print(num, "     ", titles[i], "     ", authors[i], "    ", ids[i])
                    num += 1
                except:
                    pass
            # print("没到这儿吗")
            is_index = int(input("\n选择下载序号>>").strip())
            if is_index < 0:
                print("您已取消该歌曲的下载")
                return None
            song_id = re.compile('htt.*?id\=(\d+)').findall(ids[is_index-1])[0]  # 将歌曲id匹配出来
            song_name = titles[is_index-1]
            # print("正在下载......")
            return song_id, song_name
        except TimeoutException:
            print("网络不佳，请重新下载")
            return None
        except NoSuchElementException:
            print("没有找到相关资源QAQ")
            return None
        except Exception as er:
            print("检测到异常错误，请重新下载： ", er)
            return None

    def download(self, song_id, song_name):
        # song_id, song_name = NetEaseCloud.get_id()
        download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)  # 歌曲下载的接口
        try:
            song_html = self.get_html(download_url)  # 访问下载页
            song_data = song_html.content  # 得到下载页的html.content(即歌曲数据的字节)
        except TimeoutError:
            print("检测到网络异常\n退出网易云音乐下载")
            return
        except:
            print("检测到异常\n退出网易云音乐下载")
            return
        try:
            save_path = 'music/{}.mp3'.format(song_name)
            true_path = os.path.abspath(save_path)  # 绝对路径
            print("下载中......")
            with open(save_path, 'wb') as f:
                try:
                    f.write(song_data)
                    print("{}已保存至{}".format(song_name, true_path))
                except Exception as er:
                    print("写入失败：", er)
        except Exception as err:
            print("文件找不到目录music：", err)

    def test(self, song_name):
        songs_name = []
        remove_str = ['/', '\\']
        for name in song_name:
            if name not in remove_str:
                songs_name.append(name)
            else:
                name = '&'
                songs_name.append(name)
        song_string = ''.join(songs_name)
        return song_string

    def net_ease_cloud_api(self):
        print("\n", "{:30}".format("正在使用网易云音乐VIP下载器"))
        try:
            url = "https://music.163.com/#/search/m/?s=长安忆&type=1"
            driver.get(url)
        except:
            print("网络连接异常！")
            return   # 利用return阻断程序
        try:
            driver.switch_to.frame('g_iframe')
            while True:
                name_tar = input("\n请输入歌名>>").strip()
                print("\n正在努力寻找资源.....")
                if name_tar == 'q':
                    print("\n退出网易云音乐下载")
                    break
                elif name_tar == '':
                    continue
                else:
                    try:
                        input_box = wait.until(
                            EC.element_to_be_clickable((By.XPATH, '//body/div[@class="g-bd"]/div/div/input')))
                        input_box.clear()
                        input_box.send_keys(name_tar)
                        input_box.send_keys(Keys.ENTER)
                    except NoSuchElementException:
                        print("\n没有找到相关资源QAQ")
                        return   # 设置阻断
                    song_id, song_name = self.get_id()  # 此时的song_name可能含有字符/,写文件时会报路径错误，所以要想验证
                    if song_id is None or song_name is None:
                        break  # 这个None是用户不想下载时返回的
                    else:
                        song_name = self.test(song_name)  # 若含有/或者\则转化为&
                        self.download(song_id, song_name)
        except Exception as er:
            print("检测到异常错误\n退出网易云音乐下载 ", er)


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
    net_API = NetEaseCloud()
    kg_API = KuGou()
    qq_API = QQMusic()
    print("{:^30}".format("欢迎使用VIP音乐破解"))
    if not os.path.exists("./music"):
        os.mkdir("./music/")
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
        wait = WebDriverWait(driver, 15)
    except Exception as e:
        print("请先安装最新版Chrome浏览器!", e)
    while True:
        try:
            print("\n1   酷狗音乐  (默认下载器)\n2   网易云音乐\n3   QQ音乐")
            player = input("请选择播放源>>").strip()
            if player == 'q':
                print("退出VIP音乐破解")
                exit()
            elif player == '':
                continue
            elif int(player) not in [1,2,3]:
                print("请正确输入序号\n退出VIP下载")
                break
            elif int(player) == 1:
                kg_API.download()
            elif int(player) == 2:
                net_API.net_ease_cloud_api()
            elif int(player) == 3:
                qq_API.qq_music_api()
        except:
            print("请检查输入是否符合规范")


