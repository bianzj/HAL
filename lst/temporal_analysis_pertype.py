from util.myfun import *
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd


infile_type = 'J:/type.tif'
[type,ns,nl,nb,geog,proj] = read_image_gdal(infile_type)

indir_da = r'D:\data\LSTDA\S3B_day/'
indir_ci = r'J:\CI_AREA/'

infile_lstda = indir_da + '2019_lstda_big.tif'
infile_radda = indir_da + '2019_radda_big.tif'
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
[tcwda,ns,nl,nb,geog,proj] = read_image_gdal(infile_tcw)
[hsda,ns,nl,nb,geog,proj] = read_image_gdal(infile_hs)

ktype = 12
indtype = np.where(type == ktype)

# lstda0 = np.asarray([])
# tada0 = np.asarray([])
# radda0 = np.asarray([])
# fvcda0 = np.asarray([])
# sm0 = np.asarray([])
# vzada0 = np.asarray([])
# tcwda0 = np.asarray([])


lstda0 = lstda[:,indtype[0],indtype[1]]
tada0 = tada[:,indtype[0],indtype[1]]-273.15
radda0 = radda[:,indtype[0],indtype[1]]/3600
fvcda0 = fvcda[:,indtype[0],indtype[1]]
sm0 = smda[:,indtype[0],indtype[1]]
vzada0 = vzada[:,indtype[0],indtype[1]]
tcwda0 = tcwda[:,indtype[0],indtype[1]]
hsda0 = hsda[:,indtype[0],indtype[1]]

print('123')
ind = np.abs(lstda0)>0.01
lstda0 = lstda0[ind]
radda0 = radda0[ind]
tada0 = tada0[ind]
tcwda0 = tcwda0[ind]
sm0 = sm0[ind]
fvcda0 = fvcda0[ind]
vzada0 = vzada0[ind]
hsda0 = hsda0[ind]
print('456')
results = np.stack([lstda0,radda0,tada0,tcwda0,sm0,fvcda0,vzada0,hsda0])
results = np.transpose(results)

print('789')
df = pd.DataFrame(results,columns = ['lstda','rad','ta','tcw','sm','fvc','vza','hs'])
dd = df.corr('spearman')
print(dd)

# formula = 'lstda ~ rad + ta + tcw + sm + fvc + vza '
# anova_results = anova_lm(ols(formula,df).fit())
# print(anova_results)


