from numpy import *
import numpy as np
import pandas as pd
import warnings
import logging
import math
import re
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
warnings.filterwarnings('ignore')
from flask import Flask,jsonify,request
logging.getLogger().setLevel(logging.INFO)
app = Flask(__name__)
@app.route('/api/cluster', methods = ['post'])
def process():
    try:
        input_path = request.files['input_path']
    except Exception:
        return '未输入文件'
    logging.info('数据输入成功')
    data = pd.read_csv(input_path, encoding='utf-8')
    pattern = re.compile(r'^浙江省.*')
    for i in range(np.shape(data)[0]):
        match = pattern.match(data['address'][i])
        if not match:
            data['address'][i] = ''.join(['浙江省', data['address'][i]])
    '''
    # #将可辨别的缺失市的补全
    '''
    pattern = re.compile(r'(.*(杭州市|宁波市|温州市|绍兴市|湖州市|嘉兴市|金华市|衢州市|舟山市|台州市|丽水市).*)')  # 没有市
    data['id'] = np.arange(len(data))
    for i in range(np.shape(data)[0]):
        match = pattern.match(data['address'][i])
        if not match:
            if re.compile(r'.*(上城区|下城区|江干区|拱墅区|西湖区|滨江区|萧山区|余杭区|富阳区|建德市|淳安县).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '杭州市', data_split[1]])
            elif re.compile(r'.*(海曙区|江东区|江北区|镇海区|北仑区|鄞州区|慈溪市|余姚市|奉化市).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '宁波市', data_split[1]])
            elif re.compile(r'.*(鹿城区|瓯海区|龙湾区|乐清市|瑞安市|永嘉县|洞头县|平阳县|苍南县|文成县|泰顺县|柳市镇).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '温州市', data_split[1]])
            elif re.compile(r'.*(越城区|柯桥区|上虞区|诸暨市|嵊州市|新昌县).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '绍兴市', data_split[1]])
            elif re.compile(r'.*(吴兴区|南浔区|长兴县|安吉县|德清县).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '湖州市', data_split[1]])
            elif re.compile(r'.*(嘉善县|海盐县|平湖市|海宁市|桐乡市).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '嘉兴市', data_split[1]])
            elif re.compile(r'.*(兰溪市|义乌市|东阳市|永康市|武义县|浦江县|磐安县|婺城区|金东区).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '金华市', data_split[1]])
            elif re.compile(r'.*(定海区|普陀区|岱山县|嵊泗县).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '舟山市', data_split[1]])
            elif re.compile(r'.*(椒江区|路桥区|黄岩区|温岭|玉环县|临海|三门县|仙居县|天台县).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '台州市', data_split[1]])
            elif re.compile(r'.*(丽水市|莲都区|龙泉市|缙云县|青田县|云和县|遂昌县|松阳县|庆元县|古市镇).*').match(data['address'][i]):
                data_split = data['address'][i].split('省')
                data['address'][i] = ''.join([data_split[0], '丽水市', data_split[1]])
    logging.info('填补处理成功')
    '''
    # 对各市划分编号，为了后续更方面处理
    # 温州：57
    # 绍兴：60
    # 宁波：67
    # 湖州：59
    # 衢州：65
    # 金华：61
    # 杭州：56
    # 嘉兴：58
    # 台州：62
    # 丽水：63
    # 舟山：64
    '''
    data['cate'] = data['cityId'].copy()
    logging.info('分类缺失处理成功')
    logging.critical('dataset is completed')
    data.to_csv('map.csv', encoding= 'utf-8')

    data = pd.read_csv('map.csv', encoding='utf-8')
    data['radius'] = None  # 首次运行的时候使用，后面注释掉
    data['parentId'] = None
    def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * math.asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r * 1000

    def compute_distance(data1, k, center, cate):  # 计算距离   k为簇中心的个数， center为每个簇的中心点
        for i in range(k):  # 遍历每个簇
            distance = []
            data_dist = data1[data1['labels'] == i]  # 筛选出各个簇的个数
            id = data_dist['id'].tolist()
            cent = center[i]  # 选出该簇的中心点
            lat = data_dist['lat'].tolist()
            lng = data_dist['lng'].tolist()
            if np.shape(data_dist)[0] == 1:
                for m in range(np.shape(data)[0]):  # 将经纬度和半径与样本点匹配
                    if (lat == data['lat'][m]) and (lng == data['lng'][m]) and (data['cate'][m] == cate):
                        data['radius'][m] = 0
                        data['parentId'][m] = str(0)
                continue

            for j in range(np.shape(data_dist)[0]):
                dista = haversine(lng[j], lat[j], cent[1], cent[0])  # 计算样本中各点与中心点的实际距离

                distance.append(dista)
            new_center = np.argmin(distance)  # 与聚类簇中心最近的样本点为新样本点
            radis = np.max(distance)  # 与簇中心的最大距离为簇半径
            if radis > 3000:
                return 0
            for m in range(np.shape(data)[0]):  # 将经纬度和半径与样本点匹配
                if (lat[new_center] == data['lat'][m]) and (lng[new_center] == data['lng'][m]) and (
                        data['cate'][m] == cate) and (radis < 3000):
                    data['radius'][m] = radis
                    for _, n in enumerate(id):
                        if data['parentId'][n] != str(0):
                            data['parentId'][n] = data['caseId'][m]
                    data['parentId'][m] = str(0)
                    break
                elif (radis > 3000):
                    return 0
        return 1

    for site in range(56,68):
        if site == 66:
            continue
        data1 = data[data['cate'] == site]
        x_axis = []  # 坐标组合

        for x, y in zip(data1['lat'], data1['lng']):  # 建立经度纬度的输入组合
            x_axis.append([x, y])

        x_axis = np.array(x_axis)
        flag = 0
        n_cluster = len(data1)//14
        while(flag == 0):
            clf = KMeans(n_clusters=n_cluster, init='k-means++', random_state=520)  # Kmeans分类算法
            clf.fit(x_axis)
            center = clf.cluster_centers_
            labels = clf.labels_
            data1['labels'] = labels
            flag = compute_distance(data1, n_cluster, center, site)
            n_cluster += 10
        logging.info('cityId:{},n_cluster:{}'.format(site, n_cluster))
        # print(site, ':', n_cluster)
    col = data.columns.values.tolist()
    columns = ['caseId', 'parentId', 'radius']
    for _, i in enumerate(col):
        if i not in columns:
            data = data.drop(i, axis=1)
    return data.to_json(orient='records')

if __name__ == '__main__':
    from logging.config import dictConfig

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    app.config['JSON_AS_ASCII'] = False

    app.run(host='0.0.0.0',port=8130, debug = True)