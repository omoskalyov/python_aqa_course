# python_aqa_course

This repository has a Python project with implementation of the tasks related to the Python AQA course.  

Project status (master branch):  
[![CircleCI](https://circleci.com/gh/omoskalyov/python_aqa_course.svg?style=svg)](https://circleci.com/gh/omoskalyov/python_aqa_course)

The course content:  
Phase 1: Python Basics  
Phase 2: API Testing with Requests  
Phase 3: PyTest Parallel Execution  
Phase 4: UI Testing (Selenium)  
Phase 5: Reporting (Allure)  
Phase 6: Re-using API calls to prepare test Data  

The project has automation tests written on Python 3:  
 - tests/phase1 - unit tests for testing fibonacci function  
 - tests/phase2 - api (REST) tests for testing Jira site  
 - tests/phase3 - unit tests for testing "reruns" library  
 - tests/phase4 - web (Selenium) tests for testing Jira site  

Web tests are split across features via marks:
 - feature_login
 - feature_issue

To run tests from the project:
1. Ensure:
    - python 3 is installed on your OS  
    - ensure the python executable is added to the system path  
    - Chrome browser is installed on your OS  
2. Checkout the project to file system
3. Open console and go to the project root dir
4. Install and activate python virtual environment: 
    ``` 
    python3 -m venv venv  # on windows the filename could be just "python"  
    . venv/bin/activate
    ```  
5. Install project dependencies:  
    `pip install -r requirements.txt`
6. Download and install Allure framework (for reporting):
    ```
    curl -o allure-2.7.0.zip -Ls https://bintray.com/qameta/generic/download_file?file_path=io%2Fqameta%2Fallure%2Fallure%2F2.7.0%2Fallure-2.7.0.zip
    # or curl -o allure-2.7.0.zip -Ls https://github.com/allure-framework/allure2/releases/download/2.7.0/allure-2.7.0.zip  
    unzip allure-2.7.0.zip  
    export PATH=$PATH:$(pwd)/allure-2.7.0/bin/  
    echo "export PATH=$PATH:$(pwd)/allure-2.7.0/bin/" >> $BASH_ENV  
    allure --version
    ```  
7. Run the tests related to any phase:
   - define tests folder in the pytest.ini (e.g. "testpaths = tests/phase4")
   - run the next commands:
     - `chmod +x drivers/linux/chromedriver`
     - `pytest --reruns 2 -v -l --alluredir=test_results`  
     If you need to run tests in parallel on 4 threads:  
     - `pytest -n4 --alluredir=test_results`  
     If you need to run tests related to a specific feature (mark) only:  
      - `pytest -v -m feature_login --alluredir=test_results`
8. Generate Allure report via one of the next commands:  
 - `allure generate --clean test_results  #  the allure report will be generated to the "allure-report" folder`
 - `allure serve test_results  #  the report will be generated and automatically opened in default browser`
             
Notes:  
 - the project was created in PyCharm IDE.
      
           