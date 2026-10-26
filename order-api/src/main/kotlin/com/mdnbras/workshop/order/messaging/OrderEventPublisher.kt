package com.mdnbras.workshop.order.messaging

import com.mdnbras.workshop.order.domain.OrderCreated

fun interface OrderEventPublisher {
    fun publish(event: OrderCreated)
}
