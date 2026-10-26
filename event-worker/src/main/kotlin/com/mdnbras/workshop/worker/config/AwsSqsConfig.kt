package com.mdnbras.workshop.worker.config

import java.net.URI
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sqs.SqsClient

@Configuration
class AwsSqsConfig {
    @Bean
    fun sqsClient(): SqsClient {
        val endpoint = System.getenv("AWS_ENDPOINT_URL")?.takeIf { it.isNotBlank() }
        val region = System.getenv().getOrDefault("AWS_REGION", "us-east-1")

        val builder = SqsClient.builder()
            .region(Region.of(region))
            .credentialsProvider(DefaultCredentialsProvider.create())

        if (endpoint != null) {
            builder.endpointOverride(URI.create(endpoint))
        }

        return builder.build()
    }
}
