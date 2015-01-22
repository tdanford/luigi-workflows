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

There are several different WMSs to evaluate. 

* Tug
* Galaxy 
* Hadoop-based WMS: (Oozie, Cascading, Crunch, Spark) 
* Luigi 
* Snakemake
* Ruffus
* Queue
* Cloud-based WMS: (Amazon workflow service, Google dataflow?) 
* Jenkins
* make


System Evaluation 
-----------------

| System      | Distinct Tasks | Failure | Monitor | Hadoop | Language | 3rd-Party | Docs | License | Local/Cluster | 
|:-----------:|:--------------:|:-------:|:-------:|:------:|:--------:|:---------:|:----:|:-------:|:-------------:|
|  Tug        |                |         |         |        |    X     |           |      |    X    |       X       | 
|  Galaxy     |       X        |   ???   |    X    |        |          |           |      |         |               | 
|  Hadoop WMS |       X        |    X    |         |        |          |           |      |         |               |  
|  Luigi      |       X        |    X    |         |        |          |           |      |         |               |  
|  Snakemake  |      ???       |   ???   |         |        |          |           |      |         |               |  
|  Ruffus     |      ???       |   ???   |         |        |          |           |      |         |               |  
|  Queue      |       X        |    X    |         |        |          |           |      |         |               |  
|  Cloud WMS  |       X        |    X    |         |        |          |           |      |         |               |  
|  Jenkins    |                |         |         |        |          |           |      |         |               |  


