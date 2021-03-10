from util.myfun import *



infile = r'D:\data\S3A_LST/ref.tif'
[types,ns,nl,nb,geog,proj] = read_image_gdal(infile)

unique_types = np.unique(types)
typeNum = np.size(unique_types)
monthNum = 12

lstda = np.zeros([typeNum,monthNum])
lstdaa = np.zeros([typeNum,monthNum])

indir = r'D:\data\S3A_LST/'
for kmonth in range(0,monthNum):
    infile = indir + '2019%02d_lstda.tif'%(kmonth+1)
    [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
    for ktype in range(typeNum):
        type = unique_types[ktype]
        ind = (type == types) *(mydata > -10)*(mydata < 10) *(mydata != 0 )
        temp = mydata[ind]
        lstda[ktype,kmonth] = np.average(temp)
        lstdaa[ktype,kmonth] = np.std(temp)

fig, ax = plt.subplots()
x = np.linspace(1,12,12)
for ktype in range(typeNum):
    plt.plot(x,lstda[ktype,:],color=plt.get_cmap('jet')(np.linspace(0, 1, typeNum)[ktype]))
    ax.fill_between(x,lstda[ktype,:] - lstdaa[ktype,:], lstda[ktype,:] + lstdaa[ktype,:],color=plt.get_cmap('jet')(np.linspace(0, 1, typeNum)[ktype]),alpha = 0.5)
plt.legend(['Evergreen Needleaf Forest','Evergreen Boradleaf Forest','Deciduous Needleaf Forest',
           'Deciduous Broadleaf Forest','Mixed Forest','Closed Shrublands','Open Shrublands','Woody Savannas',
           'Savanas','Grasslands','Permanent Wetlands','Croplands','Urban Areas','Croplands/Natural Vegetation Mosaic',
            'Snow and Ice','Barren or Sparsely Vegetated'],loc='upper center', fontsize=8,ncol=2)
plt.ylim([-3.5,5])
plt.show()

