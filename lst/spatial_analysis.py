from util.myfun import *
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd


infile_type = 'J:/type.tif'
[type,ns,nl,nb,geog,proj] = read_image_gdal(infile_type)

indir_da = r'D:\data\LSTDA\S3B_NIGHT/'
indir_ci = r'J:\CI_AREA/'
lstda_ = np.asarray([])
tada_ = np.asarray([])
radda_ = np.asarray([])
fvcda_ = np.asarray([])
smda_ = np.asarray([])
cida_ = np.asarray([])
count_ = np.asarray([])
type_ = np.asarray([])

iffirst = 1
for kmonth in range(1,13):

    infile_lstda = indir_da+'2019%02d'%kmonth+'_lstda.tif'
    infile_tada = indir_da +'2019%02d'%kmonth+'_tada.tif'
    infile_radda = indir_da+'2019%02d'%kmonth+'_radda.tif'
    infile_fvcda = indir_da+'2019%02d'%kmonth+'_fvcda.tif'
    infile_count = indir_da+'2019%02d'%kmonth+'_count.tif'
    infile_ci  = indir_ci + '2019_month%02d'%kmonth + '.tif'
    infile_sm = indir_da+'2019%02d'%kmonth+'_smda.tif'

    [lstda,ns,nl,nb,geog,proj] = read_image_gdal(infile_lstda)
    [tada,ns,nl,nb,geog,proj] = read_image_gdal(infile_tada)
    [radda,ns,nl,nb,geog,proj] = read_image_gdal(infile_radda)
    [fvcda,ns,nl,nb,geog,proj] = read_image_gdal(infile_fvcda)
    [count,ns,nl,nb,geog,proj] = read_image_gdal(infile_count)
    [cida,ns,nl,nb,geog,proj] = read_image_gdal(infile_ci)
    [smda,ns,nl,nb,geog,proj] = read_image_gdal(infile_sm)

    if iffirst == 0:
        lstda_ = np.hstack([lstda_,lstda])
        tada_ = np.hstack([tada_,tada])
        radda_ = np.hstack([radda_,radda])
        fvcda_ = np.hstack([fvcda_,fvcda])
        cida_ = np.hstack([cida_,cida])
        smda_ = np.hstack([smda_,smda])
        count_ = np.hstack([count_,count])
        type_ = np.hstack([type_,type])
    else:
        lstda_ = lstda
        tada_ = tada
        radda_ = radda
        fvcda_ = fvcda
        cida_ = cida
        smda_ = smda
        count_ = count
        type_ = type
        iffirst = 0




# ind = (count > 3)*((type == 12) | (type == 14))
# ind = (count > 3)*(type ==13)
# ind = (count > 3)* (type == 16)
ind = (count_ > 3)* (type_ < 12)
lstda0 = lstda_[ind]
tada0 = tada_[ind]-273.15
radda0 = radda_[ind]/3600
fvcda0 = fvcda_[ind]
type0 = type_[ind]
ci0 = cida_[ind]
sm0 = smda_[ind]
results = np.stack([lstda0,tada0,fvcda0,ci0,sm0])
results = np.transpose(results)
df = pd.DataFrame(results,columns = ['lstda','ta','fvc','ci','sm'])
formula = 'lstda ~ ta + fvc + ci + sm '
anova_results = anova_lm(ols(formula,df).fit())
print(df.corr('spearman'))
