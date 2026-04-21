# ─────────────────────────────────────────────────
# GUARDIANOPS — Terraform Main Configuration
# Tells Terraform: use AWS, use us-east-1
# ─────────────────────────────────────────────────

terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# ─────────────────────────────────────────────────
# Pull the available availability zones automatically
# This makes the code reusable in any region
# ─────────────────────────────────────────────────
data "aws_availability_zones" "available" {
  state = "available"
}
