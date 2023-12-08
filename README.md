# Conduit Commons
 ### Kafka
  - CommonProducer
  - CommonConsumer
 ### HTTP
  - Errors
  - HTTP Responses
  - Utils
  
## Build Status
[![Continuous Integration](https://github.com/conduithealth/conduit-commons/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/conduithealth/conduit-commons/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/conduithealth/conduit-commons/branch/main/graph/badge.svg?token=6HHWNT4150)](https://codecov.io/gh/conduithealth/conduit-commons)


## Setup
  - Run `./setup.sh`
    - This will install all the required dependencies and create a virtual environment called `conduit-commons` at the user folder level
  - Activate it with `source ~/.venvs/conduit-commons/bin/activate`
  - Optionally, create an alias and add to your shell of choice: 
    - ```sh
      alias commons='source ~/.venvs/conduit-commons/bin/activate'
      ```

## Publishing to Gemfury

Run `python setup.py sdist` and upload the tarball
