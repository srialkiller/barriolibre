# BarrioLibre — CI local (Build Engineer BE-004)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "==> cargo fmt --check"
cargo fmt --all -- --check

Write-Host "==> cargo clippy"
cargo clippy --all-targets --features dev_fast -- -D warnings

Write-Host "==> cargo test"
cargo test --features dev_fast

Write-Host "==> map_validator"
cargo run -p map_validator --quiet -- data/maps/barrio_tutorial_01

Write-Host "==> cargo build --release"
cargo build --release

Write-Host "CI local: OK"
