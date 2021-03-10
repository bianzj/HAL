from util.myfun import *




indir_lst = r'i:/S3b_LST/'
indir_tif = r'i:/S3b_TIF/'
outdir = r'D:\data\LSTDA\S3b_day\\'
infile_ref = r'J:/type.tif'
[ref,ns,nl,nb,geog,proj] = read_image_gdal(infile_ref)
symbol = 'S3b'
dayNight = 'day'
nodiff = 7.5


diff = np.zeros([nl, ns])
count = np.zeros([nl, ns])
difave = np.zeros([nl, ns])
for kmonth in range(1,13):
    for kday in range(1,32):
        doy = date2DOY(2019, kmonth, kday)
        infile_nadir_lst = indir_lst + symbol + '_2019%03d' % doy + '_' + dayNight + '_lst.tif'
        infile_obliq_lst = indir_lst + symbol + '_2019%03d' % doy + '_' + dayNight + '_lst_obliq.tif'
        infile_nadir_cloud = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_cloud.tif'
        infile_obliq_cloud = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_cloud_obliq.tif'
        print(infile_nadir_lst, infile_obliq_lst)
        if os.path.exists(infile_nadir_lst) != 1 or os.path.exists(infile_obliq_lst) != 1: continue
        [lst_nadir, ns, nl, nb, geog, proj] = read_image_gdal(infile_nadir_lst)
        [lst_obliq, ns, nl, nb, geog, proj] = read_image_gdal(infile_obliq_lst)
        [cloud_nadir, ns, nl, nb, geog, proj] = read_image_gdal(infile_nadir_cloud)
        [cloud_obliq, ns, nl, nb, geog, proj] = read_image_gdal(infile_obliq_cloud)
        dif = lst_obliq - lst_nadir
        ind = (dif > -nodiff) * (dif < nodiff) * (dif != 0) * (cloud_nadir == 0) * (cloud_obliq == 0)
        diff[ind] = diff[ind] + dif[ind]
        count[ind] = count[ind] + 1

outfile1 = outdir + '2019'+'year_count.tif'
outfile2 = outdir + '2019'+'year_lstda.tif'
ind = count > 0
difave[ind] = diff[ind]/count[ind]
write_image_gdal(count,ns,nl,1,geog,proj,outfile1)
write_image_gdal(difave,ns,nl,1,geog,proj,outfile2)