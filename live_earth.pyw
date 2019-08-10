# 向日葵8号是在东七区左右 所以黑天会比咱们的时间早 调个时间差 这样比最新数据晚大概一个半小时 可以做的和东8区的时间对应上
# 比最新时间早 夜十二点刚好是全黑

import win32gui, win32con, win32api
import urllib.request
import time
import re
from PIL import Image
import os
import threading
import time
import wx
import wx.adv

stop = False  # 结束


class live_earth():
    def __init__(self):
        self.base_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/"  # 官网图片地址前半部分
        self.cwd = os.getcwd()  # 当前目录
        self.main()
    
    # 更新壁纸
    def set_desktop(self, pic_path):
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "0")  # 2拉伸适应桌面,0桌面居中
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)
    
    # 下载图片
    def down_pic(self, ):
        try:
            # res = str(urllib.request.urlopen('https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json?uid=' + str(time.time())).read())
            # ask_time=re.findall('"date":"(.+?)",',res)[0]
            # ask_time=time.localtime(time.mktime(time.strptime(ask_time, '%Y-%m-%d %H:%M:%S')))
            ask_time = time.localtime(int(time.time()) // 600 * 600 - 3600 * 10 + 2400)
            pic_name_base = self.cwd + '\\download\\data\\' + time.strftime('%H%M', ask_time)
            pic_name_base2 = self.cwd + '\\download\\' + time.strftime('%H%M', ask_time)
            base_url2 = self.base_url + time.strftime('%Y/%m/%d/%H%M00', ask_time)
            pic_name_list = ['_0_0.png', '_0_1.png', '_1_0.png', '_1_1.png']
            place_list = [(0, 0), (0, 550), (550, 0), (550, 550)]
            result = Image.new('RGB', (1100, 1100))
            for i in range(4):
                conn = urllib.request.urlopen(base_url2 + pic_name_list[i])
                with open(pic_name_base + pic_name_list[i], 'wb') as f:
                    f.write(conn.read())
                ims = Image.open(pic_name_base + pic_name_list[i])
                result.paste(ims, box=place_list[i])
            result.save(pic_name_base2 + '.png')
            print(pic_name_base2 + ' Saved!')
            return pic_name_base2 + '.png'
        except:
            return False
    
    def main(self, ):
        if not os.path.exists(self.cwd + "/download"):
            os.mkdir(self.cwd + "/download")
        if not os.path.exists(self.cwd + "/download/data"):
            os.mkdir(self.cwd + "/download/data")
        
        while True:
            pic_name = self.down_pic()
            if pic_name != False:
                self.set_desktop(pic_name)
            for i in range(120):
                if stop:
                    break
                time.sleep(5)
            if stop:
                break


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "earth.ico"  # 图标地址
    ID_ABOUT = wx.NewId()  # 菜单选项“关于”的ID
    ID_EXIT = wx.NewId()  # 菜单选项“退出”的ID
    TITLE = "实时桌面壁纸"  # 鼠标移动到图标上显示的文字
    
    def __init__(self):
        threading.Thread.__init__(self)
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.on_about, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.on_exit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
    
    # “关于”选项的事件处理器
    def on_about(self, event):
        wx.MessageBox(
            '                   使用说明\n'
            '点击运行即可\n'
            '嘿兄弟 你看起来很不好，你最好在天黑前找点吃的\n\n'
            '版本: 1.0\n'
            '最后更新日期：2019-8-6\n'
            '本软件仅用于学习,研究.绝不会用于商业用途',
            "关于")
    
    # “退出”选项的事件处理器
    def on_exit(self, event):
        global stop
        stop = True
        wx.Exit()
        exit(0)
    
    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu
    
    # 获取菜单的属性元组
    def getMenuAttrs(self):
        return [
            ('关于', self.ID_ABOUT),
            ('退出', self.ID_EXIT)
        ]


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()  # 显示系统托盘图标


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True


if __name__ == "__main__":
    threading.Thread(target=live_earth).start()
    app = MyApp()
    app.MainLoop()
