Atlas One POS Fallback Service
------------------------------

Purpose:
This microservice provides POS failure fallback handling for Atlas One.
It receives POS failure events and returns a structured fallback response
that can be used by upstream systems to route transactions or trigger workflows.

Deployment Target:
Azure Container Apps
Managed Environment: managedEnvironment-atlasonecore-8480
Registry: atlasoneacr.azurecr.io

Endpoints:
/health
/fallback/pos-failure

Port:
8080

Notes:
This service is Phase 1 compliant and does not require Postgres, Redis,
NATS, Vault, or any Phase 2 infrastructure.
