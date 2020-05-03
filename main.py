import requests
from lxml import etree

sear_head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
sear_data = input("请输入检索关键词：")
sear_lnpu = input("请输入下载结束页：")
sear_lens = int(sear_lnpu)
sear_nums = 0
sear_maxl = 16 #最长标签数
with open("index.ini",'w') as sear_file:
    for page_loop in range(0,sear_lens):
        #获取每个搜索页面数据
        page_urls = requests.get("https://freesound.org/search/?q=" + sear_data + "&page=" + str(page_loop) + "\#sound", headers = sear_head)
        page_temp = open('temp.html','w',encoding='utf-8')
        page_temp.write(page_urls.text)
        page_data = etree.parse('temp.html', etree.HTMLParser())
        page_coun = 0
        for page_inde in range(1,32):
            page_find ='//*[@id="content_full"]/div['+str(2+page_inde)+']/div[1]/div[2]/div[1]/a/@href'
            page_strs = page_data.xpath(page_find)
            if len(page_strs)>=1:
                #获取每个子页面数据
                page_coun+=1
                sear_nums+=1
                chil_urls = requests.get("https://freesound.org"+page_strs[0], headers = sear_head)
                chil_temp = open('data.html','w',encoding='utf-8')
                chil_temp.write(chil_urls.text)
                chil_data = etree.parse('data.html', etree.HTMLParser())
                chil_find ='/html/head/meta[23]/@content'
                chil_strs = chil_data.xpath(chil_find)
                print("总共第：%4d条，当前%3d页%3d条 当前下载：%-48s 地址：%-64s"%(sear_nums,page_loop+1,page_coun,page_strs[0],chil_strs[0]),end="")
                chil_file=requests.get(chil_strs[0])
                with open("data/%04d.mp3"%(sear_nums),"wb") as chil_writ:
                    chil_writ.write(chil_file.content)
                chil_writ.close()
                tags_nums = 0
                for tags_loop in range(0,sear_maxl+1):
                    tags_find ='//*[@id="single_sample_content"]/ul/li['+str(tags_loop+1)+']/a/text()'
                    tags_strs = chil_data.xpath(tags_find)
                    if len(tags_strs)>=1:
                        print(" "+tags_strs[0],end="")
                        tags_nums+=1
                print("")
                sear_file.write("%04d %02d"%(sear_nums,tags_nums))
                for tags_loop in range(0,tags_nums+1):
                    tags_find ='//*[@id="single_sample_content"]/ul/li['+str(tags_loop+1)+']/a/text()'
                    tags_strs = chil_data.xpath(tags_find)
                    if len(tags_strs)>=1:
                        sear_file.write("%12s"%(tags_strs[0]))
                sear_file.write("\n")
                if page_coun==16:
                    break
