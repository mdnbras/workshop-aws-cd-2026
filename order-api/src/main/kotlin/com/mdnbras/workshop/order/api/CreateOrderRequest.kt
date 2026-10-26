package com.mdnbras.workshop.order.api

import java.math.BigDecimal

data class CreateOrderRequest(
    val customerEmail: String,
    val total: BigDecimal
)
