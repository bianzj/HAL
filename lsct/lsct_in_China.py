from util.myfun import *


############################
### functions
##############################

indir0 = r'D:/data/S3B_LSCT/'
outdir = r'D:/data/S3B_LSCT/'
infile_ref = r'D:\data\S3A_LSCT\ref.tif'
[ref,ns,nl,nb,geog,proj] = read_image_gdal(infile_ref)
symbol = 'S3B'

for kmonth in range(1,13):
    diff = np.zeros([nl, ns])
    count = np.zeros([nl, ns])
    difave = np.zeros([nl,ns])
    indir1 = indir0 + '2019_%02d'%kmonth+'/'
    for kday in range(1,32):
        doy = date2DOY(2019,kmonth,kday)
        infile = indir1 + symbol + '_2019%03d'%doy+'_day_lsct.tif'
        print(infile)
        if os.path.exists(infile) != 1: continue
        [mydata,ns,nl,nb,geog,proj] = read_image_gdal(infile)
        soil = mydata[0,:,:]
        leaf = mydata[1,:,:]
        dif = soil - leaf
        ind = (dif > -25) *(dif < 25) * (dif != 0)
        diff[ind] = diff[ind] + dif[ind]
        count[ind] =  count[ind] + 1
    outfile1 = outdir + '2019%02d'%kmonth+'_count.tif'
    outfile2 = outdir + '2019%02d'%kmonth+'_dif.tif'
    ind = count > 0
    difave[ind] = diff[ind]/count[ind]
    write_image_gdal(count,ns,nl,1,geog,proj,outfile1)
    write_image_gdal(difave,ns,nl,1,geog,proj,outfile2)



