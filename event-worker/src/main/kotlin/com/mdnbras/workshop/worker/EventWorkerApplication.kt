package com.mdnbras.workshop.worker

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class EventWorkerApplication

fun main(args: Array<String>) {
    runApplication<EventWorkerApplication>(*args)
}
