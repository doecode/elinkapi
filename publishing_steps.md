# Development Guide

Publishing to either test or production PyPI requires an account setup in the appropriate environment. For test, register [here](https://test.pypi.org/account/register/). For prod, register [here](https://pypi.org/account/register/). For ease-of-use, you can create a file, `$HOME/.pypirc`, that will automatically apply the credentials when publishing. You just need to generate an API token on the appropriate PyPI domain and format your `.pypirc` file as follows:

```
[pypi]
username = __token__
password = <the token value, including the 'pypi-' prefix>

[testpypi]
username = __token__
password = <the token value, including the 'pypi-' prefix>

```

## Development Instructions Test

### Publishing Package to test.pypi.org
1. Install the needed dependencies for packaging and publishing distribution archives: `pip install elinkapi[development]`
2. Make your desired changes within the project
3. Update the version number within the `pyproject.toml` file
4. Execute `python3 -m build`: this will generate 2 distribution archives that will be uploaded to pypi
5. Execute `twine upload --repository testpypi dist/*`: this will publish your packages to the test pypi index

### Importing the Package from test.pypi.org
1. Install the package, but don't grab the dependencies (pip will attempt to grab everything from the test server, which we do not want): `pip install --index-url https://test.pypi.org/simple/ --no-deps elinkapi`
2. Now install the other dependencies: `pip install elinkapi`
3. Or install them separately: `pip install requests pydantic urllib3==1.26.6`
4. `from elinkapi import Elink` allows instantiation of an API instance to use: 
```python
from elinkapi import Elink

api = Eink(token='your-token')
```
5. The pydantic classes can be fetched using `from elinkapi import Record, Organization`
6. Exceptions thrown may be accessed using `from elinkapi import exceptions` then reference each as
`except exceptions.BadRequestException as e:`

## Development Instructions Prod

### Publishing to Prod
1. Install the needed dependencies for packaging and publishing distribution archives `pip install elinkapi[development]`
2. Make your desired changes within the project
3. Update the version number within the `pyproject.toml` file
4. Execute `python3 -m build`: this will generate 2 distribution archives that will be uploaded to pypi
5. Execute `twine upload dist/*`: this will publish your packages to the test pypi index

### Importing the Package from Prod
1. Install the package: `pip install elinkapi`
2. `from elinkapi import Elink` allows instantiation of an API instance to use: 
```python
from elinkapi import Elink

api = Elink(token='your-token')
```
3. The pydantic classes can be fetched using `from elinkapi import Record, Organization`
4. Exceptions thrown may be accessed using `from elinkapi import exceptions` then reference each as
`except exceptions.BadRequestException as e:`
