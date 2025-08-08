import json
from upers.esay_crypt import encrypt_json_file


query_dic = {
    'headers':
        {
            "cookie": "buvid3"
            , "referer": "https://space.bilibili.com"
            , "user-agent": "Mozilla/5.0"
        },
    'dones' :
        {
            'last_done' : "",
        },
    'pages':
        {
            'p1' : {
                "pn": "1",
                "ps": "42",
                "tid": "0",
                "special_type": "",
                "order": "pubdate",
                "mid": "16",
                "index": "0",
                "keyword": "",
                "order_avoided": "true",
                "platform": "web",
                "web_location": "3.3",
                "dm_img_list": "[{\":0}]",
                "dm_img_str": "V2V",
                "dm_cover_img_str": "R2W",
                "dm_img_inter": "",
                "w_webid": "",
                "w_rid": "6ca",
                "wts": "15"
            },
            # 'pchy' : {
            #
            # },
        }
}

if __name__ == "__main__":
    uper = 'exemple'
    with open('json/query_' + uper + '.json', 'w', encoding='utf-8') as f:
        json.dump(query_dic, f, ensure_ascii=False, indent=4)
    encrypt_json_file('json/query_' + uper + '.json', 'enc/query_' + uper + '.enc')