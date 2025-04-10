git clone
cd
# install python https://www.python.org/downloads/

# make the evnironment 
 python -m venv venv 

# On Windows activate
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

flask run
