package com.mdnbras.workshop.worker.consumer

import com.fasterxml.jackson.databind.ObjectMapper
import com.mdnbras.workshop.worker.handler.OrderCreatedHandler
import com.mdnbras.workshop.worker.model.OrderCreatedEvent
import org.slf4j.LoggerFactory
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component
import software.amazon.awssdk.services.sqs.SqsClient
import software.amazon.awssdk.services.sqs.model.DeleteMessageRequest
import software.amazon.awssdk.services.sqs.model.ReceiveMessageRequest

@Component
class SqsOrderEventConsumer(
    private val sqsClient: SqsClient,
    private val objectMapper: ObjectMapper,
    private val handler: OrderCreatedHandler
) : CommandLineRunner {

    private val log = LoggerFactory.getLogger(javaClass)

    override fun run(vararg args: String?) {
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
                    val event = objectMapper.readValue(message.body(), OrderCreatedEvent::class.java)
                    handler.handle(workerName, event)

                    sqsClient.deleteMessage(
                        DeleteMessageRequest.builder()
                            .queueUrl(queueUrl)
                            .receiptHandle(message.receiptHandle())
                            .build()
                    )

                    log.info(
                        "worker={} eventId={} status=processed",
                        workerName,
                        event.eventId
                    )
                } catch (exception: Exception) {
                    log.error(
                        "worker={} status=failed reason={}",
                        workerName,
                        exception.message
                    )
                }
            }
        }
    }

    private fun requireEnv(key: String): String =
        System.getenv(key)?.takeIf { it.isNotBlank() }
            ?: error("Environment variable $key is required")
}
