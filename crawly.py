import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import os
from tkinter import Tk, Label, StringVar, ttk, Button, Entry, Text
import tkinter as tk

baseurl = "https://www.luogu.com.cn/problem/P"
savePath = "C:/Users/16515/Documents/洛谷习题\\"
blogurl = "https://www.luogu.com.cn/blog/_post/"
listurl = "https://www.luogu.com.cn/problem/list?page=1"
solutionurl = "https://www.luogu.com.cn/problem/solution/P"
minn = 1000
maxn = 1049  # 最大题号
global dificul1
dificul1 = 0
global dificul2
dificul2 = 0
global dificul3
dificul3 = 0
global dificul4
dificul4 = 0
global dificul5
dificul5 = 0
global dificul6
dificul6 = 0
global dificul7
dificul7 = 0


def click1():
    global dificul1
    dificul1 = 1
    fun()


def click2():
    global dificul2
    dificul2 = 2
    fun()


def click3():
    global dificul3
    dificul3 = 3
    fun()


def click4():
    global dificul4
    dificul4 = 4
    fun()


def click5():
    global dificul5
    dificul5 = 5
    fun()


def click6():
    global dificul6
    dificul6 = 6
    fun()


def click7():
    global dificul7
    dificul7 = 7
    fun()


def fun():
    print("计划爬取到P{}".format(maxn))
    t_list = []
    count = 0
    get_titles(listurl, t_list)
    dif_list = get_dif(listurl)

    for i in range(minn, maxn + 1):

        text_output.insert(tk.END, "正在爬取P" + str(i) + "\n")
        key_list = []
        slice(t_list[i - 1000], key_list)
        dif = dif_turn(dif_list[i - 1000])
        if dif == "入门" and dificul1 == 0:
            continue
        if dif == "普及-" and dificul2 == 0:
            continue
        if dif == "普及&提高-" and dificul3 == 0:
            continue
        if dif == "普及+&提高" and dificul4 == 0:
            continue
        if dif == "提高+&省选-" and dificul5 == 0:
            continue
        if dif == "省选&NOI-" and dificul6 == 0:
            continue
        if dif == "NOI&NOI+&CTSC" and dificul7 == 0:
            continue
        count = count + 1
        if count > 50:
            return
        print("正在爬取P{}...".format(i), end="")
        phtml = get_baseHTML(baseurl + str(i))
        shtml = get_solutionHTML(solutionurl + str(i))
        if phtml == "error":
            print("爬取失败，可能是不存在该题或无权查看")
        else:
            problem = get_baseMD(phtml)
            solution = get_solutionMD(shtml)
            print("爬取成功！正在保存...", end="")
            text_output.insert(tk.END, "爬取成功！正在保存..." + "\n")
            if key_list:
                born_file(savePath + dif + "-" + key_list[0] + "-" + key_list[1])
                path = savePath + dif + "-" + key_list[0] + "-" + key_list[1] + "\\"
            else:
                born_file(savePath + dif)
                path = savePath + dif + "\\"
            born_file(path + "P" + str(i) + "--" + t_list[i - 1000])
            new_path = path + "P" + str(i) + "--" + t_list[i - 1000] + "\\"
            saveData(problem, new_path + "P" + str(i) + "--" + t_list[i - 1000] + ".md")
            saveData(solution, new_path + "P" + str(i) + "--" + t_list[i - 1000] + "题解" + ".md")
            print("保存成功!")
            text_output.insert(tk.END, "保存成功!" + "\n")


# 模拟用户访问浏览器
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103",
        "cookie": "__client_id=af4215a6f73e4641a2ae5ed49f35ef0b93b0709b; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fauth%2Flogin; _uid=664601; C3VK=a66952"
    }
    response = requests.get(url=url, headers=headers)
    return response.text


# 获取洛谷题库信息
def get_baseHTML(url):
    basehtml = get_html(url)
    return basehtml


# 将题目信息转化为md格式
def get_baseMD(html):
    bs = BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md


# 获取题解信息
def get_solutionHTML(url):
    solutionhtml = get_html(url)
    key = get_postfix(solutionhtml)
    new_url = solutionurl + key
    new_solutionhtml = get_html(new_url)
    return new_solutionhtml


# 获得博客后缀
def get_postfix(text):
    pattern = r"%22id%22%3A(\d+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


# 将题解网页转化为md格式
def get_solutionMD(html):
    core = BeautifulSoup(html, "html.parser")
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</p>", "<br>", md)
    return md


# 生成文件夹
def born_file(name):
    if not os.path.exists(name):
        os.mkdir(name)


# 获取题目关键词
def slice(t_list, key_list):
    if t_list[0] == "[":
        key_list.append(t_list[1:5] + t_list[10:13])
        key_list.append(t_list[5:9])


# 获取标题列表
def get_titles(url, t_list):
    #for i in "123456789":
    thtml = get_html(url)
    soup = BeautifulSoup(thtml, "html.parser")
    all_titles = soup.findAll("li")
    for title in all_titles:
        name = title.find("a")
        t_list.append(name.string)


def dif_turn(dif):
    if dif == "1":
        d = "入门"
    elif dif == "2":
        d = "普及-"
    elif dif == "3":
        d = "普及&提高-"
    elif dif == "4":
        d = "普及+&提高"
    elif dif == "5":
        d = "提高+&省选-"
    elif dif == "6":
        d = "省选&NOI-"
    else:
        d = "NOI&NOI+&CTSC"
    return d


def get_dif(url):
    #for i in "123456789":
    thtml = get_html(url)
    text = urllib.parse.unquote(thtml)
    pattern = r'"difficulty":(\d)'
    numbers = re.findall(pattern, text)
    return numbers


# 存储md文件
def saveData(data, filename):
    file = open(filename, "w", encoding="utf-8")
    for d in data:
        file.writelines(d)
    file.close()


window = Tk()
# 设置窗口大小
window.geometry("600x400")

# 创建标签
label1 = Label(window, text="难度")

# 显示标签
label1.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# 创建文本框
text_output = Text(window, width=40, height=10)  # 设置初始宽度和高度
text_output.grid(row=6, column=0, columnspan=8, padx=8, pady=8, sticky='w')

# 创建选择按钮
button1 = Button(window, text="入门", command=click1)
button1.grid(row=1, column=1, padx=10, pady=10, sticky='w')
button2 = Button(window, text="普及-", command=click2)
button2.grid(row=1, column=2, padx=10, pady=10, sticky='w')
button3 = Button(window, text="普及/提高-", command=click3)
button3.grid(row=1, column=3, padx=10, pady=10, sticky='w')
button4 = Button(window, text="普及+/提高", command=click4)
button4.grid(row=2, column=1, padx=10, pady=10, sticky='w')
button5 = Button(window, text="提高+/省选-", command=click5)
button5.grid(row=2, column=2, padx=10, pady=10, sticky='w')
button6 = Button(window, text="省选/NOI-", command=click6)
button6.grid(row=2, column=3, padx=10, pady=10, sticky='w')
button7 = Button(window, text="NOI/NOI+/CTSC", command=click7)
button7.grid(row=2, column=4, padx=10, pady=10, sticky='w')

window.mainloop()
