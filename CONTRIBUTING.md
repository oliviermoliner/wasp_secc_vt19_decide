# Contributing guidelines

## Setting up the development environment

1. Fork the repo on Github

2. Clone your fork locally:

   ```sh
   git clone https://github.com/whatsyourname/wasp_secc_vt19_decide.git
   ```

3.  Use the following command to install the package along with its development requirements (it is highly recommended to use a virtualenv):

   ```sh
   # After activating your virtualenv
   pip install -e .["dev"]
   ```

4. (Optionally, but recommended) Install the pre-commit hooks, which will check and reformat staged files before commit:

   ```sh
   pre-commit install
   ```



## Testing

The package uses the ```pytest``` testing framework. To run all tests:

```sh
pytest
```



## Git branch structure

The following branches are used:

``master``
    The release branch, containing stable code.

``dev``

​    Current development branch. New development should branch off here. Only pull requests against this branch will be accepted

Always make a new branch for your work!

## Commit guidelines

- Do not put unrelated changes in the same pull request
- All commits ***shall*** be atomic
- Commits for new features or bugfixes ***may*** also contain passing test cases for the new feature/fix
- Pull requests for new features or bugfixes ***shall*** contain passing test cases for the new feature/fix
- Pull requests containing ***new failing test cases for existing functionality*** are welcome
- If a pull request adds functionality, the docs should be updated
- Commits messages should start with one of the following tags:
  - ```feature:``` for new functionality
  - ```fix:``` for bugfixes
  - ```test:``` if the commit (only) adds new test cases
  - ```refactor:``` for refactoring. No new functionality should be added, and existing test cases should pass.
  - ```doc:``` when updating the documentation
  - ```chore:``` when e.g. updating dependencies or updating the build process
- Multiline commit messages are encouraged!


