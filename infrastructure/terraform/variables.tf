# ─────────────────────────────────────────────────
# GUARDIANOPS — Variables
# All the settings in one place — easy to change
# ─────────────────────────────────────────────────

variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for naming all resources"
  type        = string
  default     = "guardianops"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC (the IP address range)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "eks_cluster_version" {
  description = "Kubernetes version for EKS"
  type        = string
  default     = "1.29"
}

variable "node_instance_type" {
  description = "EC2 instance type for Kubernetes worker nodes"
  type        = string
  default     = "t3.medium"
}

variable "node_desired_count" {
  description = "Number of worker nodes to run normally"
  type        = number
  default     = 2
}

variable "node_min_count" {
  description = "Minimum worker nodes (scale-in limit)"
  type        = number
  default     = 1
}

variable "node_max_count" {
  description = "Maximum worker nodes (scale-out limit)"
  type        = number
  default     = 3
}
