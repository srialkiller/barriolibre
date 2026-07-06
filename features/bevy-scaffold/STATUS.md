# Bevy Scaffold — Status

| Field | Value |
|---|---|
| **Branch** | `feature/bevy-scaffold` |
| **Release** | `release/vertical-slice` |
| **Lifecycle** | `planned` |
| **Sprint** | Sprint_01 |
| **Registry** | `production/branches/registry.json` |

## State machine

```
[planned] → Draft → In Design → Implementation → QA → Ready to Merge → Merged
```

**Current:** `planned` — esperando Release Manager abra rama.

## Merge target

`develop` → integración en `release/vertical-slice`

## Blockers

- B-001: No Cargo.toml (esta feature lo resuelve)

## Approvals required

- [ ] POL-005 Technical Director — `cargo check`
- [ ] POL-006 QA Director — window opens, GameState switches
- [ ] POL-007 Studio Director — Sprint 01 exit criteria
