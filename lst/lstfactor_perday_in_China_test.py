from util.myfun import *
from util.fitting_kernels import *

############################
### ta for each month
##############################

symbol = 'S3B'
indir_lst = r'I:/S3B_LST/'
indir_tif = r'I:/S3B_TIF/'
indir_fvc = r'J:\FVC_AREA/'
outdir = r'D:\data\LSTDA\S3B_NIGHT\\'
dayNight = 'NIGHT'

# symbol = 'S3B'
# indir_lst = r'I:/S3B_LST/'
# indir_tif = r'I:/S3B_TIF/'
# indir_fvc = r'J:\FVC_AREA/'
# outdir = r'D:\data\LSTDA\S3B_DAY\\'
# dayNight = 'DAY'

# symbol = 'S3A'
# indir_lst = r'J:/S3A_LST/'
# indir_tif = r'J:/S3A_TIF/'
# indir_fvc = r'J:\FVC_AREA/'
# outdir = r'D:\data\LSTDA\S3A_NIGHT\\'
# dayNight = 'NIGHT'

# symbol = 'S3A'
# indir_lst = r'J:/S3A_LST/'
# indir_tif = r'J:/S3A_TIF/'
# indir_fvc = r'J:\FVC_AREA/'
# outdir = r'D:\data\LSTDA\S3A_DAY\\'
# dayNight = 'DAY'

nodiff = 7.5
infile_ref = r'J:/type.tif'
[ref,ns,nl,nb,geog,proj] = read_image_gdal(infile_ref)

num = 110

radt_diff = np.zeros([num,nl, ns])
sm_diff = np.zeros([num,nl, ns])

count = np.zeros([nl,ns],dtype=np.int)

for kmonth in range(1,13):



    for kday in range(1,31):

        doy = date2DOY(2019,kmonth,kday)
        infile_nadir_lst = indir_lst + symbol + '_2019%03d' % doy + '_'+dayNight+'_lst.tif'
        infile_obliq_lst = indir_lst + symbol + '_2019%03d' % doy + '_'+dayNight+'_lst_obliq.tif'
        infile_nadir_cloud = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_cloud.tif'
        infile_obliq_cloud = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_cloud_obliq.tif'

        infile_ta = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_ta.tif'
        infile_rad = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_rad.tif'
        infile_sm = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_sm.tif'
        infile_fvc = indir_fvc + '2019_doy%03d' % doy + '_fvc.tif'
        infile_radt = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_radt.tif'


        infile_nadir_vza = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_vza.tif'
        infile_nadir_sza = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_sza.tif'
        infile_nadir_vaa = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_vaa.tif'
        infile_nadir_saa = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_saa.tif'
        infile_obliq_vza = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_vza_obliq.tif'
        infile_obliq_sza = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_sza_obliq.tif'
        infile_obliq_vaa = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_vaa_obliq.tif'
        infile_obliq_saa = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_saa_obliq.tif'


        print(infile_nadir_lst, infile_obliq_lst)
        if os.path.exists(infile_nadir_lst) != 1 or os.path.exists(infile_obliq_lst) != 1 or\
                os.path.exists(infile_nadir_vaa)!= 1: continue

        [lst_nadir,ns,nl,nb,geog,proj] = read_image_gdal(infile_nadir_lst)
        [lst_obliq,ns,nl,nb,geog,proj] = read_image_gdal(infile_obliq_lst)

        [cloud_nadir, ns, nl, nb, geog, proj] = read_image_gdal(infile_nadir_cloud)
        [cloud_obliq, ns, nl, nb, geog, proj] = read_image_gdal(infile_obliq_cloud)

        [rad, ns, nl, temp, geog, proj] = read_image_gdal(infile_rad)
        [sm, ns, nl, temp, geog, proj] = read_image_gdal(infile_sm)
        [radt, ns, nl, temp, geog, proj] = read_image_gdal(infile_radt)


        dif = lst_obliq - lst_nadir
        ind = (dif > -nodiff) *(dif < nodiff) * (dif != 0)  *(cloud_nadir==0)*(cloud_obliq==0) *(count < num)
        indd = np.where(ind == 1)
        sm_diff[count[indd],indd[0],indd[1]] = sm[indd]
        radt_diff[count[indd], indd[0], indd[1]] = radt[indd]+rad[indd]

        count[indd] =  count[indd] + 1



outfile5 = outdir + '2019_smda_big.tif'
outfile6 = outdir + '2019_radtda_big.tif'



write_image_gdal(sm_diff,ns,nl,num,geog,proj,outfile5)
write_image_gdal(radt_diff,ns,nl,num,geog,proj,outfile6)



