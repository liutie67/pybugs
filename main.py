from url2mp3mp4 import getmp3mp4
from bvid_acquisition import getbvids


"""发送请求：模拟浏览器对url地址发送请求"""
# 模拟浏览器
# ubuntu headers
headers = {
    "cookie": "buvid3=91276CE0-CFE0-A545-BA8A-B36A0E0279CE65976infoc; b_nut=1752732365; _uuid=A17BA8FC-B6C1-28C2-E7F10-79C77A4A510F1066615infoc; enable_web_push=DISABLE; home_feed_column=5; browser_resolution=1850-968; buvid4=38A6AADE-2460-DCFE-4342-1B18C9CEFF1E66769-025071714-1A%2Fbp2hxpBrpqjbv3apscw%3D%3D; buvid_fp=427828aa957ae69edab1f904065678ce; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTMzMjgzNTYsImlhdCI6MTc1MzA2OTA5NiwicGx0IjotMX0.dcWfh8GFM_SGGesiFQh3cwKWkNBNDKfcWP41Y05VDcE; bili_ticket_expires=1753328296; CURRENT_FNVAL=4048; rpdid=|(um)~ukuYl|0J'u~lJ|Y|R)k; b_lsid=2787BB26_1982ADE1A42; bmg_af_switch=1; sid=8l9dzykr; bsource=search_bing; bmg_src_def_domain=i1.hdslb.com"
    ,"referer": "https://www.bilibili.com/"
    , "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
}
# 请求网址：视频播放页面
url = 'https://www.bilibili.com/video/BV1RBTGz8EKp/?spm_id_from=333.1007.tianma.1-1-1.click'  # &vd_source=0a9fa60dc05e0583c5edde1708d6eba1'

# i = 63
# for bvid in getbvids()[i-1:-1]:
#     print(i, end='\t')
#     i = i + 1
#     getmp3mp4(bvid, video_path='./video', headers=headers, url=url)

getmp3mp4(bvid='BV1RBTGz8EKp', video_path='./video', headers=headers, url=url)
