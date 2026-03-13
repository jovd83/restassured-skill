#!/usr/bin/env python3
"""Initialize a Rest Assured test module for Maven or Gradle."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


POM_TEMPLATE = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <properties>
    <maven.compiler.source>{java_version}</maven.compiler.source>
    <maven.compiler.target>{java_version}</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <restassured.version>{restassured_version}</restassured.version>
    <junit.version>5.13.4</junit.version>
  </properties>
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured-bom</artifactId>
        <version>${{restassured.version}}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>rest-assured</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>json-schema-validator</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${{junit.version}}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.4</version>
        <configuration>
          <useModulePath>false</useModulePath>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""

GRADLE_TEMPLATE = """plugins {{
    java
}}

repositories {{
    mavenCentral()
}}

val restAssuredVersion = "{restassured_version}"

java {{
    toolchain {{
        languageVersion.set(JavaLanguageVersion.of({java_version}))
    }}
}}

dependencies {{
    testImplementation(platform("io.rest-assured:rest-assured-bom:$restAssuredVersion"))
    testImplementation("io.rest-assured:rest-assured")
    testImplementation("io.rest-assured:json-schema-validator")
    testImplementation("org.junit.jupiter:junit-jupiter:5.13.4")
}}

tasks.test {{
    useJUnitPlatform()
}}
"""

SPECIFICATIONS_TEMPLATE = """package {package_name}.support;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.builder.ResponseSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public final class Specifications {{
    private Specifications() {{
    }}

    public static RequestSpecification requestSpec() {{
        return new RequestSpecBuilder()
                .setBaseUri(resolveBaseUrl())
                .setContentType(ContentType.JSON)
                .build();
    }}

    public static ResponseSpecification jsonOk() {{
        return new ResponseSpecBuilder()
                .expectStatusCode(200)
                .expectContentType(ContentType.JSON)
                .build();
    }}

    private static String resolveBaseUrl() {{
        String systemValue = System.getProperty("baseUrl");
        if (systemValue != null && !systemValue.isBlank()) {{
            return systemValue;
        }}

        String envValue = System.getenv("BASE_URL");
        if (envValue != null && !envValue.isBlank()) {{
            return envValue;
        }}

        Properties properties = new Properties();
        try (InputStream stream = Specifications.class.getClassLoader().getResourceAsStream("test.properties")) {{
            if (stream != null) {{
                properties.load(stream);
                String fileValue = properties.getProperty("baseUrl");
                if (fileValue != null && !fileValue.isBlank()) {{
                    return fileValue;
                }}
            }}
        }} catch (IOException ignored) {{
        }}

        return "http://localhost:8080";
    }}
}}
"""

SMOKE_TEST_TEMPLATE = """package {package_name}.tests;

import static io.restassured.RestAssured.given;

import {package_name}.support.Specifications;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class {class_name} {{

    @Test
    @Tag("smoke")
    void {method_name}() {{
        given()
                .spec(Specifications.requestSpec())
        .when()
                .get("{smoke_path}")
        .then()
                .spec(Specifications.jsonOk());
    }}
}}
"""

TEST_PROPERTIES_TEMPLATE = """# Override with -DbaseUrl or BASE_URL
baseUrl=http://localhost:8080
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a Rest Assured module.")
    parser.add_argument("--path", required=True, help="Target module path.")
    parser.add_argument("--build", required=True, choices=["maven", "gradle"], help="Build tool.")
    parser.add_argument("--package", required=True, dest="package_name", help="Java package name.")
    parser.add_argument("--java-version", default="17", help="Java version.")
    parser.add_argument("--restassured-version", default=None, help="Rest Assured version override.")
    parser.add_argument("--smoke-path", default="/health", help="Stable endpoint used by the generated smoke test.")
    parser.add_argument("--smoke-class-name", default=None, help="Optional override for the generated smoke test class name.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files.")
    return parser


def choose_restassured_version(java_version: str, override: str | None) -> str:
    if override:
        return override
    try:
        major = int(java_version)
    except ValueError:
        major = 17
    return "6.0.0" if major >= 17 else "5.5.7"


def split_smoke_tokens(smoke_path: str) -> list[str]:
    cleaned = smoke_path.strip().split("?", 1)[0]
    parts = []
    for segment in cleaned.strip("/").split("/"):
        parts.extend(token for token in re.split(r"[^A-Za-z0-9]+", segment) if token)
    tokens = []
    for token in parts:
        lower = token.lower()
        if lower in {"api", "internal"} or re.fullmatch(r"v\d+", lower):
            continue
        tokens.append(token)
    return tokens


def pascal_case(token: str) -> str:
    pieces = re.findall(r"[A-Za-z0-9]+", token)
    return "".join(piece[:1].upper() + piece[1:] for piece in pieces if piece)


def lower_camel(tokens: list[str]) -> str:
    if not tokens:
        return ""
    first = tokens[0][:1].lower() + tokens[0][1:]
    return first + "".join(token[:1].upper() + token[1:] for token in tokens[1:])


def derive_smoke_class_name(smoke_path: str, override: str | None) -> str:
    if override:
        return override
    normalized = smoke_path.strip().split("?", 1)[0].rstrip("/") or "/"
    if normalized in {"/health", "/actuator/health", "/status", "/ping"}:
        return "HealthCheckTest"
    tokens = split_smoke_tokens(normalized)
    pascal_tokens = [pascal_case(token) for token in tokens if pascal_case(token)]
    if not pascal_tokens:
        return "SmokeTest"
    return "".join(pascal_tokens[:4]) + "SmokeTest"


def derive_smoke_method_name(smoke_path: str) -> str:
    normalized = smoke_path.strip().split("?", 1)[0].rstrip("/") or "/"
    if normalized in {"/health", "/actuator/health", "/status", "/ping"}:
        return "healthEndpointReturnsJsonOk"
    tokens = split_smoke_tokens(normalized)
    pascal_tokens = [pascal_case(token) for token in tokens if pascal_case(token)]
    if not pascal_tokens:
        return "smokeEndpointReturnsJsonOk"
    return lower_camel(pascal_tokens[:4]) + "EndpointReturnsJsonOk"


def write_file(path: Path, contents: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    module_path = Path(args.path)
    package_path = Path(*args.package_name.split("."))
    restassured_version = choose_restassured_version(args.java_version, args.restassured_version)
    smoke_class_name = derive_smoke_class_name(args.smoke_path, args.smoke_class_name)
    smoke_method_name = derive_smoke_method_name(args.smoke_path)

    if args.build == "maven":
        build_file = module_path / "pom.xml"
        build_contents = POM_TEMPLATE.format(
            group_id="example",
            artifact_id=module_path.name or "api-tests",
            java_version=args.java_version,
            restassured_version=restassured_version,
        )
    else:
        build_file = module_path / "build.gradle.kts"
        build_contents = GRADLE_TEMPLATE.format(
            java_version=args.java_version,
            restassured_version=restassured_version,
        )

    write_file(build_file, build_contents, args.force)
    write_file(
        module_path / "src" / "test" / "java" / package_path / "support" / "Specifications.java",
        SPECIFICATIONS_TEMPLATE.format(package_name=args.package_name),
        args.force,
    )
    write_file(
        module_path / "src" / "test" / "java" / package_path / "tests" / f"{smoke_class_name}.java",
        SMOKE_TEST_TEMPLATE.format(
            package_name=args.package_name,
            smoke_path=args.smoke_path,
            class_name=smoke_class_name,
            method_name=smoke_method_name,
        ),
        args.force,
    )
    write_file(
        module_path / "src" / "test" / "resources" / "test.properties",
        TEST_PROPERTIES_TEMPLATE,
        args.force,
    )
    print((module_path / "src" / "test" / "java" / package_path / "tests" / f"{smoke_class_name}.java").resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
