# BloatWeak: Extracting bloated dependencies and their related vulnerabilities from dependency configuration  files
To use BloatWeak, you can run the command:
```
python3 bloatWeak.py <pro_path> <todir>
```
- *pro_path* refers to the path for a Python project or a configuration file.
- *todir* refers to a directory that store all the output obtained from BloatWeak

BloatWeak takes together many tools to find bloated dependencies and their related vulnerabilities. To correctly use BloatWeak, you need to follow these guidelines:

- Copy bloatWeak.py into the PyCD directory
- Install those packages with pip:
	- fawltydeps
	- safety
	- pandas
	- all the other packages used by GetDep_ast.py script
- Run the command above to launch the script

As of now, this script takes the fawltydeps output on a file, where every line identifies a candidate bloated dependency. Thanks to pandas, it joins the lines with the respective dependency version obtained from the PyCD csv output. We have now obtained a file that respects the requirements file layout, so it's possible to use this as the input of safety to check any known vulnerabilities. 

So with BloatWeak we have combined these three tools, all you can find in your directory are these three files:
- pycd_out.csv: the ouput obtained from the PyCD tool with GetDep_ast.py script.
- requirements-unused.txt: the output obtained from fawltydeps and combined with the version columns of the table stored in pycd_out.csv file.
- safety_out.json: the ouput obtained from the safety tool that had analized the requirements-unused.txt dependencies file.
