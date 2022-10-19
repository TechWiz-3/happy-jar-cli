# Contribution Guidelines

First of all, thank you so much for taking a deeper look at the project. It does mean a lot.  

PRs and issues of all sorts are welcome, here are some guides to help you out.  

When contributing to this repository, preferably first discuess the changes you wish to implement via [GitHub Issues](https://github.com/TechWiz-3/happy-jar-cli/issues) page.

If you're unure you to help, check out the `Todo` section of the project's README.md.  

Following the commit messages specified in [emoji-log](https://github.com/ahmadawais/Emoji-Log) is greatly appreciated (however not mandatory). You can use my [CLI tool](https://github.com/TechWiz-3/git-commit-emojis/) for commits if that's easier.  

All changes added must pass the CI tests (TBA) provided by the GitHub Actions workflows. If not, further changes must be done in order to make up for a valid pull request / merge request. If you need help because a test isn't passing, please open an issue :+1:

When making the pull request, please ensure you tick `Allow edits by maintainers`. More info [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork)  

We also have a [Code of Conduct](./CODE_OF_CONDUCT.md) in place so please make sure to follow the given set of guidelines and thresholds while you interact with the project!  

Contributors will receive recognition for their contributions to mankind (I mean this project) in the `Contributors` section of the `README.md`. You will also receive a nice title to describle your abilities and might open-source prowess.

# Development Info
1. Clone the repo and cd into it
2. Ensure `poetry` is installed - `pip install poetry`
3. Run `poetry install`
4. Make whatever changes you need
5. To text changes run (in project root directory) `poetry run happy`
