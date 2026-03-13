# Dependency Matrix

## Maven

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>rest-assured-bom</artifactId>
      <version>${restassured.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

## Common Test Dependencies

| Need | Dependency |
|---|---|
| Core HTTP testing | `io.rest-assured:rest-assured` |
| JSON schema validation | `io.rest-assured:json-schema-validator` |
| JUnit 5 | `org.junit.jupiter:junit-jupiter` |
| Containerized integration tests | `org.testcontainers:junit-jupiter` |
| HTTP service stubbing | `org.wiremock:wiremock` |

## Gradle

```kotlin
dependencies {
    testImplementation(platform("io.rest-assured:rest-assured-bom:$restAssuredVersion"))
    testImplementation("io.rest-assured:rest-assured")
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```
