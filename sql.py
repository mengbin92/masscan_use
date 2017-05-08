#!/usr/bin/env python
# coding=utf-8

import pymysql
import xml.etree.ElementTree as ET
import os

class MySqlOp:
    def __init__(self,host,user,pwd,dbname):
        self.db = pymysql.connect(host,user,pwd,dbname)
        self.cursor = self.db.cursor()

    def select(self,sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            for row in res:
                id = row[0]
                addr = row[1]
                addrtype = row[2]
                print("id:%s\taddr:%s\taddrtype:%s",id,addr,addrtype)
        except Exception as e:
            print('select fail',e)

    def insert(self,sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print('insert fail',e)
        finally:
            self.db.commit()
    
    def is_exist(self,addr):
        try:
            sql = 'select * from blackIP where addr = \"'+addr+'\"'
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is None:
                return False
            else:
                return True
        except Exception as e:
            print('select fail',e)

    def __del__(self):
        self.cursor.close()
        self.db.close()


def readXML(path):
    ipDict = {}
    tree = ET.parse(path)
    root = tree.getroot()

    for child in root:
        #print(child.tag,child.attrib)
        for grandson in child:
            if grandson.tag == "address":
                #print(grandson.attrib['addr'],grandson.attrib['addrtype'])
                addr = grandson.attrib['addr']
                addrtype =  grandson.attrib['addrtype']
                ipDict[addr] = addrtype
    return ipDict

def getXMLfile(path):
    file_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.xml':
            file_list.append(file)
    return file_list


def modify(num,line):
    nameLine = 'output-filename = '+str(num)+'.xml\n'
    #print(nameLine)
    rangeLine = 'range = '+line
    #print(rangeLine)

    lines = open('mass.conf','r').readlines()
    #print(lines)

    rows = len(lines)-1
    for i in range(rows):
        if 'output-filename' in lines[i]:
            lines[i] = nameLine
        if 'range' in lines[i]:
            lines[i] = rangeLine

    open('mass.conf','w').writelines(lines)

if __name__ == "__main__":
    opt = MySqlOp('127.0.0.1','root',',.klio89','db_fingerprint')
    #opt.select("select * from finger")
    lines = open('ip.txt','r').readlines()
    length = len(lines)-1
    for i in range(length):
        modify(i,lines[i])
        os.system('masscan -c mass.conf')
    
    filelist = getXMLfile('.')
    print(filelist)
    for file in filelist:
        ip = readXML(file)
        for r in ip:
            #print(r,ip[r])
            if  opt.is_exist(r):
                #print('exist')
                continue
            else:
                sql = "insert into blackIP(addr,addrtype) values(\""+r+"\",\""+ip[r]+"\");"
                #print(sql)
                opt.insert(sql)
    print('Done')

    
