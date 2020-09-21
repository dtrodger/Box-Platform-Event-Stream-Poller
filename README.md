## Box Platform Event Stream Poller 
### Runtime Requirements  
[Python 3.6+](https://www.python.org/downloads/)  
[PIP package manager](https://pip.pypa.io/en/stable/installing/)  
[virtualenv](https://virtualenv.pypa.io/en/latest/)  
### Set up and Run  
1. From the project root folder, create a Python 3.6+ virtual environment  
`$ virtualenv --python=python3 env`  
2. Activate the virtual environment  
`$ source env/bin/activate`  
3. Install the project dependencies  
`$ pip install -r requirements.txt`  
4. Copy the configuration file at `configuration/example.yml` into the same directory. Name the file dev.yml   
5. Add Box Platform JWT keys and event type names and handler function names to the configuration file at line 3  
6. Add Box Platform event types to process to the configuration file at line 13  
7. Run the CLI with a flag referencing the configuration filename without the .yml extension   
`$ python src/cli/main.py poll-events` 
