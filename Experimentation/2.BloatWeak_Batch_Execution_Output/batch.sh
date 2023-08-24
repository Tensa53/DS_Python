#!/bin/sh

i=1
tot=439

while read line; do
	echo "*Executing BloatWeak for project n.$i/$tot: $line"
	#mkdir /home/daniele/git/NICHE_projects/BloatWeak_Out/Cloneables/$line/
	mkdir /home/daniele/git/Validation/BloatWeak_Out/$line/
	python -m venv /home/daniele/anyenv$i
	source /home/daniele/anyenv$i/bin/activate
	pip install --upgrade pip --quiet
	pip install -r /home/daniele/git/BloatWeak/requirements.txt --quiet
	#python3 bloatWeak.py /home/daniele/git/NICHE_projects/Repo/Cloneables/$line/ /home/daniele/git/NICHE_projects/BloatWeak_Out/Cloneables/$line/
	python3 bloatWeak.py /home/daniele/git/Validation/Repo/$line/ /home/daniele/git/Validation/BloatWeak_Out/$line/
	echo ""
	deactivate
	rm -R /home/daniele/anyenv$i/
	i=$((i+1))
done < projects-list-validation.txt
