package com.mdnbras.workshop.order;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import software.amazon.awssdk.services.sns.SnsClient;
import software.amazon.awssdk.services.sns.model.PublishRequest;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    private final SnsClient snsClient;
    private final ObjectMapper objectMapper;
    private final String topicArn;

    public OrderController(SnsClient snsClient, ObjectMapper objectMapper) {
        this.snsClient = snsClient;
        this.objectMapper = objectMapper;
        this.topicArn = System.getenv().getOrDefault(
                "ORDERS_TOPIC_ARN",
                "arn:aws:sns:us-east-1:000000000000:orders-topic");
    }

    @PostMapping
    ResponseEntity<OrderCreated> create(@RequestBody CreateOrderRequest request) throws JsonProcessingException {
        var event = new OrderCreated(
                UUID.randomUUID(),
                UUID.randomUUID(),
                request.customerEmail(),
                request.total(),
                Instant.now());

        var message = objectMapper.writeValueAsString(event);

        snsClient.publish(PublishRequest.builder()
                .topicArn(topicArn)
                .message(message)
                .messageAttributes(java.util.Map.of(
                        "eventType",
                        software.amazon.awssdk.services.sns.model.MessageAttributeValue.builder()
                                .dataType("String")
                                .stringValue("OrderCreated")
                                .build()))
                .build());

        log.info("event=OrderCreated eventId={} orderId={} published=true", event.eventId(), event.orderId());
        return ResponseEntity.accepted().body(event);
    }

    public record CreateOrderRequest(String customerEmail, BigDecimal total) {}

    public record OrderCreated(
            UUID eventId,
            UUID orderId,
            String customerEmail,
            BigDecimal total,
            Instant occurredAt) {}
}
