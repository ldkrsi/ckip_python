# ckip_python
中研院中文斷詞系統python版本用戶端程式(CKIP client in python)

支援python2和python3
## 事前準備
1. 先去官網申請帳號密碼
    + 官網連結 [http://ckipsvr.iis.sinica.edu.tw](http://ckipsvr.iis.sinica.edu.tw/)
    + 申請完後要等待一天的時間帳號才會開通
2. 修改`config.ini.example`，將申請的帳號密碼寫入
3. 將`config.ini.example`更名為`config.ini`

## 使用方法

    from CKIP_client import ckip_client
    text1 = "Facebook 是一個聯繫朋友、工作夥伴、同學或其他社交圈之間的社交工具。"
    text2 = u"Facebook 是一個聯繫朋友、工作夥伴、同學或其他社交圈之間的社交工具。"
    try:
        #指定輸出檔案
        ckip_client(text1,"output1.txt")
        ckip_client(text2.encode('utf-8'),"output2.txt")
        #不指定輸出檔案
        result, the_length = ckip_client(text1)
    except:
        pass
ckip_client如果斷詞成功會回傳兩個參數：斷詞結果(不換行), 該次傳送的字元數

## 注意事項
整理自 [http://ckipsvr.iis.sinica.edu.tw/apply.htm](http://ckipsvr.iis.sinica.edu.tw/apply.htm)

1. 傳送一次request時，大小需在約 7900 字元內。
2. 大約每傳送42000字元內，最好就要等待一段時間或所有結果回傳再送
3. 每句字數避免超過80個字
4. 每天上午六點進行系統維護，每次預計十到十五分鐘，該時間內請別使用
5. 輸入請帶標點符號，不要輸入表情符號
6. 如伺服器突然無法使用，這是正常現象
7. 本程式只支援UTF-8的輸入和輸出，如有其他需求請自行修改