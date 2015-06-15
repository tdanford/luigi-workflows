Design ideas and experiments for modeling workflows
=======

Luigi Workflows 
==================

This package contains code for representing batch, pipelined processing jobs (e.g. pre-processing and variant-calling from Illumina data).  

It also includes wrapper/glue code for running these pipelines using one or more third-party workflow managers.

Workflow Manager Requirements 
-----------------------------

The first task was to understand what the requirements for a workflow system would be.  

* Represent separate tasks in a distinct way, to allow for re-use of tasks between pipelines
* Handle task failure and restarting
* Ability to monitor task and pipeline execution
* Support a migration path to Hadoop/Spark, if necessary
* Pipelines to be expressed in a commonly-used language (i.e. Java, Python, makefiles) without need for users to learn an obscure, difficult language or completely new "workflow DSL" 
* Actively developed and supported by a third-party 
* Minimize licensing requirements
* Ability to run in single-node (local/development mode) or cluster-based systems
* Automation 

Workflow System Options 
-----------------------


* Tug
* Galaxy 
* Hadoop-based WMS
 * Oozie, 
 * Cascading, 
 * Crunch, 
 * Spark-based
* Luigi 
* Snakemake
* Ruffus
* Queue
* Cloud-based WMS
 * Amazon SWS
 * Google Cloud Dataflow 
* Jenkins
* make


System Evaluation 
-----------------

| System      | Tasks | Failure | Monitor | Hadoop | Language | 3rd-Party | Docs | License | Local/Cluster | 
|:-----------:|:-----:|:-------:|:-------:|:------:|:--------:|:---------:|:----:|:-------:|:-------------:|
|  Tug        | &nbsp;|  &nbsp; | &nbsp;  | &nbsp; |    X     |   &nbsp;  |&nbsp;|    X    |       X       | 
|  Galaxy     |   X   |   ???   |    X    |  ???   |    X     |     X     |  X   |    X    |      ???      | 
|  Hadoop WMS |   X   |    X    |    X    |   X    |    X     |     X     |  X   |    X    |       X       |  
|  Luigi      |   X   |    X    |    X    |   X    |    X     |     X     |  X   |    X    |       X       |  
|  Snakemake  |  ???  |   ???   |  &nbsp; | &nbsp; |   ???    |    (1)    |  X   |    X    |     &nbsp;    |  
|  Ruffus     |  ???  |   ???   |  &nbsp; | &nbsp; |   ???    |    (1)    |  X   |    X    |     &nbsp;    |  
|  Queue      |   X   |    X    |  &nbsp; | &nbsp; |   &nbsp; |     X     |  X   | &nbsp;  |       X       |  
|  Cloud WMS  |   X   |    X    |    X    | &nbsp; |    X     |     X     |  X   |    X    |       X       |  
|  Jenkins    | &nbsp;|  &nbsp; |    X    | &nbsp; |    X     |     X     |  X   |    X    |     &nbsp;    |  
|  Make       | &nbsp;|  &nbsp; |  &nbsp; | &nbsp; |    X     |     X     |  X   |    X    |     &nbsp;    |  

(1): it's externally developed, but not clear what the support is


