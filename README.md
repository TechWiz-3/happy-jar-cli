# Happy Jar CLI

An easy to use CLI for storing good memories and gratitiude.  

The happy jar is stored as a txt file in your home dir.  

Write to it with `happy log "happy text here :)"`  
View logs with `happy get all` or `happy get today`  

```sh
$ ./happy -h
usage: happy [-h] [--bruh] {log,get} ...

Log your good memories and gratitiude.

positional arguments:
  {log,get}
    log       logs an entry
    get       gets entries

optional arguments:
  -h, --help  show this help message and exit
  --bruh      bruh

examples:
happy log "i am so happy because you starred this project's repo on github xDD"
happy get all
```

Inspired by [michelle/happy](https://github.com/michelle/happy)  

---
### 🎉 Commit labels
If you're interested in the commit labels used in this repo, check out my [git commit emoji](https://github.com/TechWiz-3/git-commit-emojis) project
