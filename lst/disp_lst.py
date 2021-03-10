from util.myfun import *

indir = 'D:\data\S3A_LST/'

fig, axs = plt.subplots(ncols=1, figsize=(8, 4))
infile = indir + '2019_lstda.tif'
[mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
mydata[mydata==0] = None
plt.imshow(mydata,cmap='jet',vmax=2,vmin=-2)
plt.colorbar()
axs.set_axis_off()
plt.show()

#
# infile = indir + '201901_lstda.tif'
# [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
# plt.imshow(mydata,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
#
#
# dongbei = mydata[350:650,2100:2400]
# dongbei[dongbei==0] = None
# plt.imshow(dongbei,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# beijing = mydata[600:800,1700:1900]
# beijing[beijing==0] = None
# plt.imshow(beijing,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# shanghai = mydata[1000:1200,1900:2100]
# shanghai[shanghai==0] = None
# plt.imshow(shanghai,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# shenzhen = mydata[1400:1600,1600:1800]
# shenzhen[shenzhen==0] = None
# plt.imshow(shenzhen,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# infile = indir + '201908_lstda.tif'
# [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
# plt.imshow(mydata,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
#
#
# dongbei = mydata[350:650,2100:2400]
# dongbei[dongbei==0] = None
# plt.imshow(dongbei,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# beijing = mydata[600:800,1700:1900]
# beijing[beijing==0] = None
# plt.imshow(beijing,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# shanghai = mydata[1000:1200,1900:2100]
# shanghai[shanghai==0] = None
# plt.imshow(shanghai,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
#
# shenzhen = mydata[1400:1600,1600:1800]
# shenzhen[shenzhen==0] = None
# plt.imshow(shenzhen,cmap='jet',vmax=3,vmin=-3)
# plt.colorbar()
# plt.show()
