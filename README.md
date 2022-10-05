# mentor-api
API created to manage requests and responses about information from mentors in Hunty


To have project stats in sonarqube local server, you need:
To install sonarqube server and sonarqube scanner into your local machine.
To install docker to aim the image for the project and the docker hub image to sonarqube server and scanner.
And to run the server and scanner you need to used those commands:

docker run -d --name sonarqube \
    --network=bridge \
    -p 9000:9000 \
    -v sonarqube_data:/opt/sonarqube/data \
    -v sonarqube_extensions:/opt/sonarqube/extensions \
    -v sonarqube_logs:/opt/sonarqube/logs \
    sonarqube:community

docker run --network=host -e SONAR_HOST_URL='http://127.0.0.1:9000' -e SONAR_LOGIN="5c2d39616fd18de568210e827c130560117222de" -e PROJECT_KEY="template-backend-api" --user="$(id -u):$(id -g)" -v "$PWD:/usr/src" sonarsource/sonar-scanner-cli sonar-scanner \
  -Dsonar.projectKey=template-backend-api \
   -Dsonar.sources=. \
   -Dsonar.host.url=http://localhost:9000 \
   -Dsonar.login=5c2d39616fd18de568210e827c130560117222de \
   -Dsonar.language=py \
   -Dsonar.sourceEncoding=UTF-8 \
   -Dsonar.dynamicAnalysis=reuseReports \
   -Dsonar.core.codeCoveragePlugin=cobertura \
   -Dsonar.python.coverage.reportPaths=coverage.xml


And to run the images you need to mount it:
docker build -t myimage .

And to run it
docker run -d --name mycontainer -p 80:80 myimage

