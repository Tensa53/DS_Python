# Experimentation

In this folder are stored all the output results of the Experimentation section of this work. The Experimentation is divided in three different phases:
1. **Project Cloning**: Through the repository link, the source code of the project is being downloaded;
2. **BloatWeak Execution**: The tool is executed on the source code of the project to obtain the output files;
3. **Measure Script execution**: The script called *measures_proj.py* is executed to extract from the output files of the BloatWeak Execution, the following measures:
	- Number of Dependencies
	- Number of Bloated Dependencies
	- Number of Vulnerable Dependencies
	- Number of Bloated&Vulnerable Dependencies
	- Number of vulnerabilities

All the phases are executed in batch mode on all the projects analyzed of the [NICHE](https://github.com/soarsmu/NICHE) dataset
