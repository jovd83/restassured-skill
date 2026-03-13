#!/usr/bin/env python3
"""Extract a compact JSON summary from an OpenAPI or Swagger file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


def load_document(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise SystemExit("PyYAML is required for YAML OpenAPI files. Install it or convert the file to JSON.") from exc
    return yaml.safe_load(text)


def load_source(source: str) -> dict:
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"}:
        with urlopen(source, timeout=30) as response:  # nosec - caller supplies the source explicitly
            text = response.read().decode("utf-8")
        if parsed.path.lower().endswith(".json"):
            return json.loads(text)
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise SystemExit("PyYAML is required for YAML OpenAPI sources. Install it or use JSON.") from exc
        return yaml.safe_load(text)
    return load_document(Path(source))


def resolve_ref(document: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        return {"ref": ref}
    node: object = document
    for token in ref[2:].split("/"):
        if not isinstance(node, dict):
            return {"ref": ref}
        node = node.get(token)
    return node if isinstance(node, dict) else {"ref": ref}


def summarize_schema(document: dict, schema: dict | None) -> dict:
    if not schema:
        return {}
    if "$ref" in schema:
        resolved = resolve_ref(document, schema["$ref"])
        summary = summarize_schema(document, resolved if isinstance(resolved, dict) else {})
        summary["ref"] = schema["$ref"]
        return summary

    summary = {
        "type": schema.get("type"),
        "format": schema.get("format"),
    }
    required = schema.get("required") or []
    if required:
        summary["required"] = required
    for key in ("enum", "minimum", "maximum", "minLength", "maxLength", "pattern", "minItems", "maxItems"):
        if key in schema:
            summary[key] = schema[key]
    properties = schema.get("properties") or {}
    if isinstance(properties, dict):
        fields = {}
        for name, field_schema in properties.items():
            if isinstance(field_schema, dict):
                field_summary = {
                    "type": field_schema.get("type"),
                    "format": field_schema.get("format"),
                    "required": name in required,
                }
                for key in ("enum", "minimum", "maximum", "minLength", "maxLength", "pattern", "minItems", "maxItems"):
                    if key in field_schema:
                        field_summary[key] = field_schema[key]
                if "$ref" in field_schema:
                    field_summary["ref"] = field_schema["$ref"]
                if field_schema.get("items"):
                    field_summary["items"] = summarize_schema(document, field_schema["items"])
                fields[name] = {key: value for key, value in field_summary.items() if value not in (None, {}, [])}
        if fields:
            summary["fields"] = fields
    if schema.get("items"):
        summary["items"] = summarize_schema(document, schema["items"])
    return {key: value for key, value in summary.items() if value not in (None, {}, [])}


def summarize_media_types(document: dict, media_types: dict) -> dict:
    summary = {}
    for media_type, media_info in (media_types or {}).items():
        if not isinstance(media_info, dict):
            continue
        schema = media_info.get("schema") or {}
        summary[media_type] = summarize_schema(document, schema if isinstance(schema, dict) else {})
    return summary


def summarize_parameter(document: dict, parameter: dict) -> dict:
    schema = parameter.get("schema") or {}
    summary = {
        "name": parameter.get("name"),
        "in": parameter.get("in"),
        "required": parameter.get("required", False),
    }
    if isinstance(schema, dict):
        summary.update(
            {
                key: value
                for key, value in summarize_schema(document, schema).items()
                if key in {"type", "format", "enum", "minimum", "maximum", "minLength", "maxLength", "pattern"}
            }
        )
    return summary


def summarize_openapi(document: dict) -> dict:
    operations = []
    for path, methods in (document.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS:
                continue
            operation = operation or {}
            parameters = operation.get("parameters") or []
            request_body = operation.get("requestBody") or {}
            responses = operation.get("responses") or {}
            security = operation.get("security")
            operations.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "operationId": operation.get("operationId"),
                    "summary": operation.get("summary"),
                    "tags": operation.get("tags") or [],
                    "parameters": [
                        summarize_parameter(document, p)
                        for p in parameters
                        if isinstance(p, dict)
                    ],
                    "hasRequestBody": bool(request_body),
                    "requestBody": {
                        "required": request_body.get("required", False),
                        "content": summarize_media_types(document, request_body.get("content") or {}),
                    }
                    if isinstance(request_body, dict)
                    else {},
                    "security": security if security is not None else document.get("security", []),
                    "responses": {
                        status_code: {
                            "description": (response or {}).get("description"),
                            "content": summarize_media_types(document, (response or {}).get("content") or {}),
                        }
                        for status_code, response in sorted(responses.items())
                        if isinstance(response, dict)
                    },
                }
            )
    return {
        "title": (document.get("info") or {}).get("title"),
        "version": (document.get("info") or {}).get("version"),
        "openapi": document.get("openapi") or document.get("swagger"),
        "servers": [server.get("url") for server in (document.get("servers") or []) if isinstance(server, dict)],
        "securitySchemes": sorted((document.get("components") or {}).get("securitySchemes", {}).keys()),
        "operations": operations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize an OpenAPI or Swagger file.")
    parser.add_argument("--input", required=True, help="Path or URL for the OpenAPI or Swagger source.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    summary = summarize_openapi(load_source(args.input))
    rendered = json.dumps(summary, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
