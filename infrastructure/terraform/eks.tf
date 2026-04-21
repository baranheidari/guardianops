# ─────────────────────────────────────────────────
# GUARDIANOPS — EKS Cluster (Kubernetes on AWS)
#
# We create:
# - IAM role for the cluster control plane
# - The EKS cluster itself
# - IAM role for the worker nodes
# - Node group (the EC2 machines that run your containers)
# - Security group (firewall rules)
# ─────────────────────────────────────────────────

# ── IAM ROLE: EKS CLUSTER ───────────────────────
# EKS needs permission to manage AWS resources on your behalf
# Think of it as giving the cluster a security badge

resource "aws_iam_role" "eks_cluster" {
  name = "${var.project_name}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })

  tags = { Project = var.project_name }
}

# Attach AWS managed policies to the cluster role
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

# ── SECURITY GROUP: EKS CLUSTER ─────────────────
# Firewall rules — controls what traffic can reach the cluster

resource "aws_security_group" "eks_cluster" {
  name        = "${var.project_name}-eks-cluster-sg"
  description = "Security group for GuardianOps EKS cluster"
  vpc_id      = aws_vpc.main.id

  # Allow all outbound traffic (cluster needs to reach ECR, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-eks-cluster-sg"
    Project = var.project_name
  }
}

# ── EKS CLUSTER ─────────────────────────────────
# The actual Kubernetes control plane
# AWS manages this for you — no manual setup needed

resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.eks_cluster_version

  vpc_config {
    subnet_ids              = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
    security_group_ids      = [aws_security_group.eks_cluster.id]
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]

  tags = { Project = var.project_name }
}

# ── IAM ROLE: WORKER NODES ──────────────────────
# The EC2 machines (nodes) also need permissions
# They need to pull images from ECR, register with cluster, etc.

resource "aws_iam_role" "eks_nodes" {
  name = "${var.project_name}-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })

  tags = { Project = var.project_name }
}

# Worker nodes need 3 AWS managed policies
resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_ecr_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes.name
}

# ── NODE GROUP ──────────────────────────────────
# The actual EC2 machines that run your containers
# Auto-scaling: min 1, desired 2, max 3

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id
  instance_types  = [var.node_instance_type]

  scaling_config {
    desired_size = var.node_desired_count
    min_size     = var.node_min_count
    max_size     = var.node_max_count
  }

  update_config {
    max_unavailable = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_ecr_readonly,
  ]

  tags = { Project = var.project_name }
}
