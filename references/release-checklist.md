# Release Checklist

## Before Publishing

1. Run `python scripts/validate_skill_family.py --root restassured-skill`.
2. Run the external validator on the root skill if the environment provides it.
3. Verify every skill folder has:
   - `SKILL.md`
   - `agents/openai.yaml`
4. Verify deterministic scripts still compile with `python -m py_compile`.
5. Re-run at least one representative dry run after major changes to routing or scripts.

## Packaging

1. Generate a release manifest with `python scripts/generate_release_manifest.py --root restassured-skill --output <manifest-md>`.
2. Review the manifest for stale display names or descriptions.
3. Confirm the capability map still matches the actual skill surface.

## Final Check

1. Make sure no publish-critical work is hidden only in session-state artifacts.
2. Make sure examples in root `SKILL.md` still route to real skills.
3. Prefer publishing only after the root validator and one live dry run are both clean.
