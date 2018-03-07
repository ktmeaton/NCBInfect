
### Manual Curation  

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

