# NoSQL

Instructions for MongoDB

## Install Homebrew

```ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```

## Install MongoDB


```brew update```

```brew install mongodb```

## Run MongoDB server

```mongod```

## import zips.json (zip code database)

```mongoimport --db scratch --collection zips --file zips.json```


