import re


def getbvids():
    with open("bvid.txt", "r") as f:
        contents = f.readlines()
    # print(type(contents))
    # print(len(contents))
    # print(contents)
    bvids = re.findall(r',"rotate":0}},"bvid":"(.*?)","pages":\[\{"cid":', contents[0])
    # key = ',"rotate":0}},"bvid":"(.*?)","pages":[{"cid":'
    # print(key)
    # print(bvids)
    # print(type(bvids))
    # print(len(bvids))

    return bvids[0:len(bvids)//2]

if __name__ == '__main__':
    print(getbvids())
    print(getbvids()[6])
    print(len(getbvids()))