# Domotz� Public API example client in Java
  
  
This project builds a simple client in Java that shows some examples on how to write code to interact with tie Domotz API.


## Build

## Requirements

 - Java 7 or newer
 - Maven 3.5.4 or newer
 - A valid Domotz API key

 
## Building and running the example

 
```bash
# From the directory where this file is
curl https://api-eu-west-1-cell-1.domotz.com/public-api/v1/meta/open-api-definition > src/main/resources/api.json
mvn package
java -jar target/example-client-1.0-SNAPSHOT-jar-with-dependencies.jar -k [your API key] -c [your cell] agents
# lists all the agents
java -jar target/example-client-1.0-SNAPSHOT-jar-with-dependencies.jar -k [your API key] -c [your cell] device -a 1234 -d 456
# shows the device details

``` 
 
 
  