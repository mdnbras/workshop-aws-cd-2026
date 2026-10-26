package com.mdnbras.workshop.worker.model

import java.math.BigDecimal
import java.time.Instant
import java.util.UUID

data class OrderCreatedEvent(
    val eventId: UUID,
    val orderId: UUID,
    val customerEmail: String,
    val total: BigDecimal,
    val occurredAt: Instant
)
