package com.mdnbras.workshop.order.api

import com.mdnbras.workshop.order.application.CreateOrderService
import com.mdnbras.workshop.order.domain.OrderCreated
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/orders")
class OrderController(
    private val createOrderService: CreateOrderService
) {
    @PostMapping
    fun create(@RequestBody request: CreateOrderRequest): ResponseEntity<OrderCreated> =
        ResponseEntity.accepted().body(createOrderService.create(request))
}
