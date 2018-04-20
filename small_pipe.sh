source ~/.bashrc

i=`pwd|rev|cut -f 1 -d '/'|rev`

ref=/Users/mayabrandi/opt/cgMLST/klebsiella_pneumoniae/ref/GCF_000240185.1_ASM24018v2_cds_from_genomic.fna


bwa mem -R "@RG\tID:${i}\tSM:${i}" -t 4 -M -v 1  ${ref} ${i}_1.fastq.gz ${i}_2.fastq.gz > ${i}.sam

samtools view -Sb ${i}.sam >${i}.bam
samtools sort ${i}.bam >${i}.sorted.bam
samtools index ${i}.sorted.bam
freebayes -C 1 -f $ref  ${i}.sorted.bam |vcffilter -f "QUAL > 20" >  ${i}.qual20.vcf
python ../../../../make_gene_subset.py -i ../intersect_product_accesion.txt -f ${i}.qual20.vcf



