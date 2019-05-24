'''
从图片URL中下载图片
命名格式：博物馆ID_展馆ID_藏品ID_时代.jpg
'''

from urllib.request import urlretrieve
import urllib
import os
from fake_useragent import UserAgent

ua = UserAgent()


# urllib.error.ContentTooShortError
def download_images(museum_id, gallery_id, collection_id, period, collection_name, image_url):
    '''
    :param museum_id:       博物馆ID
    :param gallery_id:      展览馆ID
    :param collection_id:   藏品ID
    :param period:          展品年代
    :param image_url:       展品图片url
    :return:
    '''

    basic_path = './images'
    save_path = '_'.join([str(museum_id), str(gallery_id), str(collection_id), str(period), str(collection_name)])
    save_path = '.'.join([save_path, 'jpg'])
    save_path = os.path.join(basic_path, save_path)
    #设置User-Agent，防止服务端通过User-Agent判定为爬虫
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', ua.random)]
    urllib.request.install_opener(opener)

    try:
        urllib.request.urlretrieve(image_url, save_path)
    except urllib.error.ContentTooShortError:#若下载失败，通过递归操作重新下载
        print('Redownloading...')
        download_images(museum_id, gallery_id, collection_id, period, collection_name, image_url)
    return save_path


def do_download(all_data):
    '''

    :param all_data:  = bmap_all_collections.find(no_cursor_timeout = True)，需要指定no_cursor_timeout参数，防止超时尚未执行完毕
    :return:
    '''
    for col in all_data:
        name = col["name"]
        branchID =  col["branchId"]
        museumID =  col["museumId"]
        colID =  col["collectionId"]
        extradata = col["extraData"]
        period = ''
        if type(extradata) != type([]) and 'period' in extradata.keys():
            period = extradata["period"]
        image_url = col["bigImg"]
        download_images(museumID, branchID, colID, period, name, image_url)
    all_data.close()