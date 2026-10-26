package com.mdnbras.workshop.order.config

import java.net.URI
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sns.SnsClient

@Configuration
class AwsSnsConfig {
    @Bean
    fun snsClient(): SnsClient {
        val endpoint = System.getenv("AWS_ENDPOINT_URL")?.takeIf { it.isNotBlank() }
        val region = System.getenv().getOrDefault("AWS_REGION", "us-east-1")

        val builder = SnsClient.builder()
            .region(Region.of(region))
            .credentialsProvider(DefaultCredentialsProvider.create())

        if (endpoint != null) {
            builder.endpointOverride(URI.create(endpoint))
        }

        return builder.build()
    }
}
