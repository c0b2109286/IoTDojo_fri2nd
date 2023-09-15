import ujson
from collections import OrderedDict

class RouteMake:
    def _readtxt(self):
        # テキストファイルからデータを読み込んでlistにする.
        split = []
        with open("data/makeroute_data.txt",'r',encoding="utf-8")as f:
            data = f.readlines()
            for i in range(len(data)):
                # if data[i] in '\n':
                #     data[i].replace('\n' , '')
                data[i] = data[i].split('_')
                for j in range(len(data[i])):
                    #print(data[0][0])
                    if '\r' in data[i][j]:
                        data[i][j] = data[i][j].replace('\r', '')
                    if '\n' in data[i][j]:
                        data[i][j] = data[i][j].replace('\n', '')
                split.append(data[i])
            print(split)
            f.close()
            return split
        
    def _makeval(self,split):
        # JSONファイルから値を取得して二重リストを作成する.
        with open("data/packet_table.json", 'r', encoding="utf-8") as f:
            table= ujson.load(f)
            print("@@@@@")
            print(table)
            print(split)
            print(type(table))
            # for key in table.keys():
            #     print(key)
            print('---------')
            lis = []

            for i in range(len(split)):
                ls = []
                for list in split[i][:-2]:
                    print(list)
                    # print(type(list))
                    ls.append(table[list])
                lis.append(ls)
            print(lis)
            return lis

    def _makekey(self, lis):
        # _makeval関数にて作成したリストから辞書のキーとなる二重リストを作成する．
        print("$$$$$$$$$")
        _lis = []
        for i in range(len(lis)):
            _ls = []
            for j in range(len(lis[i])):
                if j == 0:
                    _ls.append('senser'+ str(i) + str(j))
                else:
                    _ls.append('relay'+ str(i) + str(j))
            _lis.append(_ls)
        print(_lis)
        return _lis

    def _dict(self,split, val, key):
        # _makeval関数と_makekey関数によって作成したリストを用いて辞書を生成する．
        print("##########")
        print(val)
        print(key)
        dic = OrderedDict() #順序付き辞書の作成
        for i in range(len(key)):
            print(key[0])
            if i is 0:
                dic.update(OrderedDict(zip(key[i],val[i])))
                print(dic)
                print("&&&&&")
                hopnum = split[i][-2]
                dic['hop'+str(i)] = hopnum
                rank = split[i][-1]
                dic['rank'+str(i)] = rank
                print(dic)
            else:
                dic.update(OrderedDict(zip(key[i],val[i])))
                print("######")
                print(dic)
                hopnum = split[i][-2]
                dic['hop'+str(i)] = hopnum
                rank = split[i][-1]
                dic['rank'+str(i)] = rank
                print(dic)
        return dic
    
    def _json(self, dic):
        # _dict関数によって作成したリストをJSONファイルに書き込む．
        with open('data/routeinfo.json','w',encoding="utf-8") as f:
            num = len(dic)
            print(num)
            #json.dump(dic,f,indent=num)
            ujson.dump(dic,f)
            f.close()


def _routemake(): #main関数
    rm = RouteMake()
    split = rm._readtxt()
    val = rm._makeval(split)
    key =rm._makekey(val)
    dic = rm._dict(split,val,key)
    rm._json(dic)


if __name__ == "__main__":
    _routemake()
