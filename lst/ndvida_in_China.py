from util.myfun import *


############################
### functions
##############################

indir0 = r'D:/data/S3A_LST/'
outdir = r'D:/data/S3A_LST/'
infile_ref = r'D:\data\S3A_LST\ref.tif'
[ref,ns,nl,nb,geog,proj] = read_image_gdal(infile_ref)
symbol = 'S3A'

for kmonth in range(1,13):
    diff = np.zeros([nl, ns])
    count = np.zeros([nl, ns])
    difave = np.zeros([nl,ns])
    indir1 = indir0 + '2019_%02d'%kmonth+'/'
    for kday in range(1,32):
        doy = date2DOY(2019,kmonth,kday)
        infile1 = indir1 + symbol + '_2019%03d' % doy + '_day_lst.tif'
        infile2 = indir1 + symbol + '_2019%03d' % doy + '_day_lst_obliq.tif'
        print(infile1,infile2)
        if os.path.exists(infile1) != 1 or os.path.exists(infile2) != 1: continue
        [lst_nadir,ns,nl,nb,geog,proj] = read_image_gdal(infile1)
        [lst_obliq,ns,nl,nb,geog,proj] = read_image_gdal(infile2)
        dif = lst_obliq - lst_nadir
        ind = (dif > -5) *(dif < 5) * (dif != 0)
        diff[ind] = diff[ind] + dif[ind]
        count[ind] =  count[ind] + 1
    outfile1 = outdir + '2019%02d'%kmonth+'_count.tif'
    outfile2 = outdir + '2019%02d'%kmonth+'_lstda.tif'
    ind = count > 0
    difave[ind] = diff[ind]/count[ind]
    write_image_gdal(count,ns,nl,1,geog,proj,outfile1)
    write_image_gdal(difave,ns,nl,1,geog,proj,outfile2)



