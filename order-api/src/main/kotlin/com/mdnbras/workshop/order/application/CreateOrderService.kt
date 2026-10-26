package com.mdnbras.workshop.order.application

import com.mdnbras.workshop.order.api.CreateOrderRequest
import com.mdnbras.workshop.order.domain.OrderCreated
import com.mdnbras.workshop.order.messaging.OrderEventPublisher
import java.time.Instant
import java.util.UUID
import org.springframework.stereotype.Service

@Service
class CreateOrderService(
    private val eventPublisher: OrderEventPublisher
) {
    fun create(request: CreateOrderRequest): OrderCreated {
        val event = OrderCreated(
            eventId = UUID.randomUUID(),
            orderId = UUID.randomUUID(),
            customerEmail = request.customerEmail,
            total = request.total,
            occurredAt = Instant.now()
        )

        eventPublisher.publish(event)
        return event
    }
}
