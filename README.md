# Typora 笔记助手

## 前言

> 由于 typora 无比优雅的 Markdown 输入体验，我决定使用她来记录笔记。

### 优雅的 typora

她的魅力在于：

- 一见倾心的 Markdown 输入语法，类似但完全超越印象笔记；
- 令人着迷的排版技术，包括 Markdown、LateX、Mermaid；
- 令人心醉的图片、链接嵌入功能；
- 令人愉悦的主题外观设计。

### 目标

为 typora 编写一套笔记工具：

- 配合 typora + icloud 实现 Markdown 笔记书写管理同步功能。

目前借助 icloud 已经能够实现：

- 笔记书写
- 笔记同步

现阶段缺乏的重要功能：

- 笔记目录管理
- 笔记快速打开
- 笔记快速新建
- 笔记内容全局搜索
- 笔记附件快捷插入

## 需求细化

需求列表：

- [ ] 工具设置
  - [ ] 笔记根目录
  - [ ] 单击还是双击调用笔记

- [x] 笔记目录结构显示
  - [x] 去除其他不应该显示文件
  - [x] 启动时全部展开
  - [ ] 笔记目录自动更新
    - [ ] 点击按钮更新
    - [ ] 可感知来自外部的文件变化
- [x] 最近打开的笔记显示
  - [x] 按最近时间显示打开的笔记方便调用
- [x] 笔记快速打开
  - [x] 在目录中单击
  - [x] 在最近打开中单击
  - [ ] 快捷键调用笔记工具
- [ ] 在笔记目录中操作笔记
  - [ ] 新建笔记
  - [ ] 删除笔记
  - [ ] 重命名笔记
    - [ ] 保持与资源文件、链接联动
  - [ ] 通过按钮转换编辑模式或者右键，进行上述操作
- [x] 笔记搜索
  - [x] 笔记内容全局搜索显示
  - [x] 点击打开笔记
  - [ ] 笔记文件名匹配
- [ ] 笔记附件插入
  - [ ] 附件文件自动生成链接一键插入
- [ ] 整理开源
  - [x] 在 Github 开源
  - [ ] 编写简介文档以hexo形式显示。

主要是目录显示和内容全局搜索两大块。

## 使用说明

### 要求

- Python3
- find、grep命令
- Mac OS

### 测试通过

环境：
- python 3.6.5
- MacOS 12.12/12.13

### 运行

1. 设置 Typora 为md文件默认的打开程序。
2. 打开 note_helper.py 文件，在 root_path 填入正确的笔记根目录。
3. `python note_helper.py`运行程序。

### 截图

![文件目录界面](http://wx2.sinaimg.cn/mw690/0060lm7Tly1ftzcxc8jxsj30rs0t0jvm.jpg)
![搜索界面](http://wx4.sinaimg.cn/mw690/0060lm7Tly1ftzcxcs1rtj30rs0t00xi.jpg)

## 进展

笔记目录部分完成，目录功能基本可用。

> 截至  2018-08-03 19:40:18

笔记搜索部分完成，内容全局搜索基本可用。

> 截止 2018-08-06 01:28:27

#### 已完成功能

- 笔记的目录显示和点击打开
- 最近打开列表
- 笔记内容全局搜索显示

### 开发相关

- 编程语言使用 python3 。
- GUI库使用 tkinter。
- 目录结构展示使用了Treeview。

建议想认真开发GUI程序的别使用tkinter，用qt比较靠谱。
tkinter的资料太少了，接口很难找。

### 历史版本

#### V0.1

时间
- 2018-08-06 01:28:27

功能
- 基础的文件目录浏览
- 基础的内容全局搜索

### 遇到的坑

#### IPython console 无法运行 Tkinter

发现 Sypder 里的 IPython console 无法运行 Tkinter 程序。

#### subprocess开启shell

`p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)`
subprocess要开启shell，才能输入多个命令。默认用的不是系统的解释器。

#### grep -r *.md 不能递归

`cmd = 'cd "' + self.app.root_path + '" && grep -Erni "' + text + '" *.md 2>/dev/null’`

发现直接用grep加上 *.md 找的是当前目录，`-r`也没用。

换 find：

`find . -type f -name "*.md" | awk '{print "\""$0"\""}'| xargs grep "联盟"`

`cmd = '''find "''' + self.app.root_path + '''" -type f -name "*.md" | awk \'{print "\\""$0"\\""}\'| xargs grep -Eni "''' + text + '''"'''`

#### Anaconda 的 python 和 brew 里的不一样

brew里的python有问题，note里的字向上偏移了。


