#################################### INTERSECT ####################################

######## Skapa intersect från feature table
for i in *feature_table.txt; do case=`echo $i|cut -f 1 -d .`; grep '^CDS' $i|cut -f 11 |sort|uniq>$case.genes;done
first_file=$(ls *.genes|head -1)
cp $first_file intersect
for i in *.genes;do sort $i intersect| uniq -d>temp;mv temp intersect ;done


### gör om till product_accesion
ref_feature_table=GCF_000240185.1_ASM24018v2_feature_table.txt
for i in  $(cat intersect); do grep $i $ref_feature_table|cut -f 11 >>intersect_product_accesion.txt;done

#### Hntera fasta filerna
# merge files from different lanes
for i in M*;do cd $i; cat *_*_*_1.fastq.gz > ${i}_1.fastq.gz; cat *_*_*_2.fastq.gz > ${i}_2.fastq.gz;cd ..;done

# move unmerged files
for i in M*;do cd $i; mkdir unmerged;mv *_*_*_1.fastq.gz unmerged;mv *_*_*_2.fastq.gz unmerged;cd ..;done


################### aligna etc ###################
bash small_pipe.sh



### Skapa distans fil
for i in MIC*; do for j in MIC*; do nr=`grep lcl cg_${i}/${i}.qual20.vcf ${j}/cg_${j}.qual20.vcf|cut -f 1,2,5|cut -f 4,5,6 -d '_'|sort|uniq -u|cut -f 1|cut -f 1,2 -d '_'|sort|uniq|wc -l`; echo $i $j $nr>>dist.txt;done;done
for i in MIC*; do for j in MIC*; do nr=`grep lcl ${i}/${i}.qual20.vcf ${j}/${j}.qual20.vcf|cut -f 1,2,5|cut -f 4,5,6 -d '_'|sort|uniq -u|cut -f 1|cut -f 1,2 -d '_'|sort|uniq|wc -l`; echo $i $j $nr>>dist_wgs.txt;done;done



##### skapa consensus filer istället

samtools mpileup -uf $ref MIC3553A16.sorted.bam | bcftools call -c|vcfutils.pl vcf2fq > cns.fq
samtools mpileup -uf $ref MIC3551A7.sorted.bam | bcftools call -c|vcfutils.pl vcf2fq > cns.fq

## sen köra compare_consensus.py
