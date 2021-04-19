# Event Driven Pipeline Engine
EventML is a modular software to perform Event Driven Machine Learning. It provides the building blocks and engines allowing the user to ensemble pipelines and run them conviniently. 

# Run locally
To run EventML you will need to install dependecies from the requirements.txt file. You can do so by directly installing them onto your system path or creating a virtual environment. 

```
pip3 install -r requirements.txt
```

# Use Case
We provide with a use case to predict Microsoft Stock Prices with structured event embbedings using Open Information Extraction. You can run this by running the `main.py` file as

```
python3 main.py
```

# Dependencies
* pandas and numpy: To handle data frames operations
* OpenIE : Open IE to extract structured events from text
* snscrape : To scrape information from the web


# File structure
```
+-- src
|   +-- pipes
|   |   +-- crawler.py 
|   |   +-- encoders.py
|   |   +-- ml.py
|   |   +-- openie.py
|   |   +-- pipe.py
|   |   +-- preprocessing.py
|   |   +-- sentiment.py
|   |   +-- utils.py
|   |   +-- visualization.py
|   +-- colors.py
|   +-- engine.py
+-- README.md
+-- main.py
+-- requirements.txt
```

