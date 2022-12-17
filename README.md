# mogrilla
A modular chat bot, nothing special here

It is designed to be modular, even if only discord is supported now (but should be easily movable to other chat apps), with a command system similar of what you would find on IRC, the whole bot is designed to have a similar "feeling" to a IRC bot

## Warn
This is still a WIP project, and was only designed for a specific, "semi-private" server, so don't expect  the ease of use of a widespread bot!

## Config file format:
```yaml
skills:
  hello:
  maker:
  quake:
    server: 'localhost:27960'
    chan: 'games'

messaging:
  discord:
    token: 'secret'
```

## Making skills
(for now, this will change)
* Create your skill as skills/myskill.py (see hello.py)
* Add your skills in your config file
* ???
* Profit
