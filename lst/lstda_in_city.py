from util.myfun import *
import matplotlib.pyplot as plt
import seaborn as sns

def point2area(data,pointx,pointy,off = 1):
    xstart = pointx - off
    xend = pointx + off+1
    ystart = pointy - off
    yend = pointy + off+1
    area = data[xstart:xend,ystart:yend]

    return np.average(area[area!=0])

#############################
### City information
#############################
infile = r'D:\data\S3A_LST/city_location.txt'
cityInfo = read_txt_str(infile)
cityNum = len(cityInfo)
cityInfo = np.asarray(cityInfo)
imagex = np.asarray([x[0] for x in cityInfo], dtype=np.int)
imagey = np.asarray([x[1] for x in cityInfo], dtype = np.int)
lon = np.asarray([x[2] for x in cityInfo],dtype = np.float)
lat = np.asarray([x[3] for x in cityInfo],dtype = np.float)


#############################
### LSTDA VS CITY
#############################

# monthNum = 12
# lstda = np.zeros([cityNum,monthNum])
# indir = r'D:\data\S3A_LST/'
# for kmonth in range(0,monthNum):
#     infile = indir + '2019%02d_lstda.tif'%(kmonth+1)
#     [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
#     for kcity in range(cityNum):
#         lstda[kcity,kmonth] = point2area(mydata,imagex[kcity],imagey[kcity])
# ind = np.argsort(lat)
# lstda = lstda[ind,:]
# lat = lat[ind]
# for kcity in range(cityNum):
#     plt.plot(lstda[kcity,:],color=plt.get_cmap('jet')(np.linspace(0, 1, cityNum)[kcity]))
# plt.show()

#############################
### LSTDA VS LAT
#############################

latNum = 5
monthNum = 12
latmin = np.min(lat)
latmax = np.max(lat)
dlat = (latmax-latmin)/latNum
lstda = np.zeros([latNum,monthNum])
lstdaa = np.zeros([latNum,monthNum])

indir = r'D:\data\S3A_LST/'
for kmonth in range(0,monthNum):
    infile = indir + '2019%02d_lstda.tif'%(kmonth+1)
    [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
    for klat in range(latNum):
        ind = (lat >= (latmin+dlat*klat)) * (lat <= (latmin + dlat+dlat*klat))
        imagextemp = imagex[ind]
        imageytemp = imagey[ind]
        indNum = np.sum(ind)
        lattemp = []

        for kind in range(indNum):
            temp = (point2area(mydata, imagextemp[kind], imageytemp[kind]))
            if (temp > 5): continue
            if(temp < -5): continue
            if(np.isnan(temp)):continue
            if(np.isinf(temp)):continue
            lattemp.append(temp)
        lattemp = np.asarray(lattemp)
        lstda[klat,kmonth] = np.average(lattemp)
        lstdaa[klat,kmonth] = np.std(lattemp)

fig, ax = plt.subplots()
x = np.linspace(1,12,12)
for klat in range(latNum):
    plt.plot(x,lstda[klat,:],color=plt.get_cmap('jet')(np.linspace(0, 1, latNum)[klat]))
    ax.fill_between(x,lstda[klat,:] - lstdaa[klat,:], lstda[klat,:] + lstdaa[klat,:],alpha = 0.5)
plt.legend(['<25','25-30','30-35','35-40','>40'])
plt.xlabel('month')
plt.ylabel('Directional Anisotropies (K)')
plt.show()
