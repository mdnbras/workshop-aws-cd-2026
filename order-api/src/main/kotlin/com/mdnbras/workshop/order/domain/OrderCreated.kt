package com.mdnbras.workshop.order.domain

import java.math.BigDecimal
import java.time.Instant
import java.util.UUID

data class OrderCreated(
    val eventId: UUID,
    val orderId: UUID,
    val customerEmail: String,
    val total: BigDecimal,
    val occurredAt: Instant
)
