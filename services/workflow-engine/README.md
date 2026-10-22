Atlas One Workflow Engine
-------------------------

Purpose:
This microservice provides workflow orchestration endpoints for:
- POS failure fallback routing
- CE → Title → Mortgage workflow initiation

Deployment Target:
Azure Container Apps
Managed Environment: managedEnvironment-atlasonecore-8480
Registry: atlasoneacr.azurecr.io

Endpoints:
/health
/workflow/pos-failure
/workflow/ce-title-mortgage

Port:
8080

Notes:
This service is Phase 1 compliant and does not require Postgres, Redis, NATS, Vault, or any Phase 2 infrastructure.
