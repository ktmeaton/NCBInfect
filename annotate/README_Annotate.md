
### Manual Curation  

## PRIORITY QUESTIONS
Cui or Sahl genomes?
REMEMBER: E1979001 was removed from Cui genome set (replaced with original Eppinger genome)
Harbin35/Nicholisk
125 B Plague Bombay: Too Long Branch Length: Reassemble

## Strain Filtering
- Removed all CO92 strains (Reference Genome supplied separately to avoid duplicates)

## Bioproject Filtering
- Removed PRJNA240677 (laboratory passage experiment)
- (See Below) PRJNA41469 was NOT REMOVED (KIM D27 is a lab strain generated from KIM10)
- PRJNA412669 was NOT REMOVED, even though isolate UC91309 was a laboratory infection. Retained for curiosity.
	UPDATE: Closely related to the Kurdistan strains, this is likely an "attenuated" variant of D27?
	Chosing to keep PRJNA41469
- Removed PRJNA288602 (strain KIM 10v) Laboratory Strain
- Removed PRJNA277922 (strain KIM 6) Laboratory Strain
- Removed PRJNA240677 (strain KIM1001) Laboratory Strain
- Removed PRJNA340278, Praire dog passage experiment
- Removed PRJNA315671, differential gene expression study
- Removed PRJNA293891, laboratory growth study
- Removed PRJNA291739, in silico algorithm study
- Removed PRJNA254747, radiation experiment
- Removed PRJNA240083 (strain KIM 5) Labratory Strain
- Removed PRJNA205233, small ncRNA experiment
- NOTE: Bioprojects associated with Johnson et al. (2015) Thirty-Two Complete Genomes... advertise extremely high coverage!!!

## BioSample Filtering
- 125 B Bombay: Extraordinarily long branch length, attempting reassembly
- Algeria 3 Options:
	Algeria3; GCF_9... ; Scaffold Level; 50X Cov; 561 contigs; 4427555; 2016; orig nomenclature; 2.ANT1 Grouping (BAD)
	Algeria 3; GCF_0... ; Contig Level; 20X Cov; 87 contigs; 4637400; 2015; mod nomenclature; Original Assembly; Orientalis Grouping (GOOD)
 	\*\*\* Biotyped Orientalis
	CONCLUSION -> Retain Algeria 3 (GCF_0) and delete other, because this is placed similarly to orig publication phylo placement.

- Angola: Removed SAMN02604042 and SAMN03177051; Problematic Branch Length
- A1122: Removed SAMN02603531, newer assembly is available
- E1977001: Independently sequenced in two studies (Eppinger and Cui):
	Falls in the same clade: Likely won't have a crucial difference
	In the parsnp.filtered.vcf: they differ by 3 SNPs (1 is LCB, all 3 are derived in GCA_000324785.1, ie. Cui 2013 assembly.
	Delete Cui, use original Eppinger genome.

- Harbin 35; Extraordinarily long branch length. Options:
	Harbin 35; GCF_000186725.1; 2011;
	Harbin35; GCF_000834275.1; 2015; 
	Both are complete genomes. They differ by 88 SNPs. The SRA record is available. Attempt reassembly? No = requires PacBio data.
	Could just reassembly using the illumina data to see if masking hides SNPs.

- Nicholisk 41: Extraordinarily long branch length. Breaks up the duplicates of Harbin 35.
	Assembled in same sequencing project as Harbin35

- FV-1: Extradordinarily long branch length.
	Removed, because I have little interested in more representation from US: Arizona prairie dogs.

- Nepal516: Duplicates present
	GCF_000182485.1; Scaffolds; 2009; Deleted 
	GCF_000013805.1; Complete Genome; 2006; Retained
	Close relatives of 195/P (broken up by it, poorly supported)	

- Pestoides F: Duplicates present
	GCF_000834315.1: Complete Genome; 2015; 723X; Removed SAMN03121016
	GCF_000016445.1: Complete Genome; 2007; Retained

## Recoding
- BioSample "KIM10+" is the original KIM genome sequenced (according to Bioproject accession in Cui et al. (2013))
	NOTE: KIM10+ was originally isolated in 1961, not 1968
	NOTE: KIM10+ is reported to have lots of sequencing errors.
- EV76 in Cui et al. (2013) annotation is actually the chinese variant (EV76-CN),
	the BioSample record says "China:Lanzhou" as geographic location, assume time after 1922.
- Mystery strain ?? from BioProject PRJNA47685 is CMCCo10807
- KIM D27 coded as year: 1968, geography: Kurdistan for now.
- Kimberley D17 re-encoded from Far East to South Africa.
- PEXU2 - Unknown date or geography
- EV76D - Unknown date or geography
- SCPM-O study: A few strains are estimated geographic location using biovar (ex. caucasica)
- PRJNA241466 missing strain info, pulled from SRA and publication
- El Dorado recode as El Dorado, NM, 2002
- 125 B recode as <1920
- PRJNA17687, recode as Marmot himalayana, Xinjiang China, 1973
- PRJNA169908, recode as Peru,  Trujillo
- PRJEB19335, fill in missing strain name from description

## Estimation
- Pestoides isolates geography was estimated from documented plague foci and phylogeographic clustering
- Strain 195/P is dated to before 1950, as it was sent from Dr. PM Wagle at Haffkine Institute (Bombay, India) and
	received by the Hooper Foundation in 1950.

## Publications
Gibbons et al. (2012) Comparative Genomics of 2009 Seasonal Plague (Yersinia pestis) in New Mexico 
Revazishvili et al. (2008) Characterisation of Yersinia pestis isolates from natural foci of plague in the Republic of Georgia
Golubov et al. (2004) Structural Organization of the pFra Virulence-Associated Plasmid of Rhamnose-Postive Yersinia pestis
Tsereteli et al. (2002) Plague in Southern Caucasus
Shen et al. (2010) Complete genome sequences of Yersinia pestis from natural foci in China.
Chen et al. (1955) X. Specific Precipitation of Pasteurella Pestis Antigens and Antibodies in Gels
Castro-Nallar et al. (2015) Concordance and discordance of sequence survey methods for molecular epidemiology
Bearden et al. (2009) Attenuated enzootic (pestoides) isolates of Yersinia pestis express active aspartase
Yan et al. (2014) Two-Step Source Tracing Strategy of Yersinia pestis
D'Aunoy et al. (1923) Studies on Bacillus Pestis: I. Optimum and Limiting Hydrogen-Ion Concentration for the Growth of Bacillus Pestis
Harbin35: Wilmoth et al. (1996) Identification of Yersinia pestis by BBL crystal enteric/nonfermenter identification system.
Java9: Hudson et al. (1976) Electrophoretic Studies of the Geographic Distribution of Yersinia pestis Protein Variants

## Raw Data
- KIM10+ - Known sequencing error problems
- All samples from PRJNA194125, consensus calls were done with Geneious
- All samples from PRJNA47685, known problematic genomes
- All samples from Peruvian plague work (2010), too fragmentary

## Ancient DNA Projects
- PRJEB19335 - Early Pandemic, Stone/Bronze
- PRJEB13664 - Second Pandemic, Spyrou et al. (2016)
- PRJEB12163 - Second Pandemic, Bos et al. (2016)
- PRJEB14851 - Justinian, Feldman et al. (2016)
TO ADD
- SRP008060

## Modern SRA-Exclusive Projects
- PRJNA269675: 10 Bonus "USSR" strains from the SCPM-O project. Not needed now.
- [Y] PRJNA341721: 30 Madagascar strains from 2003-2012. Needed now (I only have 2 Madagascar assemblies, and they're closely related to 1990s India plague)
- [Y] PRJNA184590: 4 Madagascar strains from 1991-1999. Needed now.
- PRJNA241466: 3 Xinghai strains from the 1950-1960s, 6 strains from Xinghai from 2009. Not currently interested.
- PRJNA194125: 15 strains from USA: NM. Not currently interested.
- PRJNA194125: 1 strain from Manchuria before 1936 (KUMA D11). Not currently interested, but maybe.
- [Y] PRJNA194125: Many interesting one-off strains:
		- TS D5 - 1953 India/Indonesia
		- Kimberley D17 - Unknown Date - South Africa
		- Java D88 - Unknown Date - Indonesia, Java
- [Y] PRJEB2029: 1 Orientalis strain from Turkey, IP674, 1952. Very interested.
- [Y] NCTC5923: 1 strain from London/Javan 1939. 1 strain from London/Bombay 1920. Interested.
		


## Assembly Record Parsing
- Removed Duplicates (Old assembly accessions for)
	CA88-4125
	PY-14
	PY-34
	PY-54
	PY-58
	PY-42
	113
	125 B Plague Bombay
	9
	24H
	EV76

## Text File of Assembly Accessions
sed replace all ">" and "<" characters with an empty string

sed replace all "GCF_" with "GCA_"

while read line; \
    do \
        ACCESSION=$(echo "$line" | awk -F $'\t' '{print $3}'); 
        DATE=$(echo "$line" | awk -F $'\t' '{print $36}'); \
	GEO=$(echo "$line" | awk -F $'\t' '{print $36}'); \
	INFILE=$(ls $ACCESSION*); \
	OUTFILE=$(echo $DATE"_"$ACCESSION".fna.gz")
	echo "Copying" $INFILE "to" $OUTFILE; \
	cp $INFILE ../rename/$OUTFILE; \
	done < ../../database/Assembly_InnerJoin_BioSample_Dedup.txt

echo -e "Species\tStrain\tDate\tGeography\tGeographyDate" > annotation.txt

awk -F $'\t' '{if (NR > 1){DATE=$36;ACCESSION=$3".fna"; GEO=$37; STRAIN=$34; print DATE"_"ACCESSION"\t"STRAIN"\t"DATE"\t"GEO"\t"DATE " " GEO}}'
../database/Assembly_InnerJoin_BioSample_Dedup.txt >> annotation.txt

sed -i 's/"//g' annotation.txt
sed -i 's/://g' annotation.txt
sed -i 's/,//g' annotation.txt

mv 283.pilon.mask.fasta 1994_IP283.fna; \
mv 542.pilon.mask.fasta 1952_IP542.fna; \
mv 543.pilon.mask.fasta 1953_IP543.fna; \
mv 557.pilon.mask.fasta 1963_IP557.fna; \
mv 562.pilon.mask.fasta 1947_IP562.fna; \
mv 579.pilon.mask.fasta 1898_IP579.fna

echo -e "1994_IP283.fna\tIP283\t1994\tIndia\t1994 India" >> annotation.txt; \
echo -e "1952_IP542.fna\tIP542\t1952\tKenya\t1952 Kenya" >> annotation.txt; \
echo -e "1953_IP543.fna\tIP543\t1953\tCongo\t1953 Congo" >> annotation.txt; \
echo -e "1963_IP557.fna\tIP557\t1963\tKurdistan\t1963 Kurdistan" >> annotation.txt; \
echo -e "1947_IP562.fna\tIP562\t1947\tKurdistan\t1947 Kurdistan">> annotation.txt; \
echo -e "1898_IP579.fna\tIP579\t1898\tIndia\t1898 India">> annotation.txt

for file in `ls *.fna*`; do sed -i 's/,//g' $file; done
for file in `ls *.fna*`; do sed -i 's/ /_/g' $file; done

## SQL
# Inner Join Assembly and BioSample
SELECT *
FROM Assembly
INNER JOIN BioSample 
ON 
(Assembly.biosample = Biosample.biosample_accession
OR Assembly.biosample = Biosample.biosample_secondary_accession)

# Full Outer Join (Retain only BioSample columns)
SELECT * FROM 
(SELECT Assembly.accession,BioSample.* FROM BioSample
LEFT JOIN Assembly
ON (Assembly.biosample = Biosample.biosample_accession OR Assembly.biosample = Biosample.biosample_secondary_accession)
UNION
SELECT Assembly.accession,BioSample.* FROM Assembly
LEFT JOIN BioSample
ON Assembly.biosample = Biosample.biosample_accession OR Assembly.biosample = Biosample.biosample_secondary_accession)
WHERE accession IS NULL
