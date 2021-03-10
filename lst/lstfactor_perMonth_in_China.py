from util.myfun import *
from util.fitting_kernels import *

############################
### ta for each month
##############################

symbol = 'S3A'
indir_lst = r'j:/S3A_LST/'
indir_tif = r'J:/S3A_TIF/'
indir_fvc = r'J:\FVC_AREA/'
outdir = r'D:\data\LSTDA\S3A_day\\'
dayNight = 'day'

symbol = 'S3B'
indir_lst = r'I:/S3B_LST/'
indir_tif = r'I:/S3B_TIF/'
indir_fvc = r'J:\FVC_AREA/'
outdir = r'D:\data\LSTDA\S3B_DAY\\'
dayNight = 'day'

nodiff = 7.5
infile_ref = r'J:/type.tif'
[ref,ns,nl,nb,geog,proj] = read_image_gdal(infile_ref)

for kmonth in range(1,13):
    ta_diff = np.zeros([nl, ns])
    rad_diff = np.zeros([nl, ns])
    fvc_diff = np.zeros([nl, ns])
    sm_diff = np.zeros([nl, ns])

    vza_diff = np.zeros([nl,ns])
    hs_diff = np.zeros([nl,ns])

    count = np.zeros([nl, ns])


    for kday in range(1,32):
        doy = date2DOY(2019,kmonth,kday)
        infile_nadir_lst = indir_lst + symbol + '_2019%03d' % doy + '_'+dayNight+'_lst.tif'
        infile_obliq_lst = indir_lst + symbol + '_2019%03d' % doy + '_'+dayNight+'_lst_obliq.tif'
        infile_nadir_cloud = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_cloud.tif'
        infile_obliq_cloud = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_cloud_obliq.tif'

        infile_ta = indir_tif + symbol + '_2019%03d' % doy + '_'+dayNight+'_ta.tif'
        infile_rad = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_rad.tif'
        infile_sm = indir_tif + symbol + '_2019%03d' % doy + '_' + dayNight + '_tcw.tif'
        infile_fvc = indir_fvc + '2019_doy%03d' % doy + '_fvc.tif'


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


        [vza1, ns, nl, temp, geog, proj] = read_image_gdal(infile_nadir_vza)
        [vza2, ns, nl, temp, geog, proj] = read_image_gdal(infile_obliq_vza)
        [sza1, ns, nl, temp, geog, proj] = read_image_gdal(infile_nadir_sza)
        [sza2, ns, nl, temp, geog, proj] = read_image_gdal(infile_obliq_sza)
        [vaa1, ns, nl, temp, geog, proj] = read_image_gdal(infile_nadir_vaa)
        [vaa2, ns, nl, temp, geog, proj] = read_image_gdal(infile_obliq_vaa)
        [saa1, ns, nl, temp, geog, proj] = read_image_gdal(infile_nadir_saa)
        [saa2, ns, nl, temp, geog, proj] = read_image_gdal(infile_obliq_saa)


        [rad, ns, nl, temp, geog, proj] = read_image_gdal(infile_rad)
        [ta, ns, nl, temp, geog, proj] = read_image_gdal(infile_ta)
        [sm, ns, nl, temp, geog, proj] = read_image_gdal(infile_sm)
        [fvc, ns, nl, temp, geog, proj] = read_image_gdal(infile_fvc)

        vin1 = kernel_Vin(vza1)
        vin2 = kernel_Vin(vza2)
        vindif = vin2 - vin1
        hs1 = kernel_RLhs(sza1,vza1,np.abs(saa1-vaa1))
        hs2 = kernel_RLhs(sza2,vza2,np.abs(saa2-vaa2))
        hsdif = hs2 - hs1

        dif = lst_obliq - lst_nadir
        ind = (dif > -nodiff) *(dif < nodiff) * (dif != 0)  *(cloud_nadir==0)*(cloud_obliq==0)

        rad_diff[ind] = rad_diff[ind] + rad[ind]
        ta_diff[ind] = ta_diff[ind] + ta[ind]
        sm_diff[ind] = sm_diff[ind] + sm[ind]
        fvc_diff[ind] = fvc_diff[ind] + fvc[ind]

        vza_diff[ind] = vza_diff[ind] + vindif[ind]
        hs_diff[ind] = vza_diff[ind] + hsdif[ind]


        count[ind] =  count[ind] + 1

    outfile3 = outdir + '2019%02d' % kmonth + '_radda.tif'
    outfile4 = outdir + '2019%02d' % kmonth + '_tada.tif'
    outfile5 = outdir + '2019%02d' % kmonth + '_smda.tif'
    outfile6 = outdir + '2019%02d' % kmonth + '_fvcda.tif'
    outfile7 = outdir + '2019%02d' % kmonth + '_vzada.tif'
    outfile8 = outdir + '2019%02d' % kmonth + '_hsda.tif'


    ind = count > 0
    rad_diff[ind] = rad_diff[ind]/count[ind]
    ta_diff[ind] = ta_diff[ind] / count[ind]
    sm_diff[ind] = sm_diff[ind] / count[ind]
    fvc_diff[ind] = fvc_diff[ind] / count[ind]
    vza_diff[ind] = vza_diff[ind] / count[ind]
    hs_diff[ind] = hs_diff[ind] / count[ind]

    write_image_gdal(rad_diff,ns,nl,1,geog,proj,outfile3)
    write_image_gdal(ta_diff,ns,nl,1,geog,proj,outfile4)
    write_image_gdal(sm_diff,ns,nl,1,geog,proj,outfile5)
    write_image_gdal(fvc_diff,ns,nl,1,geog,proj,outfile6)
    write_image_gdal(vza_diff,ns,nl,1,geog,proj,outfile7)
    write_image_gdal(hs_diff,ns,nl,1,geog,proj,outfile8)



