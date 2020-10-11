### Code repository for MBS BBK project

### Database setup
1. There must be an instance of PostgresSQL running on the same machine. There must be a user setup with the name 'theme-extractor' and the password 'tepassword'.
2. The SQL script /setup/db-setup.sql must be run as the postrgres user
3. The database must then be hosted on localhost:5432 (this is the default)

### Services installation
1. Make sure that python v3.7 is installed on the machine
2. Navigate to the project directory at the root level. Run `pip install -r requirements.txt` to install the packages used by the project
3. To run the API services, execute ‘python run_api.py’. This will host the API on port 5000 on localhost. 

### UI installation
1. Make sure that node v.12+ is installed on the machine
2. Navigate to `ui/theme-view`. Run `npm install` to install the project dependencies.
3. Run ‘ng serve’ in the same directory. This will serve the UI application on port 4200. 

### Notebooks installation
1. Follow the same instructions as for services steps 1 & 2
2. Navigate to the /notebooks folder and open the jupyter notebooks in a suitable notebook viewer (e.g. VS Code has one built in). Alternatively, follow the installation instructions at https://jupyter.org/ to download the full suite. 

### Manual

#### Launching the app
1. Navigate to 'http://localhost:4200' in your web browser of choice (this has been tested in Google Chrome and Microsoft Edge)
2. Navigate between the 'articles' and the 'themes' pages by clicking the buttons on the left

#### Loading in new data
1. Type in the following into the web browser 'http://localhost:5000/api/data-load'. This will trigger the data loading process. This should take around 4 hours. 

### Acknowledgements
The following file incorporates code from the github project 'theguardian-api-python' (https://github.com/prabhath6/theguardian-api-python): /services/data_extractor/guardian_connector.py. This was directly copied rather than imported as a library due to issues arising from attempting to install it in the normal way. 

All other files have been written by the author (Matthew Burnett-Stuart)