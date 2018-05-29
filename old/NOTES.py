
######## (1)    skapa cgMLST gen set fil från cgMLST_ncs_genes_cut.csv - hämtad frånhttp://www.cgmlst.org/ncs
ref_feature_table=CDS_GCF_000009885.1_ASM988v1_feature_table.txt
for i in  $(cat cgMLST_ncs_genes_cut.csv); do grep $i $ref_feature_table|cut -f 11 >>cgMLST_ncs_genes_product_accesion.csv ;done


ref_genome_feature_table=GCF_000240185.1_ASM24018v2_feature_table.txt
for i in  $(cat cgMLST_ncs_genes_product_accesion.csv); do grep $i $ref_genome_feature_table|cut -f 11 >>cgMLST_ncs_genes_product_accesion_ref_genome.csv;done


#### (2) krymp SNP-vcferna till att bara inehålla cg-gener
for i in MIC*;do cd $i; python ../make_gene_subset.py -i ../cgMLST_ncs_genes_product_accesion_ref_genome.csv -f ${i}.qual20.vcf;cd ..;done

### (3) List with differing genes
for i in MIC*; do for j in MIC*; do grep lcl ${i}/cg_${i}.qual20.vcf ${j}/cg_${j}.qual20.vcf|cut -f 1,2,5| cut -f 6,7 -d '_'|sort|uniq -u|cut -f 1 -d '_'|sort|uniq>>differing_genes;done;done

cat differing_genes |sort|uniq>>uniq_differing_genes

## (4) kolla coverage på specifik position##

ref=/Users/mayabrandi/opt/cgMLST/klebsiella_pneumoniae/ref/GCF_000240185.1_ASM24018v2_cds_from_genomic.fna

for samp in M*;do echo ${samp};for i in $(cat uniq_differing_genes);do id=`grep $i ${samp}/cg_${samp}.qual20.vcf|cut -f 1|sort|uniq`;loci=`grep $i ${samp}/cg_${samp}.qual20.vcf|cut -f 2|sort|uniq`;for j in $loci;do echo $id; bam-readcount -f $ref ${samp}/${samp}.sorted.bam ${id}:$j-$j|cut -f 1,4>>${samp}/loci_cov;done ;done;done

## (5) skapa genlista med gener som har dålig cov på vissa snp-positioner
make_low_cov_gene_list.py
cat low_cov |sort|uniq>>low_cov_uniq

### (6) skapa nya vcfer utan gener med low cov
for i in MIC*;do cd $i;python ../make_gene_subset.py -i ../cgMLST_ncs_genes_product_accesion_ref_genome.csv -f cg_*.qual20.vcf -c;cd ..;done


### (7) Skapa ny distans fil med bara high cov genes
for i in MIC*; do for j in MIC*; do nr=`grep lcl ${i}/high_cov*${i}.qual20.vcf ${j}/high_cov*${j}.qual20.vcf|cut -f 1,2,5|cut -f 6,7 -d '_'|sort|uniq -u|cut -f 1 -d '_'|sort|uniq|wc -l`; echo $i $j $nr >>high_cov_dist.txt ;done;done

### (8) Skapa distans fil med alla
for i in MIC*; do for j in MIC*; do nr=`grep lcl ${i}/cg_${i}.qual20.vcf ${j}/cg_${j}.qual20.vcf|cut -f 1,2,5|cut -f 6,7 -d '_'|sort|uniq -u|cut -f 1 -d '_'|sort|uniq|wc -l`; echo $i $j $nr >>dist.txt ;done;done

