## Development Instructions Test

### Publishing Package to test.pypi.org
1. Install the needed dependencies for packaging and publishing distribution archives: `pip install ostiapi[development]`
2. Make your desired changes within the project
3. Update the version number within the `pyproject.toml` file
4. Execute `python3 -m build`: this will generate 2 distribution archives that will be uploaded to pypi
5. Execute `twine upload --repository testpypi dist/*`: this will publish your packages to the test pypi index

### Importing the Package from test.pypi.org
1. Install the package, but don't grab the dependencies (pip will attempt to grab everything from the test server, which we do not want): `pip install --index-url https://test.pypi.org/simple/ --no-deps ostiapi`
2. Now install the other dependencies: `pip install --index-url https://test.pypi.org/simple/ ostiapi`
a. Or install them separately: `pip install requests pydantic urllib3==1.26.6`
3. `import ostiapi` will allow you to access the entire API functionality using dot notation. E.g. `ostiapi.set_api_token("Your_API_Token")`
4. The pydantic classes can be fetched using `from ostiapi import Record`

## Development Instructions Prod

### Publishing to Prod
1. Install the needed dependencies for packaging and publishing distribution archives `pip install ostiapi`
2. Make your desired changes within the project
3. Update the version number within the `pyproject.toml` file
4. Execute `python3 -m build`: this will generate 2 distribution archives that will be uploaded to pypi
5. Execute `twine upload dist/*`: this will publish your packages to the test pypi index

### Importing the Package from Prod
1. Install the package: `pip install ostiapi`
2. `import ostiapi` will allow you to access the entire API functionality using dot notation. E.g. `ostiapi.set_api_token("Your_API_Token")`
3. The pydantic classes can be fetched using `from ostiapi import Record`