package com.mdnbras.workshop.order.messaging

import com.fasterxml.jackson.databind.ObjectMapper
import com.mdnbras.workshop.order.domain.OrderCreated
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import software.amazon.awssdk.services.sns.SnsClient
import software.amazon.awssdk.services.sns.model.MessageAttributeValue
import software.amazon.awssdk.services.sns.model.PublishRequest

@Component
class SnsOrderEventPublisher(
    private val snsClient: SnsClient,
    private val objectMapper: ObjectMapper
) : OrderEventPublisher {

    private val log = LoggerFactory.getLogger(javaClass)
    private val topicArn = System.getenv().getOrDefault(
        "ORDERS_TOPIC_ARN",
        "arn:aws:sns:us-east-1:000000000000:orders-topic"
    )

    override fun publish(event: OrderCreated) {
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
    }
}
