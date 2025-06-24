# Setup

Step 1: Add a .env file with
```
API_KEY=XXXXXXX
API_SECRET=XXXXXXX
STAGE_URL=XXXXXXX    # only needed if testing staging env
PARENT_XID=XXXXXXX   # only needed for interface=ui
ORG_XID=XXXXXXX      # only needed for interface=ui

```

Step 2: Create and switch to python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Step 3: Install packages 
```
pip install -r requirements.txt
```

Step 4: Run the tests
```
#### To see help
python3 app.py -h

#### To run all the tests 
python3 app.py -a  

#### To run selected tests
python3 app.py -s "BANDWIDTH REPORT BY VISITOR" "ENCODING REPORT BY VIDEO RENDITION"
```
