package com.mdnbras.workshop.worker;

import java.net.URI;
import java.time.Duration;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.DeleteMessageRequest;
import software.amazon.awssdk.services.sqs.model.ReceiveMessageRequest;

@SpringBootApplication
public class EventWorkerApplication {

    private static final Logger log = LoggerFactory.getLogger(EventWorkerApplication.class);

    public static void main(String[] args) {
        SpringApplication.run(EventWorkerApplication.class, args);
    }

    @Bean
    SqsClient sqsClient() {
        var endpoint = System.getenv().getOrDefault("AWS_ENDPOINT_URL", "http://localhost:4566");
        var region = System.getenv().getOrDefault("AWS_REGION", "us-east-1");

        return SqsClient.builder()
                .endpointOverride(URI.create(endpoint))
                .region(Region.of(region))
                .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test")))
                .build();
    }

    @Bean
    CommandLineRunner consume(SqsClient sqsClient, ObjectMapper objectMapper) {
        return args -> {
            var workerName = System.getenv().getOrDefault("WORKER_NAME", "worker");
            var queueUrl = requireEnv("QUEUE_URL");

            log.info("worker={} status=started queue={}", workerName, queueUrl);

            while (!Thread.currentThread().isInterrupted()) {
                var response = sqsClient.receiveMessage(ReceiveMessageRequest.builder()
                        .queueUrl(queueUrl)
                        .maxNumberOfMessages(5)
                        .waitTimeSeconds(2)
                        .build());

                for (var message : response.messages()) {
                    try {
                        var event = objectMapper.readTree(message.body());
                        process(workerName, event);

                        sqsClient.deleteMessage(DeleteMessageRequest.builder()
                                .queueUrl(queueUrl)
                                .receiptHandle(message.receiptHandle())
                                .build());

                        log.info("worker={} eventId={} status=processed", workerName, text(event, "eventId"));
                    } catch (Exception exception) {
                        // Não removemos a mensagem. Depois do Visibility Timeout ela volta para a fila.
                        // Após maxReceiveCount, o SQS a envia para a DLQ.
                        log.error("worker={} status=failed reason={}", workerName, exception.getMessage());
                    }
                }
            }
        };
    }

    private static void process(String workerName, JsonNode event) throws InterruptedException {
        var orderId = text(event, "orderId");
        var email = text(event, "customerEmail");
        var total = event.path("total").asText();

        if ("notification".equals(workerName)) {
            if ("fail@workshop.local".equalsIgnoreCase(email)) {
                throw new IllegalStateException("simulated notification failure");
            }
            log.info("worker=notification action=send-email orderId={} to={}", orderId, email);
        } else if ("analytics".equals(workerName)) {
            log.info("worker=analytics action=record-metric orderId={} total={}", orderId, total);
        } else {
            log.info("worker={} action=consume orderId={}", workerName, orderId);
        }

        // Pequena pausa apenas para o fluxo ficar visível nos logs durante o workshop.
        Thread.sleep(Duration.ofMillis(250));
    }

    private static String text(JsonNode node, String field) {
        return node.path(field).asText("unknown");
    }

    private static String requireEnv(String key) {
        var value = System.getenv(key);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Environment variable " + key + " is required");
        }
        return value;
    }
}
