sampleA={"神州长城","中集集团","晨鸣纸业","古井贡酒","招商港口","百联股份","浙江医药","江西铜业","中金黄金","国泰君安","掌阅科技"}
sampleB={"神州长城","中集集团","晨鸣纸业","古井贡酒","招商港口","百联股份"}
sampleH={"中集集团","晨鸣纸业","江西铜业","国泰君安","小米集团","阿里影业","平安好医生"}
print(sampleA | sampleH | sampleB)
print(sampleA & sampleH & sampleB)
print(sampleA-sampleB)
print(sampleH-sampleA)
sampleA.add("光大证券")
sampleH.add("光大证券")
sampleA.remove("神州长城")
sampleB.remove("神州长城")
sampleH.remove("小米集团")
sampleH.remove("阿里影业")
print(sampleH)