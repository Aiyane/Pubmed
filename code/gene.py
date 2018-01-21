# coding: utf-8


def getGene():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\gene_name.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getOrgan():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\organ.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getLocus():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\gene_locus.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getOrf():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\gene_orf.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getPrimary():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\gene_primary.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getSynonym():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\gene_synonym.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def getRes():
    for gene, organ, locus, orf, pri, syn in zip(getGene(), getOrgan(), getLocus(), getOrf(), getPrimary(), getSynonym()):
        if "soy" in organ.lower() or "glycine" in organ.lower():
            yield '$'.join([gene.strip(), organ.strip(), locus.strip(), orf.strip(), pri.strip(), syn.strip(), "\n"])

for line in getRes():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\allGene.txt", "a", encoding="utf8") as f:
        f.write(line)
