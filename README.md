# Bloated Dependencies Detection in ML Python Projects
This repository stores the source code of the PyCD fork. I decided to fork this project because i had to do some works for my thesis related to dependency smells in ML Python Projects. I created a new script called Bloatweak that finds bloated dependencies affected by known vulnerabilities. All the related materials to the original project are stored in [DS_Python](https://github.com/Tensa53/BloatWeak/tree/master/DS_Python/) folder.

# BloatWeak: Extracting bloated dependencies and their related vulnerabilities from dependency configuration files

The building block of BloatWeak, describing its execution flow:
![building_block](https://github.com/Tensa53/BloatWeak/blob/master/Building_Block/building_block.svg "Building_Block")

To use BloatWeak, you can run the command:
```
python3 bloatWeak.py <pro_path> <todir>
```
- *pro_path* refers to the path for a Python project or a configuration file.
- *todir* refers to a directory that stores all the output obtained from BloatWeak

BloatWeak takes together many tools to find bloated dependencies and their related vulnerabilities. To correctly use BloatWeak, you need to follow these steps:


- Create a python virtual environment, running the following command: `python -m venv thenameofyourvenv`
- Install the packages listed in requirements.txt with pip, you can simple run the following command: `pip install -r /path/to/requirements.txt`
- These are all the packages that are going to be installed:
	- [fawltydeps](https://github.com/tweag/fawltydeps)==0.12.0
	- [pandas](https://github.com/pandas-dev/pandas)==2.0.3
    - [packaging](https://github.com/pypa/packaging)==21.3
	- [astunparse](https://github.com/simonpercivall/astunparse)==1.6.3 (used by GetDep_ast.py)
	- [requests](https://github.com/psf/requests)==2.31.0 (used by GetDep_ast.py)
	- [toml](https://github.com/uiri/toml)==0.10.2 (used by GetDep_ast.py)
- Run the command above to launch the script

You can find the script into the [bloatWeak](https://github.com/Tensa53/BloatWeak/tree/master/bloatWeak) directory.

As of now, this script executes *GetDep_ast.py* script of [PyCD](https://github.com/Tensa53/BloatWeak/tree/master/DS_Python/PyCD) and takes the output in a csv file, then temporary stores it in a collection of dependency objects. After executing fawltydeps , reads line by line its output stored in fawltydeps_out.txt, visit the dependencies collection and if finds the respective dependency of the line, marks it as a bloated one (only the ones required for the installation/deployment of the software). After reading the fawltydeps output, temporary installs the bloated dependencies with pip and run again fawltydeps to check if the deps are really bloated. Thanks to the dependency objects collection, checks which ones are vulnerable, reading the [safetyDB](https://github.com/pyupio/safety-db) (*safetydb_insecure_full.json*).

So with BloatWeak we have combined different tools. All you cand find in your directory are these files:
- **pycd_out.csv**: the ouput obtained from the PyCD tool with GetDep_ast.py script.
- **safetyDB_out.csv**: the filtered db with all the vulnerabilities information of the analyzed project's dependencies
