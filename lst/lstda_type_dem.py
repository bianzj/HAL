from util.myfun import *
import seaborn as sns


infile = r'D:\data\S3A_LST/ref.tif'
[types,ns,nl,nb,geog,proj] = read_image_gdal(infile)

infile = r'd:\data\s3a_lst/dem.tif'
[dems,ns,nl,nb,geog,proj] = read_image_gdal(infile)

unique_types = np.unique(types)
typeNum = np.size(unique_types)
monthNum = 12

lstda = np.zeros([typeNum,monthNum])
lstdaa = np.zeros([typeNum,monthNum])


unique_types = np.unique(types)
typeNum = np.size(unique_types)-1
monthNum = 12
demNum = 15

demmin = np.min(dems)
demmax = np.max(dems)
dlat = (demmax-demmin)/demNum
lstda = np.zeros([typeNum,demNum])
lstdaa = np.zeros([typeNum,demNum])


indir = r'D:\data\S3A_LST/'
infile = indir + '201907_lstda.tif'
[mydata, ns, nl, nb, geog, proj] = read_image_gdal(infile)

for ktype in range(typeNum):
    for klat in range(demNum):
        ind = (dems >= (demmin+dlat*klat)) * (dems <= (demmin + dlat+dlat*klat))*\
              (ktype+1 == types) * (mydata > -10) * (mydata < 10) * (mydata != 0)
        lattemp = mydata[ind]
        lstda[ktype,klat] = np.average(lattemp)
        lstdaa[ktype,klat] = np.std(lattemp)

fig, ax = plt.subplots()
lstda = np.transpose(lstda)
lstda = np.flip(lstda,0)
sns.heatmap(lstda,
            yticklabels=['>7500','7000','6500','6000','5500','5000','4500','4000',
                         '3500','3000','2500','2000','1500','1000','500'],
            xticklabels=np.linspace(1,16,16,dtype=np.int),cmap='jet')
plt.xlabel('surface type')
plt.ylabel('DEM (m)')
plt.show()
