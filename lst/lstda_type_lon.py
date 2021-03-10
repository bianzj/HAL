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
lonNum = 10

lonmin = 80
lonmax = 130
dlat = (lonmax-lonmin)/lonNum
lstda = np.zeros([typeNum,lonNum])
lstdaa = np.zeros([typeNum,lonNum])



indir = r'D:\data\S3A_LST/'
infile = indir + '2019_lstda.tif'
[mydata, ns, nl, nb, geog, proj] = read_image_gdal(infile)

for ktype in range(typeNum):
    for klon in range(lonNum):
        ind = (lon >= (lonmin+dlat*klon)) * (lon <= (lonmin + dlat+dlat*klon))*\
              (ktype+1 == types) * (mydata > -10) * (mydata < 10) * (mydata != 0)
        lontemp = mydata[ind]
        lstda[ktype,klon] = np.average(lontemp)
        lstdaa[ktype,klon] = np.std(lontemp)

fig, ax = plt.subplots()

sns.heatmap(lstda,
            xticklabels=['80-85',' ','90-95',' ','100-105',' ','110-115',' ','120-125',' '],
            yticklabels=np.linspace(1,16,16,dtype=np.int),cmap='jet')
plt.xlabel('Longitute')
plt.ylabel('Surface type')

plt.show()