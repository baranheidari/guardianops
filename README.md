# 🛡️ GuardianOps — AI-Powered Cloud Security Platform

A production-grade DevOps portfolio project demonstrating end-to-end cloud infrastructure automation on AWS.

---

## 🏗️ Architecture Overview

```
GitHub Push → GitHub Actions CI/CD → Docker Build → AWS ECR
                                                         ↓
Internet → AWS Load Balancer → Kubernetes Service → Flask App Pods
                                                         ↑
                              AWS EKS Cluster (Kubernetes v1.30)
                                                         ↑
                         Terraform-managed VPC, Subnets, Node Groups
```

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Application | Python Flask, Gunicorn |
| Containerization | Docker |
| Container Registry | AWS ECR |
| Orchestration | Kubernetes (AWS EKS v1.30) |
| Infrastructure as Code | Terraform |
| Networking | AWS VPC, Public/Private Subnets, NAT Gateway |
| CI/CD | GitHub Actions |
| Cloud | AWS (EKS, ECR, VPC, IAM) |

---

## 📁 Project Structure

```
guardianops/
├── app/
│   ├── app.py              # Flask security dashboard
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container definition
├── infrastructure/
│   ├── terraform/          # AWS infrastructure as code
│   │   ├── main.tf         # Provider configuration
│   │   ├── vpc.tf          # VPC, subnets, routing
│   │   ├── eks.tf          # EKS cluster + node group
│   │   ├── variables.tf    # Input variables
│   │   └── outputs.tf      # Output values
│   └── kubernetes/         # Kubernetes manifests
│       ├── deployment.yaml # App deployment (2 replicas)
│       ├── service.yaml    # Load balancer service
│       └── configmap.yaml  # App configuration
└── .github/
    └── workflows/
        └── deploy.yml      # CI/CD pipeline
```

---

## 🔧 Infrastructure Details

### Networking
- Custom VPC: `10.0.0.0/16`
- 2 Public subnets across `us-east-1a` and `us-east-1b`
- 2 Private subnets across `us-east-1a` and `us-east-1b`
- Internet Gateway for public access
- NAT Gateway for private subnet outbound traffic

### Kubernetes Cluster
- EKS v1.30 (upgraded from v1.29 — one minor version at a time rule)
- Node group: 2x `t3.medium` EC2 instances
- Auto-scaling: min 1, desired 2, max 3
- Rolling update deployment strategy (zero downtime)
- Liveness and readiness health probes

### CI/CD Pipeline
On every push to `main`:
1. Checkout code
2. Authenticate to AWS
3. Login to ECR
4. Build and push Docker image (tagged with commit SHA)
5. Update kubeconfig for EKS
6. Apply Kubernetes manifests
7. Rolling update deployment
8. Verify deployment health

---

## 🛠️ Key Engineering Decisions

**Vocareum IAM Constraints → Data Sources Pattern**
Vocareum sandbox environments cannot create IAM roles. Rather than failing, I used Terraform `data` sources to reference pre-existing lab roles (`LabEksClusterRole`, `LabEksNodeRole`), demonstrating the ability to adapt IaC to real-world enterprise constraints.

**EKS Authentication Mode Migration**
Migrated EKS cluster authentication from `CONFIG_MAP` to `API_AND_CONFIG_MAP` mode using `aws eks update-cluster-config` to enable modern access entry management — the same migration pattern used in production EKS upgrades.

**Kubernetes Version Upgrade**
AWS EKS only supports one minor version upgrade at a time. When `v1.29` AMIs were deprecated, upgraded to `v1.30` (not `v1.31`) — understanding and following AWS EKS upgrade policies.

**Git History Cleanup**
Accidentally committed a 674MB Terraform provider binary. Removed it from git history using `git filter-branch --force --index-filter` followed by a force push — a real-world skill for maintaining clean repository history.

**GitHub Actions for EKS Deployment**
Cloud9 sandbox network restrictions prevented direct `kubectl` access to EKS. Solved this by routing deployments through GitHub Actions, which runs on its own network infrastructure — a production-grade GitOps pattern.

---

## 🚀 Deploy Your Own

### Prerequisites
- AWS account with EKS permissions
- Terraform >= 1.0
- Docker
- kubectl
- AWS CLI

### 1. Deploy Infrastructure
```bash
cd infrastructure/terraform
terraform init
terraform apply -auto-approve
```

### 2. Configure kubectl
```bash
aws eks update-kubeconfig --region us-east-1 --name guardianops-cluster
```

### 3. Build and Push Docker Image
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t guardianops ./app
docker tag guardianops:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/guardianops:v1
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/guardianops:v1
```

### 4. Deploy to Kubernetes
```bash
kubectl apply -f infrastructure/kubernetes/
kubectl get pods -l app=guardianops
```

### 5. Tear Down (save costs)
```bash
cd infrastructure/terraform
terraform destroy -auto-approve
```

---

## 📊 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Security dashboard home |
| `GET /health` | Health check (used by Kubernetes probes) |
| `GET /api/events` | Security events feed |
| `GET /api/stats` | Dashboard statistics |

---

## 👤 Author

**Baran Heidari**
Seneca College — Computer Systems Technology
[GitHub](https://github.com/baranheidari) | bheidari3@myseneca.ca