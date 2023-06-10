from treelib import Tree, Node
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
from selenium.webdriver.firefox.service import Service

# from selenium.webdriver.common.proxy import Proxy, ProxyType
import sys

options = Options()
options.add_argument("-headless")
# options.headless = True
#s = Service(r"driver\\geckodriver.exe") 
browser = webdriver.Firefox(options=options)

divison = -1  # Decide which Trees will be selected and built
timeout_sec = 10

wordDict = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "-",
    "_",
]

keywordsFile = ""
dictTree = Tree()
root = Node(data="")
dictTree.add_node(root)
parents = []


def init_tree():
    print("Initing trees")
    

    for firstWord in wordDict[divison]:# For each char
        node1layer = Node(data=firstWord)
        dictTree.add_node(node1layer, parent=root)
        parents.append(node1layer)

        for secWord in wordDict:
            node2layer = Node(data=secWord)
            dictTree.add_node(node2layer, parent=node1layer)


def add_leaf_node(root):
    for word in wordDict:
        node = Node(data=word)
        dictTree.add_node(node, parent=root)


def cut_accepted_leaves(leaves):
    global parents

    flag = 1
    for node in dictTree.leaves():
        if node not in leaves or node in parents:
            dictTree.remove_node(node.identifier)
            flag = 0

    if flag == 0:
        cut_accepted_leaves(leaves)


def traversal_paths_to_leaf():
    # flag is used to judge whether end recursive
    #flag = 1
    leaves = dictTree.leaves()
    for path in dictTree.paths_to_leaves():
        keyWord = ""
        for node in path:
            keyWord = keyWord + dictTree[node].data

        leaf = dictTree[path[-1]]
        # Judging whether this keyword can be used to search in docker hub
        # options.add_argument('--proxy-server=http://ip:port')# TODO:这里需要获取代理
        # Note: Refer https://blog.csdn.net/woaixuexi6666/article/details/126394558
        status = check_keyword_search_results(keyWord)
        if status == 1:
            print("Before removing:")
            print_trees()

            dictTree.remove_node(leaf.identifier)

            #print("After removing:")
            #print_trees()

            #NOTE: comment here to avoid wordtree reset
            #cut_accepted_leaves(leaves)

            #print("After cutting:")
            #print_trees()

            with open(keywordsFile, "a+") as keyword_list:
                keyword_list.write(keyWord + "\n")  # Adding to vaild words.
            # keywordList.append(keyWord)
        # no results
        elif status == -2:
            dictTree.remove_node(leaf.identifier)
            cut_accepted_leaves(leaves)
        # If it can't, add a new character behind this keyword
        elif status == -1:
            return
        else:
            add_leaf_node(leaf)
            flag = 0
        print_trees()
    if print_trees():# This function shows if the tree is empty
        traversal_paths_to_leaf()


def check_number(number):
    num = str(number).split(",")
    
    # num over 1,000,000
    if len(num) > 2:
        return 0
    # num less 1,000
    elif len(num) == 1:
        return 1

    try:  # Why here?
        imageNum = int(num[0]) * 1000 + int(num[1])
        if imageNum < 2500:
            return 1
    except Exception as _:
        return 0  # if len(num)==0,return 0. Usually it will not happen

    return 0


def check_keyword_search_results(keyWord):
    # root node is ""
    if keyWord == "":
        return -1

    print("Check the Keywords:", keyWord)

    url = "https://hub.docker.com/search?q={}&type=image".format(keyWord)
    for _ in range(5):
        try:
            browser.get(url)
            break
        except Exception as e:
            print("retry...")
            continue

    
    try:
        element = Wait(browser, timeout_sec).until(
        Expect.presence_of_element_located((By.CLASS_NAME, "MuiTypography-root MuiTypography-h3 css-lhhh1d"))
        )

        if "No results" in element.text:
            print("There doesn't have search results...")
            # return 0
            return -2
        """
        NOTE: in fact we cannot capture 'No result' here but we must wait for some secs.
        """
    except Exception as e:
        pass #Continue executing


    # NOTE: thisstep will fix browser.page_source,so donot comment it.

    #print(f"wegot {browser.page_source}")
    soup = BeautifulSoup(browser.page_source, "html.parser")

    links = soup.find_all("div", class_="MuiBox-root css-r29exk")
        #print(f"We got {links}")
        # FIXME: 这里什么都没抓到
    if not links:
        print("fatal:no links located. Retry")
        return check_keyword_search_results(keyWord=keyWord)#Reexecute
    
    for link in links:
        print(f"Raw text is:{link.div.text}")
        if "-" in link.div.text and "of" in link.div.text:
            num = link.div.text.split()[4]
            imageNum = check_number(num)
            print(f"{keyWord}: got {num}, means {imageNum}")
            return imageNum
        elif link.div.text=="images":
            #Patch: no result here
            print("No result here")
            return -2
    return 0

def print_trees():
    res=[]
    for path in dictTree.paths_to_leaves():
        res.append("".join([dictTree[w].data for w in path]))
    print(res)
    return res

def main():
    init_tree()
    traversal_paths_to_leaf()
    browser.quit()


if __name__ == "__main__":
    
    divison = int(sys.argv[1])  # should be 0~37
    if divison >=0 and divison<38:
        keywordsFile="./keywords/keyWordList-"+wordDict[divison]+".txt"
        main()
        
    
