# BarrioLibre — run dev (fast compile + map-only assets)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "cargo run (dev_fast: dynamic linking, map-only assets)"
cargo run --features dev_fast @args
