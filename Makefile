blog:
	# You may need to adjust to the python environment of your choice
	python3 automation/blogger.py

view:
	open -na "Google Chrome" --args --new-window http://localhost:5000/
	cd build && python -m http.server 5000

