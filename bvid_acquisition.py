import re


def getbvids(bvid_path):
    with open(bvid_path, "r") as f:
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
    bvid_path = "bvid-房产中介与炒房客.txt"
    print(getbvids(bvid_path))
    print(getbvids(bvid_path)[0])
    print(len(getbvids(bvid_path)))