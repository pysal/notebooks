# developer Makefile for repeated tasks
# 

.PHONY: clean

nb:
	docker run -it --rm  -p 8888:8888 -p 4000:4000 -v ${PWD}:/home/jovyan/work darribas/gds_dev:4.0

term:
	docker run -it --rm  -p 8888:8888 -p 4000:4000 -v ${PWD}:/home/jovyan/work darribas/gds_dev:4.0 sh -c "/bin/bash"


clean: 
	find . -name "*.pyc" -exec rm '{}' ';'
	find pysal -name "__pycache__" -exec rm -rf '{}' ';'
	rm -rf dist
	rm -rf build
	rm -rf PySAL.egg-info
	rm -rf tmp

