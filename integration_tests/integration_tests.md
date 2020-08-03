### Integration tests

The purpose of this folder is to house integration tests. We often will want integration tests to work across (and
compare) versions. As such we have this folder outside of the main lambda_functions folder structure.


The integration test suites aren't part of the pipeline as they create real data on the sirius side
(against whatever branch you point them to). Their purpose is to give us confidence that all our real world
infrastructure is working as it should for all of our happy and unhappy paths.

They are to be run either locally against our mock or against real world infrastructure (not live!).

### Prerequisites

To set up for the integration tests you should check a few things first:

 - In `conftest.py`, check that the url you are pointing to is correct.
 - In `conftest.py`, check that the `configs_to_test` is set to what you want to test against.
 - In `conftest.py`, take note of the ids you will be testing against.


 ### Run the tests
 create a virtualenv:

 - `virtualenv venv`
 - `source venv/bin/activate`

 `cd` into this folder and run `pip install -r requirements.txt` or
 whatever requirements you need for your version.

 Run `aws-vault exec identity -- python -m pytest -n2 --dist=loadfile --html=report.html --self-contained-html` and all integration tests will run against your setup.


 ### Gotchas

 Make sure you are able to assume digideps dev role with your credentials or tests will not work.
You may need to update some Sirius data. This is temporary, we're going to get them to create some stable
test data for us, but for now, you need to log into Cloud9 and run:
`UPDATE cases SET onlinelpaid = 'A33718377316' WHERE uid = 700000000013;`
