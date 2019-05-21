from fake_useragent import UserAgent
import requests
import json
import pymongo
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["govmuseum"]
bmap_all_collections = mydb["bmap_all_collections"]



api_url = 'https://baike.baidu.com/museum/api/getcollectionlist?branchId='
ua = UserAgent()
bmap_json = '../bmap_export_V2.json'#'../bmap0521.json'
f = open(bmap_json,mode='r')
bmap_data = json.loads(f.read())

def get_gallery_collections(branchID):
    get_url = ''.join([api_url, str(branchID)])

    respon = requests.get(get_url, allow_redirects=False, headers={"User-Agent": ua.random})
    print("ID: {0}, CODE: {1}".format(branchID, respon.status_code))
    return json.loads(respon.content)



for bm in bmap_data:
    if 'galleryNums'  in bm.keys():
        if bm["galleryNums"]==str(1):#只有一个展馆
            data = get_gallery_collections(bm["galleryIds"])["data"]
            for da in data:
                bmap_all_collections.insert_one(da)
        else:#有多个展馆
            ids = bm["galleryIds"].split(',')
            for gid in ids:
                data = get_gallery_collections(gid)["data"]

                for da in data:

                    bmap_all_collections.insert_one(da)