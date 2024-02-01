The project MUST be run in Python 3.11.2 for TensorFlow to work. Python 3.2+ is not supported yet.
After installing 3.11.2, create a new venv using this interpreter. Then, install all the requirements:
pip install -r requirements.txt
Put any files that aren't relevant to the project in your folder so we can keep everything organized. 
If you add any libraries, update the requirements.txt and commit the changes:
  pip freeze > requirements.txt
  git commit requirements.txt -m "add new library"
  git push origin $BRANCH

