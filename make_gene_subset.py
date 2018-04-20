#!/usr/bin/env python
from argparse import ArgumentParser

def make_gene_subset(intersect_file, files):
    intersect = open(intersect_file).readlines()
    for f_name in files:
        get_sequence = False
        new_file = 'cg_'+f_name
        f = open(f_name,'r')
        f2 = open(new_file,'a')
        for line in f:
            if line[0]=='>':
                # Get header
                try:
                    gene_id = line.split('[protein_id=')[1].split(']')[0]+'\n'
                except:
                    gene_id= None
                if gene_id and gene_id in intersect:
                    f2.write(line)
                    get_sequence = True
                else:
                    get_sequence = False
            elif get_sequence:
                # Get sequence
                f2.write(line)

def make_vcf_subset(intersect_file, files):
    intersect = open(intersect_file).readlines()
    for f_name in files:
        new_file = 'cg_'+f_name
        f = open(f_name,'r')
        f2 = open(new_file,'a')
        for line in f:
            if line[0:3]=='lcl':
                # Get header
                try:
                    new_gene_id = '_'.join(line.split('_')[3:5])+'\n'
                    if len(new_gene_id.split())==1:
                        gene_id = new_gene_id
                except:
                    gene_id= None
                if gene_id and gene_id in intersect:
                    f2.write(line)
            else:
                f2.write(line)


def make_vcf_subset_2(intersect_file, f_name):
    intersect = open(intersect_file).readlines()
    low_cov_file=open('../low_cov_uniq','r')
    low_cov_genes=[]
    for line in low_cov_file.readlines():
        low_cov_genes.append(line.rstrip('\n'))
    new_file = 'high_cov_'+f_name
    f = open(f_name,'r')
    f2 = open(new_file,'a')
    for line in f:
        if line[0:3]=='lcl':
             # Get header
            try:
                new_gene_id = '_'.join(line.split('_')[3:5])+'\n'
                if len(new_gene_id.split())==1:
                    g=str(new_gene_id.split('_')[1])
                    if g.rstrip('\n') not in low_cov_genes:
                        gene_id = new_gene_id
                    else:
                        gene_id= None
            except:
                gene_id= None
            if gene_id and gene_id in intersect:
                f2.write(line)
        else:
            f2.write(line)



def main(args):
    if args.c:
        make_vcf_subset_2(args.i, args.f[0])
    else:
        make_vcf_subset(args.i, args.f)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i',
                       help='file with all core genes')
    parser.add_argument('-f', nargs='*',
                       help=('Fasta files with reference genomes that should be reduced to only contain core genes'))
    parser.add_argument('-c',action='store_true')
    args = parser.parse_args()
    main(args)

