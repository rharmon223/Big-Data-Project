import json
import glob
import os
import csv
import re
from DB import DB, DB_NAME

def main():
    data = []
    db = DB(DB_NAME)
    create_tables(db)
    
    con = db.connection()
    cur = db.cursor()
    
    for file in glob.glob("*.csv"):
        f = open(file, 'rb')
        reader = csv.reader(f)
        headers = reader.next()
        with open(file) as csvfile:
                
                reader = csv.DictReader(csvfile)
                table_name=re.sub(r'[^a-zA-Z]','',file.replace('.csv',''))
                
                print table_name
                q = 'insert into '+ table_name +' VALUES (%s, '
                for i in range(1,len(headers)):
                    q = q + '%s, '
                q = q[:-2]+')'
                
                val = ''
                for i in range(0,len(headers)):
                    header_name = re.sub(r'[^a-zA-Z]','',headers[i].replace(' ',''))
                    val = val + 'row[\''+header_name+'\'], '
                val = val [:-2]
                for row in reader:
                    cur.execute(q, (eval(val)))
    con.commit()
    
    joinData ='select coffee.date as date, coffee.value as coffeeValue,\
    copper.mid as copperValue, CottonETF.close as CottonETFValue, \
    GoldIndex.close as GlodValue, NASDAQVIX.settle as NASDAQVIXsettle,\
    NYMEXAMEXNaturalGasIndex.close as GasClose,  NYMEXCrudeOIl.settle as CrudeOIlSettle,\
    SPVIX.close as SPVIXClose, SoybeanETF.close as BeanClose, WheatETF.close as WheatClose\
    from coffee, copper,CottonETF, GoldIndex, GoldSilverIndex, NASDAQVIX,\
    NYMEXAMEXNaturalGasIndex, NYMEXCrudeOIl, SPVIX, SoybeanETF,\
    WheatETF  where coffee.date>\'2014-01-01 00:00:00\' and\
    coffee.date<\'2014-12-31 00:00:00\' and coffee.date=copper.date\
    and  CottonETF.date=copper.date\
    and GoldIndex.date=copper.date\
    and GoldSilverIndex.date=copper.date\
    and NASDAQVIX.date=copper.date\
    and NYMEXAMEXNaturalGasIndex.date=copper.date\
    and NYMEXCrudeOIl.date=copper.date\
    and SPVIX.date=copper.date\
    and SoybeanETF.date=copper.date\
    and WheatETF.date=copper.date order by coffee.date asc'
    
    header = ['date', 'coffeevalue', 'coppervalue', 'cottonetfvalue', 'glodvalue', 'nasdaqvixsettle',\
              'gasclose', 'crudeoilsettle', 'spvixclose', 'beanclose', 'wheatclose']
    t = db.query(joinData)
    with open("D:/Big-Data-Project/testData.csv", "wb") as f:
        writer = csv.DictWriter(f, fieldnames =header)
        writer.writeheader()
        writer = csv.writer(f)
        writer.writerows(t)

def create_tables(db):
    con = db.connection()
    cur = db.cursor()
    for file in glob.glob("*.csv"):
        table_name=re.sub(r'[^a-zA-Z]','',file.replace('.csv',''))
        d = 'drop table if exists ' + table_name
        print d
        cur.execute(d)  
    
    for file in glob.glob("*.csv"):
        f = open(file, 'rb')
        reader = csv.reader(f)
        headers = reader.next()
        table_name=re.sub(r'[^a-zA-Z]','',file.replace('.csv',''))
        q1 = 'create table '+ table_name+' (date timestamp,'
        for i in range(1,len(headers)):
            header_name = re.sub(r'[^a-zA-Z]','',headers[i].replace(' ',''))
            q1 = q1 + header_name+' float,'
        q1 = q1[:-1]+')'
        print q1
        cur.execute(q1)
    con.commit()
        

if __name__ == '__main__':
    main()
        
    
    