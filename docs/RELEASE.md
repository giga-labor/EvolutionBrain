# Release Guide

## Versioning
Usare Semantic Versioning: `MAJOR.MINOR.PATCH`.

## Preparazione release
1. Aggiorna `CHANGELOG.it.md`.
2. Esegui test locali (`pytest`).
3. Tagga release:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

## GitHub Release
- crea release da tag
- copia note dal changelog
- allega eventuali artefatti
