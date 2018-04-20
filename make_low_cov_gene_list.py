
samps=['MIC3551A7','MIC3558A2','MIC4109A19','MIC4109A20','MIC4202A34','MIC4202A36','MIC4202A37','MIC4202A39','MIC4353A1']
f2=open('low_cov','a')
for samp in samps:
    print samp
    f=open(samp+'/loci_cov','r')
    genes=f.readlines()
    for gene in genes:
        id,cov= gene.split()
        if int(cov)<20:
            print id
            f2.write(id.split('_')[-2]+'\n')
    f.close()

f2.close()
