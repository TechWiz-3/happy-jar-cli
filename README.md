# Happy Jar CLI
An easy to use CLI for storing good memories and gratitiude.  

```bash
# basic logging
$ happy log "Happy text here! :D"

# view logs with
$ happy get all

# or,
$ happy get today
```

## Installation
```sh
pip install happyjar
```
**Binaries:**  
Download the binary for your platform from the `Artifacts` section of the latest [GitHub Actions](https://github.com/TechWiz-3/happy-jar-cli/actions) run.

## What is it?
<img src="https://github.com/TechWiz-3/happy-jar-cli/blob/main/media/happy.jpg?raw=true" width="400px"></img>  
[Source](https://twitter.com/imovesactive/status/1274960313863950337)

## Usage

```sh
$ happy --help
usage: happy [-h] {log,get} ...

Log your good memories and gratitiude.

positional arguments:
  {log,get}
    log       logs an entry
    get       gets entries

optional arguments:
  -h, --help  show this help message and exit

examples:
happy log "i am so happy because you starred this project's repo on github xDD"
happy get all
```

## Example

<img src="https://github.com/TechWiz-3/happy-jar-cli/blob/main/media/example.png?raw=true" width="700px"></img>  

Inspired by [michelle/happy](https://github.com/michelle/happy)  

## Todo
- [ ] Add support for markdown emojis with the `:emoji:` format. Use Textualize/rich for this.  

Check [Issues](https://github.com/TechWiz-3/happy-jar-cli/issues) for more.

## Contributors

* [HitBlast](https://github.com/hitblast) the Mighty
* [Diwash Dahal](https://github.com/diwash007) the Conqueror
* [Franklin Ikeh](https://github.com/fr4nkln11) the Neat
* [Micah Wood](https://github.com/mxw7265) the Strong

---
### 🎉 Commit labels
If you're interested in the commit labels used in this repo, check out my [git commit emoji](https://github.com/TechWiz-3/git-commit-emojis) project
