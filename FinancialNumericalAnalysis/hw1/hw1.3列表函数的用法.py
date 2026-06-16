index_name=["Dow","Nas","Sp500","Rus3000","Sse","Szse"]
index_number=[27665.64,10853.55,3340.94,1946.98,3260.35,4627.28]
print(index_name[2],index_name[4])
print(index_number.index(10853.55),index_number.index(4627.28))
add_name=["fus100","Cac40","Dax","Moe"]
add_number=[6032.09,5034.14,13202.84,3315.81]
index_name.extend(add_name)
index_number.extend(add_number)
del index_name[3]
del index_number[3]
index_name.insert(6,"Sen")
index_number.insert(6,38854.55)
print(index_name,"\n",index_number)
index_number.sort(reverse=True)
print(index_number)
index_number.sort(reverse=False)
print(index_number)
index_number.clear()
index_name.clear()
print(index_name)
print(index_number)
del index_name
del index_number
print(index_number)
print(index_name)