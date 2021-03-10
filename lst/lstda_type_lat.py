from util.myfun import *
import seaborn as sns


infile = r'D:\data\S3A_LST/ref.tif'
[types,ns,nl,nb,geog,proj] = read_image_gdal(infile)
targetArea = 'D:\data\S3A_LST//ref.tif'
dataset = gdal.Open(targetArea)
if dataset == None:
    print(targetArea + " ")
ns = dataset.RasterXSize
nl = dataset.RasterYSize
im_bands = dataset.RasterCount
data = dataset.ReadAsArray(0, 0, ns, nl)
geog = dataset.GetGeoTransform()
proj = dataset.GetProjection()
nsi = np.zeros([nl, ns])
nli = np.zeros([nl, ns])
for k in range(nl):
    nli[k, :] = k
    nsi[k, :] = np.linspace(0, ns - 1, ns)
nli = np.reshape(nli, -1)
nsi = np.reshape(nsi, -1)
###
temp1, temp2 = imagexy2geo(dataset, nli, nsi)
lon, lat = geo2lonlat(dataset, temp1, temp2)
lat = np.reshape(lat,[nl,ns])
lon = np.reshape(lon,[nl,ns])



unique_types = np.unique(types)
typeNum = np.size(unique_types)-1
monthNum = 12
latNum = 7

latmin = np.min(lat)
latmax = np.max(lat)
dlat = (latmax-latmin)/latNum
lstda = np.zeros([typeNum,latNum])
lstdaa = np.zeros([typeNum,latNum])


indir = r'D:\data\S3A_LST/'
infile = indir + '201901_lstda.tif'
[mydata, ns, nl, nb, geog, proj] = read_image_gdal(infile)

for ktype in range(typeNum):
    for klat in range(latNum):
        ind = (lat >= (latmin+dlat*klat)) * (lat <= (latmin + dlat+dlat*klat))*\
              (ktype+1 == types) * (mydata > -10) * (mydata < 10) * (mydata != 0)
        lattemp = mydata[ind]
        lstda[ktype,klat] = np.average(lattemp)
        lstdaa[ktype,klat] = np.std(lattemp)

fig, ax = plt.subplots()
lstda = np.transpose(lstda)
lstda = np.flip(lstda,0)
sns.heatmap(lstda,
            yticklabels=['>45','40-45','35-40','30-35','25-30','20-35','<25'],
            xticklabels=np.linspace(1,16,16,dtype=np.int),cmap='jet')

plt.show()