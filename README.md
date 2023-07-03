# Bloated Dependency Detection in Python Projects
This repository stores the source code of the PyCD fork. I decided to fork this project because i had to do some works for my thesis related to dependency smells. I created a new script called Bloatweak that finds bloated dependencies affected by vulnerabilities. The old readme is still here (at the end of this page) and i just changed the links to the directories.

# BloatWeak: Extracting bloated dependencies and their related vulnerabilities from dependency configuration  files

The building block of BloatWeak, describing its execution flow:
![building_block](https://github.com/Tensa53/DS_Python/blob/master/building_block/building_block.svg "building_block")

To use BloatWeak, you can run the command:
```
python3 bloatWeak.py <pro_path> <todir>
```
- *pro_path* refers to the path for a Python project or a configuration file.
- *todir* refers to a directory that stores all the output obtained from BloatWeak

BloatWeak takes together many tools to find bloated dependencies and their related vulnerabilities. To correctly use BloatWeak, you need to follow these steps:

- Install those packages with pip:
	- fawltydeps
	- safety
	- pandas
	- astunparse (used by GetDep_ast.py)
	- toml (used by GetDep_ast.py)
- Run the command above to launch the script

You can find the script into the [PyCD](https://github.com/Tensa53/DS_Python/tree/master/PyCD) directory.

As of now, this script takes the fawltydeps output on a text file, where every line identifies a candidate bloated dependency. Thanks to pandas, it joins the lines with the respective dependency version obtained from the PyCD csv output. We have now obtained a file that respects the requirements file layout, so it's possible to use this as the input of safety to check any known vulnerabilities. 

All you can find in your shell output is the list of all bloated dependency, the ones affected by vulnerabilities are highlighted with 'VULNERABLE!' message on the same line.

So with BloatWeak we have combined these three tools, all you can find in your directory are three files:
- pycd_out.csv: the ouput obtained from the PyCD tool with GetDep_ast.py script.
- requirements-unused.txt: the output obtained from fawltydeps and joined with the version column of the table stored in pycd_out.csv file.
- safety_out.json: the ouput obtained from the safety tool that had analized the requirements-unused.txt dependencies file.

# Towards Better Dependency Management: A First Look at Dependency Smells in Python Projects (old readme)
This repository stores the source code of PyCD and all materials in this study

We studied three dependency smells in Python projects.
- Missing dependency
- Bloated dependency
- Version constraint inconsistency

## Materials
The following sections describe the main materials included in this repository.    
[PyCD](https://github.com/Tensa53/DS_Python/tree/master/PyCD). This folder stores the source code of PyCD. 

[Extracting Imports](https://github.com/Tensa53/DS_Python/tree/master/Extracting_Imports). This folder stores the source code that extracts dependency relations from source code 

[Evaluation of PyCD](https://github.com/Tensa53/DS_Python/tree/master/Evaluation_of_PyCD). This folder stores all results of the approaches (PyCD, GDG, and Libraries.io). In particular, "Evaluation of PyCD/Truth" stores our constructed ground truth.

The evaluation dataset is constructed from open-source projects in Github. You can find the name of these project in "Evaluation of PyCD/evaluate_pycd_212.xlsx". 

[Empirical Study](https://github.com/Tensa53/DS_Python/tree/master/Empirical_Study). This folder stores the results for emipircal study.
Our empirical study is conducted on 132 open-source Python projects in Github. You can find the name of these projects in "Empirical Study/Details of 132 projects.xlsx" folder. 

[Harmful DS report](https://github.com/Tensa53/DS_Python/tree/master/Harmful_DS_report) This folder stores the list of the links to 39 reported issues for harmful dependency smells.
