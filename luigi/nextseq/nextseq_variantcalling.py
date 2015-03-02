#!/usr/bin/env python

import luigi 
import os
import subprocess
import logging
import uuid

def touchfile(filename):
    if not os.path.exists(filename):
        outf = open(filename, 'w')
        outf.close()

# "Generates" the FASTQ -- in practice, we'd replace the body of the 'run' method 
# here with code that grabs one or more FASTQ files from an external source (e.g. 
# S3) 
class GetFastq(luigi.Task):
    sample = luigi.Parameter(description="The name of the sample's fastq files to get")

    def filename(self):
        return '%s.fastq' % self.sample

    def run(self):
        touchfile(self.filename())
    
    def output(self):
        return luigi.LocalTarget(self.filename())

class AlignFastq(luigi.Task):
    sample = luigi.Parameter(description="The name of the sample to align")
    bwa_db = luigi.Parameter(description="The BWA database name to use", default="e_coli")
    logger = logging.getLogger('luigi-interface')

    def output_filename(self):
        return '%s.sam' % self.sample

    def temp_filename(self): 
        return '%s.sam' % (str(uuid.uuid4()))
    
    def run(self):
        for fastq in self.input():
            self.logger.info('fastq: %s' % fastq.path)
            temp = self.temp_filename()
            with open(temp, 'w') as outf:
                bwa_dbname = str(self.bwa_db)
                child_proc = subprocess.Popen(['bwa', 'mem', bwa_dbname, fastq.path], stdout=outf)
                child_proc.wait()
            os.rename(temp, self.output_filename())

    def requires(self):
        return [ GetFastq(self.sample) ]

    def output(self):
        return luigi.LocalTarget(self.output_filename())

class ConvertSamToBam(luigi.Task):
    sample = luigi.Parameter(description="The name of the sample to convert")
    logger = logging.getLogger('luigi-interface')

    def output_filename(self):
        return '%s.bam' % self.sample

    def temp_filename(self): 
        return '%s.bam' % (str(uuid.uuid4()))

    # samtools view -b -S ${sample}.sam > ${sample}.bam
    def run(self):
        for sam in self.input():
            self.logger.info('sam: %s' % sam.path)
            temp = self.temp_filename()
            with open(temp, 'w') as outf: 
                childproc = subprocess.Popen(['samtools', 'view', '-b', '-S', sam.path], stdout=outf)
                childproc.wait()
            os.rename(temp, self.output_filename())
            
    def requires(self):
        return [ AlignFastq(self.sample) ]

    def output(self):
        return luigi.LocalTarget(self.output_filename())

class SortBam(luigi.Task):
    sample = luigi.Parameter(description='the name of the sample whose bam is to be sorted')
    logger = logging.getLogger('luigi-interface')

    def requires(self):
        return [ ConvertSamToBam(self.sample) ]

    def temp_filename(self):
        return '%s_sorted.%s.bam' % ( self.sample, uuid.uuid4() )

    # java -jar /usr/local/share/java/SortSam.jar I=${sample}.bam O=${sample}_sorted.bam SO=coordinate
    def run(self):
        bam = self.input()[0]
        temp = self.temp_filename()
        with open(temp, 'w') as outf: 
            childproc = subprocess.Popen(['java', '-jar', '/usr/local/share/java/SortSam.jar',
                                          'I=%s' % bam.path, 'O=%s' % temp, 'SO=coordinate'])
            childproc.wait()
        os.rename(temp, '%s_sorted.bam' % self.sample)

    def output(self):
        return luigi.LocalTarget('%s_sorted.bam' % self.sample)
    

class MarkDuplicates(luigi.Task):
    sample = luigi.Parameter(description='the name of the sample in which to mark duplicates')
    logger = logging.getLogger('luigi-interface')

    def requires(self):
        return [ SortBam(self.sample) ]

    def metrics_file(self):
        return '%s_dedup_metrics.txt' % self.sample

    def temp_filename(self):
        return '%s_dedup.%s.bam' % ( self.sample, uuid.uuid4() )

    # java -jar /usr/local/share/java/MarkDuplicates.jar I=${sample}.bam O=${sample}_dedup.bam
    def run(self):
        bam = self.input()[0]
        self.logger.info('bam: %s' % bam.path)
        temp = self.temp_filename()
        with open(temp, 'w') as outf: 
            childproc = subprocess.Popen(['java', '-jar', '/usr/local/share/java/MarkDuplicates.jar',
                                          'I=%s' % bam.path, 'O=%s' % temp, 'M=%s' % self.metrics_file()])
            childproc.wait()
        os.rename(temp, '%s_dedup.bam' % self.sample)

    def output(self):
        return luigi.LocalTarget('%s_dedup.bam' % self.sample)

class Pipeline(luigi.Task):
    sample = luigi.Parameter(description='the name of the sample to process') 
    logger = logging.getLogger('luigi-interface')
    
    def requires(self):
        return [ MarkDuplicates(self.sample) ]
    
    def run(self): pass

if __name__=='__main__':
    luigi.run()

