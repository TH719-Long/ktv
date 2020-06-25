# KTV模拟点歌系统

## 开发环境

python 3.7

mysql 5.7

pymysql 0.9.3

win32api 228（控制电脑软件）

mutagen 1.44.0（音乐文件解析）

tkinter（GUI库）

## 功能清单

- 对曲库进行管理
- 能够展现曲库中的歌曲名称
- 并按歌名、演唱者、年代等进行查询
- 并能够对歌曲进行播放（MP3、MP4等格式）
- 统计点歌的周、月度TOP10排行。

## 页面展示

![image-20200616174033567](https://github.com/trammels-zjx/ktv/blob/master/img/image-20200616174033567.png)

**活跃度**

![image-20200616174115091](https://github.com/trammels-zjx/ktv/blob/master/img/image-20200616174115091.png)



## 注意事项

1. 本项目音乐文件路径为	D:\\音乐\\
2. 连接数据库的信息已处理
3. 本项目实现了数据库和本地读取两种方式实现（本地读取代码见注释）
