package com.mdnbras.workshop.order

import java.net.URI
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sns.SnsClient

@SpringBootApplication
class OrderApiApplication {

    @Bean
    fun snsClient(): SnsClient {
        val endpoint = System.getenv().getOrDefault("AWS_ENDPOINT_URL", "http://localhost:4566")
        val region = System.getenv().getOrDefault("AWS_REGION", "us-east-1")

        return SnsClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.of(region))
            .credentialsProvider(
                StaticCredentialsProvider.create(
                    AwsBasicCredentials.create("test", "test")
                )
            )
            .build()
    }
}

fun main(args: Array<String>) {
    runApplication<OrderApiApplication>(*args)
}
