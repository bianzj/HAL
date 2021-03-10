from util.myfun import *
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd


infile_type = 'J:/type.tif'
[type,ns,nl,nb,geog,proj] = read_image_gdal(infile_type)

indir_da = r'D:\data\LSTDA\S3B_day/'
indir_ci = r'J:\CI_AREA/'

infile_lstda = indir_da + '2019_lstda_big.tif'
infile_radda = indir_da + '2019_radtda_big.tif'
infile_tada = indir_da + '2019_tada_big.tif'
infile_sm = indir_da + '2019_smda_big.tif'
infile_fvcda = indir_da + '2019_fvcda_big.tif'
infile_vza = indir_da + '2019_vzada_big.tif'
infile_hs = indir_da + '2019_hsda_big.tif'
infile_tcw = indir_da + '2019_tcwda_big.tif'

[lstda,ns,nl,nb,geog,proj] = read_image_gdal(infile_lstda)
[tada,ns,nl,nb,geog,proj] = read_image_gdal(infile_tada)
[radda,ns,nl,nb,geog,proj] = read_image_gdal(infile_radda)
[fvcda,ns,nl,nb,geog,proj] = read_image_gdal(infile_fvcda)
[smda,ns,nl,nb,geog,proj] = read_image_gdal(infile_sm)
[vzada,ns,nl,nb,geog,proj] = read_image_gdal(infile_vza)
[hsda,ns,nl,nb,geog,proj] = read_image_gdal(infile_hs)
[tcwda,ns,nl,nb,geog,proj] = read_image_gdal(infile_tcw)


num = 7
coeffs = np.zeros([num,nl,ns])

for kl in range(nl):
    print(kl,nl)
    for ks in range(ns):

        temp = lstda[:,kl,ks]

        ind = (np.abs(temp)>0.001)
        if np.sum(ind) < 10:continue
        lstda0 = lstda[ind,kl,ks]
        tada0 = tada[ind,kl,ks]-273.15
        radda0 = radda[ind,kl,ks]/3600
        fvcda0 = fvcda[ind,kl,ks]
        sm0 = smda[ind,kl,ks]
        vzada0 = vzada[ind,kl,ks]
        hsda0 = hsda[ind,kl,ks]
        tcwda0 = tcwda[ind,kl,ks]

        results = np.stack([lstda0,radda0,tada0,tcwda0,sm0,fvcda0,vzada0,hsda0])
        results = np.transpose(results)

        df = pd.DataFrame(results,columns = ['lstda','rad','ta','tcw','sm','fvc','vza','hs'])
        formula = 'lstda ~ rad + ta + tcw + sm + fvc + vza + hs '
        anova_results = anova_lm(ols(formula,df).fit())
        dd = df.corr('spearman')
        coeffs[:,kl,ks] = np.asarray(dd["lstda"][1:])

outfile = indir_da + 'coeffs.tif'
write_image_gdal(coeffs,ns,nl,num,geog,proj,outfile)
