package com.mdnbras.workshop.worker.handler

import com.mdnbras.workshop.worker.model.OrderCreatedEvent
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class OrderCreatedHandler {
    private val log = LoggerFactory.getLogger(javaClass)

    fun handle(workerName: String, event: OrderCreatedEvent) {
        when (workerName) {
            "notification" -> handleNotification(event)
            "analytics" -> handleAnalytics(event)
            else -> log.info("worker={} action=consume orderId={}", workerName, event.orderId)
        }

        Thread.sleep(250)
    }

    private fun handleNotification(event: OrderCreatedEvent) {
        if (event.customerEmail.equals("fail@workshop.local", ignoreCase = true)) {
            error("simulated notification failure")
        }

        log.info(
            "worker=notification action=send-email orderId={} to={}",
            event.orderId,
            event.customerEmail
        )
    }

    private fun handleAnalytics(event: OrderCreatedEvent) {
        log.info(
            "worker=analytics action=record-metric orderId={} total={}",
            event.orderId,
            event.total
        )
    }
}
