FROM maven:3.9.11-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY pom.xml ./pom.xml
COPY order-api/pom.xml ./order-api/pom.xml
COPY event-worker/pom.xml ./event-worker/pom.xml
RUN mvn -q -pl order-api -am dependency:go-offline
COPY order-api/src ./order-api/src
RUN mvn -q -pl order-api -am package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /workspace/order-api/target/order-api-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
