from tkinter import *
import tkinter.messagebox as messagebox
import os
import win32api
import win32con
from mutagen import File
import datetime
import pymysql


class music():
    __musicPlayPath = 'D:\KGMusic\KuGou.exe'
    # 全部音乐列表
    __musicDefaultList = []
    # 搜索
    musicCurList = []
    # 点歌列表
    __userSelMusicList = []
    # 全部音乐信息列表
    __allMusicList = []
    # 活跃度列表
    __musicActivityList = []

    def __init__(self, musicPath):
        self.__musicPath = musicPath

    def database(self):
        con = pymysql.connect(
            host='localhost',
            user='******',
            passwd='*****',
            db='****'
        )
        cursor = con.cursor()
        return cursor, con

    def sort(self, activity):
        music.__musicActivityList.clear()
        # 数据库查询
        database, con = self.database()
        # 数据库
        sql = 'select * from activity'
        database.execute(sql)
        data = database.fetchall()
        print(data)
        dic = {}
        for i in data:
            print(i[0])
            b = i[0].split('|')
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            e = datetime.datetime.strptime(b[1].strip(), '%Y-%m-%d')
            d = datetime.datetime.strptime(now_time, '%Y-%m-%d')
            c = (d - e).days
            if c < activity:
                dic[b[0]] = dic.setdefault(b[0], 0) + 1
            allList = dic
            sort_list = sorted(allList.items(), key=lambda item: item[1], reverse=True)
        num = 1
        for e in sort_list:

            base = 'TOP{}   '.format(num) + e[0] + '               累计点播次数{}'.format(e[1])
            music.__musicActivityList.append(base)
            if num > 9:
                break
            num += 1
        database.close()
        return music.__musicActivityList

    def delUserMusicListItem(self, item):
        if item in music.__userSelMusicList:
            music.__userSelMusicList.remove(item)
            database, con = self.database()
            # 数据库
            print(item)
            item = '\'' + item + '\''
            sql = 'delete from ordermusic where title={0}'.format(item)
            database.execute(sql)
            data = database.fetchall()
            print(data)
            con.commit()

            messagebox.showinfo('提示', '删除成功！')

    def addUserMusicListItem(self, item):
        database, con = self.database()
        sql = 'insert into ordermusic value({0})'.format(item)
        try:
            database.execute(sql)
            con.commit()
            data = database.fetchall()
            print(type(data[0]))
        except:
            messagebox.showinfo('失败', '点歌列表中存在歌曲 \"' + item + '\"!')

        if not (item in music.__userSelMusicList):
            music.__userSelMusicList.append(item)

            messagebox.showinfo('成功', '已经添加歌曲 \"' + item + '\"!')
            print(music.__userSelMusicList)

    def readUserMuslicList(self):
        return music.__userSelMusicList

    def getSerachList(self):
        return music.musicCurList

    def setDefaultMuslic(self):
        music.__musicDefaultList = self.readMusicFromDisk()

    def readDefaultMuslic(self):
        return music.__musicDefaultList

    # 搜索
    def getMusicListByUserKey(self, searchTxt, classes):

        if str(searchTxt).__len__() < 1:
            music.musicCurList = music.__musicDefaultList[:]
            return
        music.musicCurList.clear()
        print("搜索")
        print(music.__allMusicList)
        for m in music.__allMusicList:
            print(m)
            if searchTxt == str(m[classes]):
                print("加入成功")
                print(m)
                music.musicCurList.append(m['title'])
            else:
                print("没找到")

    def loadUserMusicListFromDisk(self):
        # 数据库读取点歌列表
        database, con = self.database()
        sql = 'select * from ordermusic'
        database.execute(sql)
        data = database.fetchall()
        ordermusic = []
        for i in data:
            ordermusic.append(i[0])
        music.__userSelMusicList = ordermusic

    # 读取音乐列表
    def readMusicFromDisk(self):
        music.__musicDefaultList = [d for d in os.listdir(self.__musicPath) if d.upper().endswith(".mp3") >= 0]
        print(music.__musicDefaultList)

        self.readMusicInformation()
        return music.__musicDefaultList

    # 取全部音乐信息
    def readMusicInformation(self):

        # 本地从文件夹里获取音乐信息, 数据转换为可以插入数据库的数据
        url_base = 'D:\\音乐\\'
        for i in music.__musicDefaultList:
            a = {}
            b = ''

            url = url_base + i
            afile = File(url)
            author = afile.tags["TPE1"].text[0]  # 作者
            year = afile.tags["TDRC"].text[0]  # 年代
            a['author'] = author
            a['year'] = year
            a['title'] = i
            b = '(\''+str(i) + '\',\'' + str(author) + '\',' + str(year) + ')\''
            print(b)
            music.__allMusicList.append(a)

        print(music.__allMusicList)

    def playMusic(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        win32api.ShellExecute(0, 'open', music.__musicPlayPath,
                              '\"' + self.__musicPath + value + '\"', '', 1)

    def addMusicActivity(self, value):

        tmpAry = value + '|'
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        data = '\''+tmpAry+time+'\''
        database, con = self.database()
        # 数据库
        sql = 'insert into activity value({0})'.format(data)
        database.execute(sql)
        con.commit()
        database.close()


class gui(music):

    def __init__(self, winName):
        self.winName = winName

        self._music__musicPath = 'D:\\音乐\\'

        super().__init__(self._music__musicPath)
        self.lbx = StringVar()
        self.var = StringVar()

    def sort1(self):
        self.lbx.set(self.sort(7))

    def sort2(self):
        self.lbx.set(self.sort(30))

    # 点歌
    def addMusicToUserList(self):
        index = int(self.listbox1.curselection()[0])
        value = self.listbox1.get(index)
        print(value)
        # 加入点歌列表数据库
        self.addUserMusicListItem(value)
        # 加入活跃度数据库
        self.addMusicActivity(value)

    def UpdateUserMusicList(self):
        self.lbx.set(self.readUserMuslicList())

    def searchMusic(self, event):
        w = event.widget
        txt = w.get()

        classes = self.var.get()

        self.getMusicListByUserKey(txt, classes)
        self.lbx.set(self.getSerachList())

    def delUserMusic(self):
        index = int(self.listbox1.curselection()[0])
        value = self.listbox1.get(index)
        self.delUserMusicListItem(value)

        self.lbx.set(self.readUserMuslicList())
        # self.saveUserMusicListToDisk()

    def allmusic(self):
        self.lbx.set(self.readDefaultMuslic())

    def initForm(self):
        self.winName.title("KTV点歌系统")
        self.winName.geometry('700x480+10+10')
        self.winName['bg'] = "pink"
        self.winName.resizable(width=False, height=False)

        self.btn1 = Button(self.winName, text='全部歌曲', bg='lightblue', command=self.allmusic)
        self.btn1.grid(row=1, column=1)
        self.btn2 = Button(self.winName, text='点歌列表', bg='lightblue', command=self.UpdateUserMusicList)
        self.btn2.grid(row=1, column=2)
        self.btn3 = Button(self.winName, text='添加歌曲到点歌列表', bg='lightyellow', command=self.addMusicToUserList)
        self.btn3.grid(row=1, column=3)
        self.btn4 = Button(self.winName, text='删除歌曲', bg='lightyellow', command=self.delUserMusic)
        self.btn4.grid(row=1, column=4)
        self.btn5 = Button(self.winName, text='周活TOP10', bg='lightyellow', command=self.sort1)
        self.btn5.grid(row=2, column=1)
        self.btn6 = Button(self.winName, text='月活TOP10', bg='lightyellow', command=self.sort2)
        self.btn6.grid(row=2, column=3)

        self.lab1 = Label(self.winName, text='搜索：')
        self.lab1.grid(row=1, column=8)

        self.r1 = Radiobutton(self.winName, text='按歌名搜索', variable=self.var, value='title')
        self.r1.grid(row=1, column=12)
        self.r2 = Radiobutton(self.winName, text='按歌手搜索', variable=self.var, value='author')
        self.r2.grid(row=2, column=12)
        self.r3 = Radiobutton(self.winName, text='按年代搜索', variable=self.var, value='year')
        self.r3.grid(row=3, column=12)

        self.txt1 = Entry(self.winName, width=20)
        self.txt1.bind('<Return>', self.searchMusic)
        self.txt1.grid(row=1, column=9)

        self.scrollbar = Scrollbar()
        self.scrollbar.grid(row=4, column=13, rowspan=13, sticky='NS')

        self.listbox1 = Listbox(self.winName, listvariable=self.lbx, width=90, height=25,yscrollcommand=self.scrollbar.set)
        self.setDefaultMuslic()
        self.lbx.set(self.readDefaultMuslic())
        self.listbox1.bind('<Double-Button-1>', self.playMusic)
        self.listbox1.grid(row=4, column=1, columnspan=12)
        self.scrollbar.config(command=self.listbox1.yview)
        self.loadUserMusicListFromDisk()



if __name__ == '__main__':
    tk = Tk()
    form = gui(tk)
    form.initForm()
    tk.mainloop()