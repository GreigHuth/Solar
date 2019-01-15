# Solar
Rudamentary simlulation of the first 4 planets of the solar system using beeman algorithm for approximating position.
Generates a little animation of the simulation and saves the Kinetic energy and Gravitational potential of the system to the 
corresponding files.


## Dependencies
* python 2 (any version)
* numpy (any version)
* matplotlib (any version)
* virtualenv
* pip

## install guide
**set-up virtualenv**

`virtualenv -p/where/python2/is .venv`

`source .venv/bin/activate`

**install dependencies**

`pip install -r requirements.txt` 

then navigate to directory and run 
`python main.py`

## Things to add and issues
* add the rest of the planets (although apparently that messes the whole thing up
* there is an issue if you are using ubuntu for windows, installing matplotlib through pip using ubuntu for windows causes
a problem with the window manager and it doesnt display anything.
