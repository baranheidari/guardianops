# ─────────────────────────────────────────────────
# GUARDIANOPS — EKS Cluster
# Using pre-existing Vocareum lab roles
# ─────────────────────────────────────────────────

# Look up existing roles — don't create them
data "aws_iam_role" "eks_cluster" {
  name = "c193349a4970076l13675961t1w713890-LabEksClusterRole-3yl0iY75OvCX"
}

data "aws_iam_role" "eks_nodes" {
  name = "c193349a4970076l13675961t1w713890439-LabEksNodeRole-tkbGPbpGQKv7"
}

# ── SECURITY GROUP: EKS CLUSTER ─────────────────
resource "aws_security_group" "eks_cluster" {
  name        = "${var.project_name}-eks-cluster-sg"
  description = "Security group for GuardianOps EKS cluster"
  vpc_id      = aws_vpc.main.id

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
resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-cluster"
  role_arn = data.aws_iam_role.eks_cluster.arn
  version  = var.eks_cluster_version

  vpc_config {
    subnet_ids              = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
    security_group_ids      = [aws_security_group.eks_cluster.id]
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  tags = { Project = var.project_name }
}

# ── NODE GROUP ──────────────────────────────────
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-nodes"
  node_role_arn   = data.aws_iam_role.eks_nodes.arn
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

  tags = { Project = var.project_name }
}
