---
name: restassured-documentation-tests
description: Use when Codex needs to add human-readable documentation to Rest Assured automation code, including class purpose, role boundaries, shared specs, and scenario intent.
metadata:
  author: jovd83
  version: "1.0"
---

# Document Automation Code

## 1. Document Only What Helps

1. Add class-level comments when the test role is not obvious.
2. Add short comments before complex setup or custom filters.
3. Do not add comments that restate the code literally.

## 2. Explain Boundaries

1. Explain shared specs, auth helpers, builders, and virtualization seams.
2. Explain why a test is tagged as smoke, contract, or integration when not obvious.

## 3. Troubleshooting

1. Problem: The code already reads clearly.
   Fix: Do not add noise comments.
