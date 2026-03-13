#!/usr/bin/env python3
"""Extract a compact JSON summary from a WSDL file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree


NS = {
    "wsdl": "http://schemas.xmlsoap.org/wsdl/",
    "soap": "http://schemas.xmlsoap.org/wsdl/soap/",
}


def summarize_wsdl(path: Path) -> dict:
    root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
    services = []
    for service in root.findall("wsdl:service", NS):
        ports = []
        for port in service.findall("wsdl:port", NS):
            address = port.find("soap:address", NS)
            ports.append(
                {
                    "name": port.get("name"),
                    "location": None if address is None else address.get("location"),
                }
            )
        services.append({"name": service.get("name"), "ports": ports})

    port_types = []
    for port_type in root.findall("wsdl:portType", NS):
        operations = []
        for operation in port_type.findall("wsdl:operation", NS):
            faults = [fault.get("name") for fault in operation.findall("wsdl:fault", NS)]
            operations.append({"name": operation.get("name"), "faults": faults})
        port_types.append({"name": port_type.get("name"), "operations": operations})

    return {"services": services, "portTypes": port_types}


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a WSDL file.")
    parser.add_argument("--input", required=True, help="Path to the WSDL file.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    summary = summarize_wsdl(Path(args.input))
    rendered = json.dumps(summary, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
