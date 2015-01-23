#!/usr/bin/env python

import luigi 
import os

class AlignFastq(luigi.Task):
    sample = luigi.Parameter(description="The name of the sample to align")
    
    def run(self):
        filename = '%s.sam' % self.sample
        if not os.path.exists(filename):
            outf = open(filename, 'w')
            outf.write('\n')
            outf.close()

    def output(self):
        return [ luigi.LocalTarget('%s.sam' % self.sample) ]

class ConvertSamToBam(luigi.Task):
    
    sample = luigi.Parameter(description="The name of the sample to convert")
    
    def run(self):
        for sam in self.input():
            print(sam.path)
            
    def requires(self):
        return AlignFastq(self.sample)

    def output(self):
        pass

if __name__=='__main__':
    luigi.run()

