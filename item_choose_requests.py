import requests, re
import time

nr_url_list = []


def req_nr_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
        ,
        'cookie': 'session-id=134-1523147-8424152; i18n-prefs=USD; ubid-main=131-1506301-4586412; lc-main=en_US; session-id-time=2082787201l; session-token=OaCfkMRb+hIOGIJhr/t3UYGwJQY6tkmQV2Agzel/FfB6UfmC/Cb18qiYZmXpZnj7yC0mmMio1r0eDGCrt4zGd4wS8+WwP3RbprvA2YY5OBOw/ryflLZLazN79sCoyVeiewJraJlPweNqoHj8nmPgrXEbe/8HTl9wZgcvft0mwoo4fKAE7fAwh9sDHcUEeTQi'}
    req = requests.get(headers=headers, url=url)
    req_text = req.text.replace('\n', '')
    return req_text


def nr_url_get(text):
    mid_text = re.findall(r'<ul id="zg_browseRoot">.*?</ul>', text)[0]
    nr_cate_urls = re.findall(r'<li><a href=.*?>', mid_text)
    nr_cate_names = re.findall(r'\'>.+?<', mid_text)
    # TODO 等待根据当前nr在上一级中的排序，判断是否继续传给request获取链接
    m, n = len(nr_cate_urls), len(nr_cate_names)
    if m != n:
        nr_cate_names = nr_cate_names[1:]
    nr_url_id = 0
    for (url, name) in zip(nr_cate_urls, nr_cate_names):
        nr_cate_urls_dic = {}
        new_url = url.replace('<li><a href=\'', '').replace('\'>', '')
        new_name = name.replace('>', '').replace('<', '')
        nr_cate_urls_dic[new_name] = new_url
        nr_cate_urls_dic['id'] = nr_url_id
        nr_url_id += 1
        nr_url_list.append(nr_cate_urls_dic)


def page_url_get(text):
    base_url = 'https://www.amazon.com'
    page_url_text = re.findall(r'<ol id="zg-ordered-list".*?</ol>', text)[0]
    nr_page_urls = re.findall(r'class="a-link-normal" href=".*?">', page_url_text)
    print(len(nr_page_urls))
    nr_page_full_urls = []
    for url in nr_page_urls:
        new_url = base_url + url.replace('class="a-link-normal" href="', '').replace('">', '')
        nr_page_full_urls.append(new_url)
        print(new_url)
    return nr_page_full_urls


def req_page(text):
    try:
        dimensionToAsinMap = re.findall(r'dimensionToAsinMap.*?\}', text)[0]
        asins = re.findall(r'B[A-Z0-9]{9}', dimensionToAsinMap)  # B[A-Z0-9]{9}与B([A-Z0-9]{9})匹配结果不同
        # TODO 源代码里还有父ASIN可以抓取
    except:
        asins = ['单体']
    # inno_asins = []  # 该部分用来去掉重复的ASIN以及不符合格式的ASIN
    # test_asins = []
    # for asin in asins:
    #     if asin in test_asins:
    #         continue
    #     elif not (asin.isalpha() or asin.isdigit()):
    #         nasin = 'B' + asin
    #         test_asins.append(asin)
    #         inno_asins.append(nasin)
    print(asins)

    # TODO 通过正则表达式找出评论数': rating_num,
    #                      '评分': rating,
    #                      '小类目': min_bsr_type,
    #                      '小排名': min_bsr_num,
    #                      '大类目': max_bsr_type,
    #                      '大排名': max_bsr_num


if __name__ == '__main__':
    url = 'https://www.amazon.com/gp/new-releases/pet-supplies/2975238011/ref=zg_bsnr_nav_petsupplies_2_2975221011'
    text = req_nr_url(url)
    # nr_url_get(text)
    page_urls = page_url_get(text)
    # for item in nr_url_list:
    #     print(item)
    for url in page_urls:
        text = req_nr_url(url)
        req_page(text)
        time.sleep(2)
