package com.mdnbras.workshop.worker.config

import java.net.URI
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sqs.SqsClient

@Configuration
class AwsSqsConfig {
    @Bean
    fun sqsClient(): SqsClient {
        val endpoint = System.getenv().getOrDefault("AWS_ENDPOINT_URL", "http://localhost:4566")
        val region = System.getenv().getOrDefault("AWS_REGION", "us-east-1")

        return SqsClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.of(region))
            .credentialsProvider(
                StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test"))
            )
            .build()
    }
}
