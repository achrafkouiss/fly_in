run: 
	@python3 network.py

clean:
	@find . -type d -name __pycache__ -exec rm -r {} \+