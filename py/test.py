# from PIL import Image
# import pytesseract
##导入通用包
import numpy as np
import pandas as pd
import os
import json
import re
import base64
import xlwings as xw
##导入腾讯AI api
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

#定义函数
def excelFromPictures(picture,SecretId,SecretKey):

    rowIndex = []
    colIndex = []
    content = []
    try:
        with open(picture,"rb") as f:
                img_data = f.read()
        img_base64 = base64.b64encode(img_data)
        cred = credential.Credential(SecretId, SecretKey)  #ID和Secret从腾讯云申请
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        req = models.TableOCRRequest()
        params = '{"ImageBase64":"' + str(img_base64, 'utf-8') + '"}'
        req.from_json_string(params)
        resp = client.TableOCR(req)
        #     print(resp.to_json_string())
        ##提取识别出的数据，并且生成json
        result1 = json.loads(resp.to_json_string())
        for item in result1['TextDetections']:
            rowIndex.append(item['RowTl'])
            colIndex.append(item['ColTl'])
            content.append(item['Text'])
    except TencentCloudSDKException as err:
        print(err)

    ##导出Excel
    ##ExcelWriter方案
    rowIndex = pd.Series(rowIndex)
    colIndex = pd.Series(colIndex)

    index = rowIndex.unique()
    index.sort()

    columns = colIndex.unique()
    columns.sort()

    data = pd.DataFrame(index = index, columns = columns)
    for i in range(len(rowIndex)):
        data.loc[rowIndex[i],colIndex[i]] = re.sub(" ","",content[i])

    writer = pd.ExcelWriter("." + re.match(".*\.",f.name).group() + "xlsx", engine='xlsxwriter')
    data.to_excel(writer,sheet_name = 'Sheet1', index=False,header = False)
    writer.save()

    #xlwings方案
    # wb = xw.Book()
    # sht = wb.sheets('Sheet1')
    # for i in range(len(rowIndex)):
    #     sht[rowIndex[i],colIndex[i]].value = re.sub(" ",'',content[i])
    # wb.save("../tables/" + re.match(".*\.",f.name).group() + "xlsx")
    # wb.close()



# if not ('tables') in os.listdir():
#     os.mkdir("./tables/")
#
# os.chdir("./pictures/")
# pictures = os.listdir()
# for pic in pictures:
#     excelFromPictures(pic,"YoungID","YourKey")
#     print("已经完成" + pic + "的提取.")

pic='./test.png'
APPID=1304274829
SecretID='AKID711krgKPt50kFUfvGL9i5KJ1W2KLlc1C'
SecretKey='3kUx97sd8MEOIvGRpxrUs9Au2vd4JH0S'
excelFromPictures(pic,SecretID,SecretKey)