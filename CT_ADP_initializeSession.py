import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import r
from pymongo import MongoClient
import config.config
#import DatabaseClient
from bson.objectid import ObjectId
import pymongo as pm
import random
import numpy as np
import redis
import TestRunTimeQueue

sessionID = "5c18ea9a4394ba62080040ae"

 # def main():
 #    sessionID = "5c18ea9a4394ba62080040ae"
 #    initializeSuccess = sessionConfigInitial(sessionID)
 #    N_Par_item_success = N_Par_itemselect(sessionID)
 #    getFirstItem_success = getFirstItemID(sessionID)


#初始化内容以及冗余储存
def sessionConfigInitial(sessionID):
    # 连接数据库
    config.config.initconfig()
    configData = config.config.configData
    clientName = configData['db_host'] + ":" + configData['db_port']
    client = MongoClient(clientName)
    db = client.catxx
    db.authenticate(configData['db_username'], configData['db_password'])

    # DatabaseClient()
    # db= DatabaseClient.db

    col_session = db.session
    col_test = db.test
    v_session = col_session.find_one({"_id": ObjectId(sessionID)})
    testId = v_session['sessiontype']['testID']
    v_test = col_test.find_one({"_id": ObjectId(testId)})

    responsepattern = []
    thetahistory = []

    initconfig = {
        "SelfAdpQMaxLength": v_test['adp']['SelfAdpQMaxLength'],
        "SelfAdpQMinLength": v_test['adp']['SelfAdpQMinLength'],
        "AdpPrecision": v_test['adp']['AdpPrecision'],
        "ThetaInitialValue": v_test['adp']['ThetaInitialValue'],
        "DifficultyInitialValue": v_test['adp']['DifficultyInitialValue']
    }

    initConstraints = v_test['adp']['Constraint']

    ##从Constraint中查找内容
    #  id="5b0e07b64be3e8ccd7f78d7a"
    col_session.update_one({"_id": ObjectId(sessionID)}, {"$set": {"adp.config": initconfig}})
    col_session.update_one({"_id": ObjectId(sessionID)}, {"$set": {"adp.currenTheta": initconfig["ThetaInitialValue"]}})
    col_session.update_one({"_id": ObjectId(sessionID)}, {"$set": {"adp.responsepattern": responsepattern}})
    col_session.update_one({"_id": ObjectId(sessionID)}, {"$set": {"adp.thetahistory": thetahistory}})
    col_session.update_one({"_id": ObjectId(sessionID)}, {"$set": {"adp.Constraints": initConstraints}})
    client.close()
    return 1


def N_Par_itemselect(sessionID):

    config.config.initconfig()
    configData = config.config.configData

    clientName = configData['db_host'] + ":" + configData['db_port']
    client = MongoClient(clientName)
    db_auth = client.catxx
    db_auth.authenticate(configData['db_username'], configData['db_password'])
    if not client:
        return 0

    db = client.catxx
    col_session = db.session
    col_qb = db.qb
    col_kp = db.kp
    col_test = db.test
    if not col_session.find_one({"_id":ObjectId(sessionID)}):
        return 0

    vsession = col_session.find_one({"_id":ObjectId(sessionID)})
    if vsession["sessiontype"]["type"] == "test":
        return 0


    N_Par_itemNumlist = N_Par_itemRandom(configData['unmarkedItemNumber'])#把位置取出来



    #找到未标参的所有题
    v = col_qb.find({"parameter.trainingtag":"0"}).sort("AccumulativeRespCount",pm.DESCENDING)#找到所有未标记参数的题目，按曝光率降序排列


    #选出曝光率最高的前六道题,生成一个二维矩阵
    two_dime_itemlist=[]
    two_dime_itemlist=np.ones((configData['unmarkedItemNumber'],2), dtype=np.object)
    for i in range(0,configData['unmarkedItemNumber']):
            two_dime_itemlist[i][0]=str(v[i]["_id"]) #题号
            two_dime_itemlist[i][1]=str(N_Par_itemNumlist[i]) #位置


    #r = redis.StrictRedis(host=configData['redisHost'], port=configData['redisport'], db=0)#指定参数host、port与指定的服务器和端⼝连接
    client.close()
    # print(two_dime_itemlist)
    return(two_dime_itemlist)


#为未标参题目生成number个随机位置
def N_Par_itemRandom(number):

    N_Par_itemlist = []

    numberlist = range(5,29) #生成5-28列表

    N_Par_itemlist = random.sample(numberlist,number)    #生成5-28区间内number个无重复数字的随机数列表
    N_Par_itemlist.sort(reverse = False)   #降序排列

    return N_Par_itemlist


#通过r算法获取第一题ID
def getFirstItemID(sessionID ):
    config.config.initconfig()
    configData = config.config.configData
    Unselected_module = []
    Unselected_i = []
    Unselected_abcr=[]

    clientName = configData['db_host'] + ":" + configData['db_port']
    client = MongoClient(clientName)
    db = client.catxx
    db.authenticate(configData['db_username'], configData['db_password'])
    col_session = db.session
    col_test = db.test
    col_qb=db.qb
    col_parameter=db.parameter
    col_kp = db.kp
    v_par = col_qb.find({"parameter.trainingtag": "1"})

    re = redis.Redis(host='127.0.0.1', port='6379')
    # 获得Unselected_i,Unselected_abcr,Unselected_module
    for row in v_par:
        Unselected_i.append(row["_id"])

        Unselected_abcr.append(row["parameter"]["parameters"][1]["value"])
        Unselected_abcr.append(row["parameter"]["parameters"][0]["value"])
        Unselected_abcr.append(row["parameter"]["parameters"][2]["value"])
        Unselected_abcr.append(row["parameter"]["ExposureRate"])
        # Unselected_abcr.append(list)

        if (re.exists(row["PointID"])):
            Unselected_module.append(re.get(row["PointID"]))
        else:
            v_kp = col_kp.find_one({"_id": ObjectId(row["PointID"])})
            kpID = str(v_kp['_id'])
            while (v_kp["kpGrade"]!= "b"):
                f_kpID = v_kp["parentKnowledgePoint"]["knowledgePointID"] #f_kpID是父知识点ID
                v_kp = col_kp.find_one({"kpID": f_kpID})
            Unselected_module.append(v_kp["name"])
            re.set(row["PointID"], v_kp["name"]) #将知识点ID和模式对应写入redis
        # Unselected_abcr.append(row["parameter"]["parameters"][1]["value"])
        # Unselected_abcr.append(row["parameter"]["parameters"][0]["value"])
        # Unselected_abcr.append(row["parameter"]["parameters"][2]["value"])
        # Unselected_abcr.append(row["parameter"]["ExposureRate"])

        # moduleName = ""
        # if (r.exists(row["PointID"])):
        #     Unselected_module.append(r.get(row["PointID"]))
        # else:
        #     v_kp = col_kp.find_one({"_id": ObjectId(row["PointID"])})
        #     kpid = str(v_kp['_id'])
        #     if (v_kp["kpGrade"] == "a"):
        #         client.close()
        #         return 0
        #
        #     while (v_kp["kpGrade"] != "b"):
        #         kpID = v_kp["parentKnowledgePoint"]["knowledgePointID"]
        #         v_kp = col_kp.find_one({"kpID": kpID})
        #     if v_kp["index"] == 1:
        #         moduleName = "A"
        #     if v_kp["index"] == 2:
        #         moduleName = "B"
        #     if v_kp["index"] == 3:
        #         moduleName = "C"
        #
        #     Unselected_module.append(moduleName)
        #     r.set(kpid, moduleName)

    theta = [-10000]
    #v_unselected_abcr = np.array(Unselected_abcr) #将 Unselected_abcr转变为矩阵
    v = robjects.FloatVector(Unselected_abcr)
    v_unselected_abcr = robjects.r['matrix'](v, ncol=4,byrow=True ) # 将 Unselected_abcr转变为矩阵
    v_unselected_i =robjects.StrVector(Unselected_i)          #直接是list就行,这个要再看看！！！
    # v = robjects.FloatVector(Unselected_abcr)
    # v_unselected_abcr = robjects.r['matrix'](v, ncol = 4)
    v_unselected_module = robjects.StrVector(Unselected_module)
    v_theta = robjects.FloatVector(theta)

    Idlist=[]
    robjects.r.source('./../../R/selectitem/First_item.R')
    Idlist = robjects.r.First_item(v_unselected_i, v_unselected_abcr, v_unselected_module, v_theta)    #Idlist这里是临时存放的，等秋蓉写好后进行替换
    Id=Idlist[0]

    itemlist = [{"itemID":Id}]
    col_session.update_one({"_id":ObjectId(sessionID)},{"$set":{"items":itemlist}})
    col_session.update_one({"_id":ObjectId(sessionID)},{"$set":{"adp.selecteditem":Id}})
    col_session.update_one({"_id":ObjectId(sessionID)},{"$set":{"adp.NextItemID":Id}})
    thetahistory = []
    col_session.update_one({"_id":ObjectId(sessionID)},{"$set":{"adp.thetahistory":thetahistory}})

    #这一段要出现在responds之后
    # firstItem = col_qb.find_one({"_id": ObjectId(Id)})
    # CurrentAccumulativeRespCount = firstItem["parameter.AccumulativeRespCount"]
    # CurrentTotalAccumulativeRespCount = firstItem["parameter.TotalAccumulativeRespCount"]
    # col_qb.update({"_id":ObjectId(Id)},{"$set":{"parameter.AccumulativeRespCount":CurrentAccumulativeRespCount + 1}})  #更新小里程数
    # col_qb.update({"_id":ObjectId(Id)},{"$set":{"parameter.TotalAccumulativeRespCount":CurrentTotalAccumulativeRespCount + 1}})  #更新大里程数

    # v1 = col_parameter.find_one({"_id": ObjectId("5b0e0f004be3e8ccd7f78d7b")})
    # CurrentTotalSessionCount=v1["TotalSessionCount"]
    # CurrentExposureRate=CurrentTotalAccumulativeRespCount/CurrentTotalSessionCount
    # col_qb.update({"_id":ObjectId(Id)},{"$set":{"parameter.ExposureRate":CurrentExposureRate}})
    client.close()
    print(Id)
    return Id

initializeSuccess = sessionConfigInitial(sessionID)
N_Par_item_success = N_Par_itemselect(sessionID)
getFirstItem_success = getFirstItemID(sessionID)

