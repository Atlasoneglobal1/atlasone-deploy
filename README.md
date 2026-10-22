📘 Atlas One v40.1 — Deployment Repository (README)
Overview
This repository contains the Atlas One v40.1 Unified Deployment Baseline and the Phase 1 Azure Container Apps deployment, including the Workflow Engine and POS Fallback services, manifests, and GitHub Actions workflows required for Phase 1 (Nick) and Phase 2/3 (Ignatius) engineering work.

The YAML package represents the frozen v40.1 architecture, including:

Identity Layer

Telco Sovereignty (SIM/eSIM/LTE)

Routing Identity (TSIO)

Provenance Engine (WPS)

Food Defense Sovereign Stack

ELB Event Mesh

Gateway Routing

Vertical Adapters (health, gig, remit, title, mortgage, food defense)

This baseline is the single source of truth for the v40.1 architecture and code generation work.

Phase 1 Target Platform
Phase 1 deploys to Azure Container Apps (confirmed October 22, 2026):

Azure Container Apps — environment managedEnvironment‑atlasonecore‑8480

Azure Container Registry — atlasoneacr (atlasoneacr.azurecr.io)

Resource group — atlasone‑core

Key Vault — atlasone‑kv‑core

Managed Identity — atlasone‑acrpull‑id (pulls images from ACR; no registry passwords)

All AWS / EKS / GHCR references in the v40.1 YAML and codebase are legacy and are not used for deployment.

Repository Structure
Code
atlasone-deploy/
  .github/workflows/
    workflow-engine-deploy.yml  # Build, push and deploy the Workflow Engine
    pos-fallback-deploy.yml     # Build, push and deploy the POS Fallback
  services/
    workflow-engine/            # FastAPI service, Dockerfile, requirements
    pos-fallback/               # FastAPI service, Dockerfile, requirements
  manifests/                    # Container App definitions (staging + prod)
  docs/
    INTEGRATION-NOTES.md        # Fixes made when integrating the service packages
  codebase/                     # v40.1 reference source (legacy, AWS/EKS)
  yaml/
    atlas-one-v40.1.yaml        # Unified deployment baseline (architecture reference)
Additional folders will be added during code generation:

Code
  docker/
  verticals/
Services
Workflow Engine
Workflow orchestration entry points for POS failure fallback routing and CE → Title → Mortgage workflow initiation.

Endpoints: /health, /workflow/pos-failure, /workflow/ce-title-mortgage

Port: 8080

Container Apps: atlasone‑workflow‑engine‑staging, atlasone‑workflow‑engine‑prod

POS Fallback
Receives POS failure events and returns a structured fallback response that upstream systems use to route transactions or trigger workflows.

Endpoints: /health, /fallback/pos-failure

Port: 8080

Container Apps: atlasone‑pos‑fallback‑staging, atlasone‑pos‑fallback‑prod

Both services are FastAPI, expose an interactive API page at /docs, and do not require Postgres, Redis, NATS, Vault, or any Phase 2 infrastructure.

Deployment
Push to main (changes under services/<service>/) — builds the image in ACR, tags it with the Git SHA and latest, deploys to staging, and checks /health.

Manual run (Actions tab → Run workflow) — deploy to staging or prod.

GitHub signs in to Azure with OIDC. Required repository secrets: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID.

Manual commands:

Code
az acr build --registry atlasoneacr --image workflow-engine:latest services/workflow-engine
az containerapp create -n atlasone-workflow-engine-staging -g atlasone-core --yaml manifests/workflow-engine-staging.yaml
File: atlas-one-v40.1.yaml
This file contains:

All microservice container definitions

Environment variables

Secrets (referenced, not stored)

Namespace routing

ELB channel definitions

Scaling rules

Logging + monitoring configuration

Cluster metadata (EKS / Istio / ESO) — legacy

Vertical adapters

Food Defense threat graph + scoring + lockdown + recovery + monitoring + simulation

This YAML file is the architecture reference and will be used for:

Phase 2 scaling + CI/CD (Ignatius)

Phase 3 vertical activation

Code generation alignment

Patent deployment diagrams

Responsibilities
Nick — Phase 1 Deployment
Nick will:

Integrate the Workflow Engine and POS Fallback services

Build and push images to atlasoneacr

Deploy staging and production Container Apps in atlasone‑core

Bind secrets and environment variables

Wire CI/CD via GitHub Actions

Validate health checks and logging

Prepare for Phase 3 vertical adapter activation

Ignatius — Phase 2 & 3 Scaling + CI/CD
Ignatius will use this YAML to:

Scale identity, provenance, and safety lineage

Extend CI/CD pipelines

Configure monitoring + logging

Optimize performance and autoscaling

Integrate regulator routing

Prepare production‑grade deployment

Versioning
Build: atlas-one-v40.1.0-stable

Generated: 2026‑10‑18

Deployment Target: Azure Container Apps (East US)

Registry: atlasoneacr.azurecr.io

Legacy v40.1 baseline target: EKS (us‑east‑1), Kubernetes 1.30, Istio 1.23, ESO 0.10

All future updates will follow semantic versioning:

Code
v40.1.x
Notes for Engineers
This YAML file is frozen and must not be modified without founder approval.

All code generation will reference this baseline.

CI/CD pipelines are in .github/workflows and deploy to Azure Container Apps.

Vertical activation (Phase 3) depends on this exact routing and namespace layout.

Contact
For architecture questions: Elvis Ackel
For Phase 1 deployment: Nick (TechNick Solutions)
For Phase 2/3 scaling: Ignatius (Repartiq)

Guided Links (for deeper context)
v40.1 Architecture

YAML Baseline

Phase 1 Responsibilities

Phase 2 Responsibilities

Begin Code Generation
