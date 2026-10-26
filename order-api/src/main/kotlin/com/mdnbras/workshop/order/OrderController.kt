package com.mdnbras.workshop.order

import com.fasterxml.jackson.databind.ObjectMapper
import java.math.BigDecimal
import java.time.Instant
import java.util.UUID
import org.slf4j.LoggerFactory
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import software.amazon.awssdk.services.sns.SnsClient
import software.amazon.awssdk.services.sns.model.MessageAttributeValue
import software.amazon.awssdk.services.sns.model.PublishRequest

@RestController
@RequestMapping("/orders")
class OrderController(
    private val snsClient: SnsClient,
    private val objectMapper: ObjectMapper
) {
    private val log = LoggerFactory.getLogger(javaClass)

    private val topicArn = System.getenv().getOrDefault(
        "ORDERS_TOPIC_ARN",
        "arn:aws:sns:us-east-1:000000000000:orders-topic"
    )

    @PostMapping
    fun create(@RequestBody request: CreateOrderRequest): ResponseEntity<OrderCreated> {
        val event = OrderCreated(
            eventId = UUID.randomUUID(),
            orderId = UUID.randomUUID(),
            customerEmail = request.customerEmail,
            total = request.total,
            occurredAt = Instant.now()
        )

        val message = objectMapper.writeValueAsString(event)

        snsClient.publish(
            PublishRequest.builder()
                .topicArn(topicArn)
                .message(message)
                .messageAttributes(
                    mapOf(
                        "eventType" to MessageAttributeValue.builder()
                            .dataType("String")
                            .stringValue("OrderCreated")
                            .build()
                    )
                )
                .build()
        )

        log.info(
            "event=OrderCreated eventId={} orderId={} published=true",
            event.eventId,
            event.orderId
        )

        return ResponseEntity.accepted().body(event)
    }
}

data class CreateOrderRequest(
    val customerEmail: String,
    val total: BigDecimal
)

data class OrderCreated(
    val eventId: UUID,
    val orderId: UUID,
    val customerEmail: String,
    val total: BigDecimal,
    val occurredAt: Instant
)
