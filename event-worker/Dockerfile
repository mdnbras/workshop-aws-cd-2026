FROM maven:3.9.11-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY pom.xml ./pom.xml
COPY order-api/pom.xml ./order-api/pom.xml
COPY event-worker/pom.xml ./event-worker/pom.xml
RUN mvn -q -pl event-worker -am dependency:go-offline
COPY event-worker/src ./event-worker/src
RUN mvn -q -pl event-worker -am package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /workspace/event-worker/target/event-worker-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
