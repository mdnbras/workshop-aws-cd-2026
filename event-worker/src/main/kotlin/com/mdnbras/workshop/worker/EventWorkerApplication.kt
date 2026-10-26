package com.mdnbras.workshop.worker

import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.ObjectMapper
import java.net.URI
import org.slf4j.LoggerFactory
import org.springframework.boot.CommandLineRunner
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sqs.SqsClient
import software.amazon.awssdk.services.sqs.model.DeleteMessageRequest
import software.amazon.awssdk.services.sqs.model.ReceiveMessageRequest

@SpringBootApplication
class EventWorkerApplication {

    @Bean
    fun sqsClient(): SqsClient {
        val endpoint = System.getenv().getOrDefault("AWS_ENDPOINT_URL", "http://localhost:4566")
        val region = System.getenv().getOrDefault("AWS_REGION", "us-east-1")

        return SqsClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.of(region))
            .credentialsProvider(
                StaticCredentialsProvider.create(
                    AwsBasicCredentials.create("test", "test")
                )
            )
            .build()
    }

    @Bean
    fun consume(sqsClient: SqsClient, objectMapper: ObjectMapper) = CommandLineRunner {
        val workerName = System.getenv().getOrDefault("WORKER_NAME", "worker")
        val queueUrl = requireEnv("QUEUE_URL")

        log.info("worker={} status=started queue={}", workerName, queueUrl)

        while (!Thread.currentThread().isInterrupted) {
            val response = sqsClient.receiveMessage(
                ReceiveMessageRequest.builder()
                    .queueUrl(queueUrl)
                    .maxNumberOfMessages(5)
                    .waitTimeSeconds(2)
                    .build()
            )

            response.messages().forEach { message ->
                try {
                    val event = objectMapper.readTree(message.body())
                    process(workerName, event)

                    sqsClient.deleteMessage(
                        DeleteMessageRequest.builder()
                            .queueUrl(queueUrl)
                            .receiptHandle(message.receiptHandle())
                            .build()
                    )

                    log.info(
                        "worker={} eventId={} status=processed",
                        workerName,
                        text(event, "eventId")
                    )
                } catch (exception: Exception) {
                    // A mensagem não é removida. Depois do Visibility Timeout ela volta para a fila.
                    // Após maxReceiveCount, o SQS a envia para a DLQ.
                    log.error(
                        "worker={} status=failed reason={}",
                        workerName,
                        exception.message
                    )
                }
            }
        }
    }

    companion object {
        private val log = LoggerFactory.getLogger(EventWorkerApplication::class.java)

        private fun process(workerName: String, event: JsonNode) {
            val orderId = text(event, "orderId")
            val email = text(event, "customerEmail")
            val total = event.path("total").asText()

            when (workerName) {
                "notification" -> {
                    if (email.equals("fail@workshop.local", ignoreCase = true)) {
                        error("simulated notification failure")
                    }
                    log.info(
                        "worker=notification action=send-email orderId={} to={}",
                        orderId,
                        email
                    )
                }

                "analytics" -> log.info(
                    "worker=analytics action=record-metric orderId={} total={}",
                    orderId,
                    total
                )

                else -> log.info(
                    "worker={} action=consume orderId={}",
                    workerName,
                    orderId
                )
            }

            // Pequena pausa apenas para o fluxo ficar visível nos logs durante o workshop.
            Thread.sleep(250)
        }

        private fun text(node: JsonNode, field: String): String =
            node.path(field).asText("unknown")

        private fun requireEnv(key: String): String =
            System.getenv(key)?.takeIf { it.isNotBlank() }
                ?: error("Environment variable $key is required")
    }
}

fun main(args: Array<String>) {
    runApplication<EventWorkerApplication>(*args)
}
