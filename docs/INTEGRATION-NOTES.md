# Workflow Engine and POS Fallback: Integration Notes

Integrated by Nick Muigai (TechNick Solutions), October 22, 2026.
Source: workflow-engine.zip, pos-fallback.zip, manifests.zip and github.zip (uploaded to atlasone-deploy by Elvis, Oct 22).

All changes below were needed for the packages to build, start and deploy to the Azure environment. Service logic was not changed.

## Packaging

- Every file in the ZIPs was a folder holding a `New Text Document.txt` (for example `Dockerfile/New Text Document.txt`). Rebuilt as real files.
- `github/workflows/` moved to `.github/workflows/`. GitHub only runs workflows from `.github`.

## Services

| Service | Change | Reason |
|---|---|---|
| pos-fallback | Folder `apps/` renamed to `app/` | The Dockerfile copies `app/` and starts `app.main:app`. With `apps/` the image build fails. |
| pos-fallback | `routes.py` imports `handle_pos_failure` instead of `handle_pos_failure_event` | `handle_pos_failure_event` does not exist. The service crashed on startup with an ImportError. |
| pos-fallback | Route changed from `/pos/failure` to `/fallback/pos-failure` | Matches the endpoint documented in the service README. |
| both | Added `app/__init__.py` | Makes `app` a regular Python package. |
| both | Pinned `fastapi==0.115.6`, `uvicorn==0.32.1` | Unpinned versions can change between builds. |

Tested locally: both services start on port 8080, `GET /health` returns 200, and all POST endpoints return the expected JSON.

## Manifests

| Change | Reason |
|---|---|
| Resource group `atlasonecore` changed to `atlasone-core` | `atlasonecore` does not exist. |
| Resource type `Microsoft.Web/containerApps` changed to `Microsoft.App/containerApps` | `Microsoft.Web` is the old preview provider. The environment ID path is corrected to match. |
| `<SUB-ID>` filled in | Subscription 89f827c6-d82e-41a3-95d5-bbffc115fc9c. |
| ACR username/password removed; registry pull uses user-assigned managed identity `atlasone-acrpull-id` | ACR admin user is disabled, so username/password login fails. The scope requires Managed Identity. |
| App names changed to `atlasone-<service>-<env>` | Matches the names in the Oct 22 task document (Task N4). |
| Image tags `:staging` / `:prod` changed to `:latest` for first deploy; pipeline then deploys by Git SHA | The task document builds `:latest`. No `:staging` or `:prod` tags are ever pushed, so those apps would fail to pull. |
| Removed `apiVersion` / `kind` | Not part of the `az containerapp create --yaml` format. |
| Added env vars `APP_ENV`, `PORT`, `HEALTH_ENDPOINT` | From the Oct 20 email. |
| Added liveness/readiness probes on `/health` and scale rules (min 1 replica) | So health is checked by the platform and the app does not scale to zero. |

## GitHub Actions workflows

| Change | Reason |
|---|---|
| `AZURE_CREDENTIALS` (service principal secret) replaced with OIDC login (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`) | The Oct 20 package requires no service principal secrets. OIDC stores no password. |
| `ACR_USERNAME` / `ACR_PASSWORD` docker login removed; image built with `az acr build` | ACR admin user is disabled. `az acr build` builds in Azure using the signed-in identity. |
| Resource group `atlasonecore` changed to `atlasone-core`; app names match the manifests | Deploy step would fail. |
| Added branch filter (`main`) and a manual run option for staging or prod | Previously deployed from any branch and had no way to reach prod. |
| Image pushed as both `:<git-sha>` and `:latest` | SHA for traceability, `latest` for the task document. |
| Added a post-deploy `/health` check | The pipeline fails if the new revision is unhealthy. |
| Action versions updated (`checkout@v4`, `azure/login@v2`) | Current versions. |

## Notes

- The POS fallback logic is a placeholder: it echoes the request and returns `fallback_triggered`. The code comment says it will be extended once Phase 3 orchestration is defined.
- Each app has an interactive API page at `/docs` where the endpoints can be tried in a browser.

## Required from Elvis (role assignments, which Contributor cannot create)

1. AcrPull on `atlasoneacr` for the managed identity `atlasone-acrpull-id` (created by Nick in `atlasone-core`).
2. An Entra app registration for GitHub OIDC with a federated credential for `Atlasoneglobal1/atlasone-deploy` (branch `main`), Contributor on `atlasone-core` (needed for `az acr build` and `az containerapp update`). Then its client ID added as the `AZURE_CLIENT_ID` GitHub secret.
