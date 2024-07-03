
import pandas as pd
import sqlite3

def get(url):
    data = pd.read_csv(url)   
    return pd.DataFrame(data)

def columnDel(data, delCol):
    data.drop(delCol, inplace = True, axis = 1)
    
    return data

def dropNull(data):
    return data.dropna(how = "any", axis = 0) 

def dataMerge(t1, t2, key, t1S, t2S):
    return pd.merge(t1, t2, how ='left', on = key, suffixes=(t1S, t2S))

def save(data, path, file, table):
    try:
        conn = sqlite3.connect(path+file)
        data.to_sql(table, conn, if_exists='replace', index=False)
        conn.close()
        return [path+file, table]
    
    except:
        conn = sqlite3.connect("../data/"+file)
        data.to_sql(table, conn, if_exists='replace', index=False)
        conn.close()
        return [path+file, table]

def main():
    url1 = "https://opendata.arcgis.com/datasets/7ba962035bb548bb9893add2b5491896_0.csv"
    data1 = get(url1)
    delCol1 = ["F1995", "F1996", "F1997", "F1998",	"F1999", "F2000", "F2001",	"F2002", "F2003", "F2004",	"F2005", "F2006", "F2007",	"F2008", "F2009", "F2010",	"F2011", "F2012",  "F2013", "F2014"]
    data1 = columnDel(data1, delCol1)
    data1 = dropNull(data1)

    url2 = "https://opendata.arcgis.com/datasets/d48cfd2124954fb0900cef95f2db2724_0.csv"
    data2 = get(url2)
    delCol2 = ["F2022", "F2023", "F2024", "F2025", "F2026", "F2027", "F2028", "F2029", "F2030"]
    data2 = columnDel(data2, delCol2)
    data2 = dropNull(data2)

    finalData = dataMerge(data1, data2, ["ISO3"], "_C", "_F")

    targetedPath = "./data/" 
    fileName = "Data.sqlite"
    dbName = "CO2Emissions_FossilFuel"
    
    return save(finalData, targetedPath, fileName, dbName)

if __name__ == "__main__":
    main()
