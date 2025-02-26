
## How to run

### Create virtual environment and install dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the back end

```
cd server
python app.py
```

### Run the front end

In a **different terminal**, navigate to the project's directory and run

```
source .venv/bin/activate
cd frontend
python frontend.py
```

## Exploring the current app

Go to your browser.

If you go to [http://127.:0.0.1:8000](http://127.:0.0.1:8000), you should see the front end of your app. The landing page is a page that lists the current available pages (Add student, List students, Delete students)

Click on the different links, and explore the pages.

Go to the source code and try to map which parts of the code trigger the different functionality you see.

## Exploring the tests

Check the two test cases in `tests/browser/test_student_forms.py`. Try to understand the code there

Now run the current tests and make sure they pass (You must make sure you have your front end and backend running as above. The commands you type here are in a **third** terminal)

```
source .venb/bin/activate
pytest
```

## Your Task

Add two tests for the delete student page:

Test 1: makes sure that the homepage has the delete student link and goes to the right page
Test 2: makes sure delete student works as expected (hint: you may need to first add a student so you are sure the email you will delete exists)