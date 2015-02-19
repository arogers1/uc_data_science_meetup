## Set up Database

* Load in the .sql file ```mysql -u username -p scriptures < scriptures.sql```

* Add the polarity column to the database files  ```mysql -u username -p scriptures < add_polarity_column.sql```

## Set up Sentiment Analysis Dictionary

* Go and grab the AFINN-111.txt file ```wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip```

* Unzip the file download  ```unzip imm6010.zip```

## Set up Flask

* Make sure python 2.7.+ is installed ```python -V```

* Make sure pip is installed  ```sudo easy_install pip```

* Set up virtualenvwrapper  ``` pip install virtualenvwrapper```

* Create an environment ```mkvirtualenv scripture_env```

* Install python dependencies ```pip install Flask, mysql-python, flask-sqlalchemy``` or ```pip install -r /path/to/requirements.txt```

* Run the app ```python runserver.py```


## Exploration Questions

* What are the most positive / negative verses in scripture?

* What are the weaknesses of this type of analysis?

* What is the most positive / negative book?

* Who writes the smallest verses in the scripture?

* What book has the most word diversity?
