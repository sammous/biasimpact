# Bias Impact 

## BiasImpacter

Back end of the BiasImpact application

### Installation

Environnement Variable needed :
````python
mongo_host = os.getenv("BIASIMPACTER_DC_MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("APP_MONGO_DB")
mongo_user = os.getenv("APP_MONGO_USER")
mongo_pw = os.getenv("APP_MONGO_PASS")
````

The `script` folder contains a `bash` script that creates a user to MongoDB.

## BiasImpacted 

Frond end of the BiasImpact application
