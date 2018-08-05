# -*- coding: utf-8 -*-

import os
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue

class App(object):
    def __init__(self, master, root_path):
        self.root_path = root_path
        self.nodes = dict()
        self.md_file = dict()
        self.recent_file = dict()
        self.recent_node = dict()
        self.search_queue = queue.Queue()
        self.note = ttk.Notebook(master, height = 400,width = 400, padding=[0,0,0,0])
        note = self.note
        '''file frame'''
        frame_file = tk.Frame(note)
        note.add(frame_file, text = '文件')
        note.pack(fill='both', expand=True)
        frame_file.columnconfigure(0, weight=1) # column with treeview
        frame_file.rowconfigure(0, weight=1) # row with treeview
        master.geometry('500x500')
        self.file_tree = ttk.Treeview(frame_file, height=20)
        file_tree = self.file_tree
        file_tree.heading('#0', text='文档目录', anchor='w')
        file_tree.grid(row=0, column=0, sticky='nsew')
        file_tree.bind('<<TreeviewOpen>>', self.open_file_node)
        file_tree.bind('<ButtonRelease-1>', self.file_click)
        self.recent_tree = ttk.Treeview(frame_file, height=5)
        recent_tree = self.recent_tree
        recent_tree.heading('#0', text='最近打开', anchor='w')
        recent_tree.grid(row=3, column=0,sticky='nsew')
        recent_tree.bind('<ButtonRelease-1>', self.recent_click)
        '''search frame'''
        frame_search = tk.Frame(note)
        note.add(frame_search, text = '搜索')
        frame_search.columnconfigure(0, weight=1) # column with treeview
        frame_search.rowconfigure(1, weight=1) # row with treeview
        self.search_text = tk.StringVar()
        search_text = self.search_text
        search_text.trace("w", lambda name, index, mode,
                          search_text=search_text: self.search_entry_callback(search_text))
        self.search_entry = ttk.Entry(frame_search, textvariable=search_text)
        search_entry = self.search_entry
        search_entry.grid(row=0, column=0, sticky='nsew')
        self.search_tree = ttk.Treeview(frame_search, height=17)
        search_tree = self.search_tree
        search_tree.heading('#0', text='搜索结果', anchor='w')
        search_tree.grid(row=1, column=0, sticky='nsew')

        abspath = os.path.abspath(self.root_path)
        self.insert_file_node('', abspath, abspath)
        
        search_thread = searchThread(self)
        search_thread.start()

    def search_entry_callback(self, search_text):
        self.search_queue.put(search_text.get())

    def insert_file_node(self, parent, text, abspath):
        if text.startswith('.') or text.endswith('.assets'):
            return
        node = self.file_tree.insert(parent, 'end', text=text, open=True)
        self.md_file[node] = abspath
        if os.path.isdir(abspath):
            for p in os.listdir(abspath):
                self.insert_file_node(node, p, os.path.join(abspath, p))

    def file_click(self, event):
        node = self.file_tree.identify('item',event.x,event.y)
        file = self.md_file.get(node, None)
        print(file)
        if file:
            if os.path.isdir(file):
                return
            cmd = ['open', file]
            subprocess.call(cmd)
            self.add_recent(file)

    def add_recent(self, file):
        node = self.recent_node.get(file)
        if node:
            self.recent_tree.move(node, '', 0)
        elif file.endswith('.md'):
            root_path_len = len(self.root_path)
            node = self.recent_tree.insert('', 0,
                                               text=file[root_path_len+1:],
                                               open=True)
            self.recent_file[node] = file
            self.recent_node[file] = node

    def recent_click(self, event):
        node = self.file_tree.identify('item',event.x,event.y)
        file = self.recent_file.get(node, None)
        print(file)
        if file:
            cmd = ['open', file]
            subprocess.call(cmd)

    def open_file_node(self, event):
        node = self.file_tree.identify('item',event.x,event.y)
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.file_tree.delete(self.file_tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

class searchThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        app = self.app
        search_queue = app.search_queue
        app.search_tree.bind('<ButtonRelease-1>', self.search_click)
        while not False:
            text = search_queue.get()
            if not search_queue.empty():
                continue
            if len(text) < 1:
                self.set_search_tree('')
                continue
            if text == '__!!!@@@exit@@@!!!__':
                break
            cmd = '''find "''' + self.app.root_path + '''" -type f -name "*.md" | awk \'{print "\\""$0"\\""}\'| xargs grep -Eni "''' + text + '''"'''
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()
            result = str(out, encoding='utf-8')
            self.set_search_tree(result)
            print(result)

    def set_search_tree(self, result):
        search_tree = self.app.search_tree
        for node in search_tree.get_children():
            search_tree.delete(node)
        file_nodes_dict = dict()
        content_nodes_dict = dict()
        self.content_nodes_dict = content_nodes_dict
        root_path_len = len(self.app.root_path)
        for line in result.split('\n'):
            if len(line) < 1:
                return
            colon_position1 = line.find(':')
            colon_position2 = line.find(':', colon_position1 + 1)
            file_name = line[0:colon_position1]
            file_name = file_name[root_path_len+1:]
            line_number = line[colon_position1+1:colon_position2]
            content = line[colon_position2+1:]
            if not file_nodes_dict.get(file_name):
                file_nodes_dict[file_name] = search_tree.insert('', 'end', text=file_name, open=True)
            file_node = file_nodes_dict[file_name]
            content_node = search_tree.insert(file_node, 'end', text=line_number + '行 ' + content)
            content_nodes_dict[content_node] = file_name

    def search_click(self, event):
        node = self.app.search_tree.identify('item',event.x,event.y)
        file_name = self.content_nodes_dict.get(node)
        if file_name:
            file_path = self.app.root_path + '/' + file_name
            cmd = ['open', file_path]
            subprocess.call(cmd)
            self.app.add_recent(file_path)

if __name__ == '__main__':
    root_path = '/Users/deep/Library/Mobile Documents/com~apple~CloudDocs/工作/笔记'
    root = tk.Tk()
    root.title('Typora笔记助手')
    app = App(root, root_path=root_path)
    root.mainloop()
    app.search_queue.put('__!!!@@@exit@@@!!!__')
