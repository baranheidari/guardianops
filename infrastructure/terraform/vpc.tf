# ─────────────────────────────────────────────────
# GUARDIANOPS — VPC and Networking
#
# We create:
# - 1 VPC (your private data center in AWS)
# - 2 public subnets  (internet-facing: load balancer lives here)
# - 2 private subnets (hidden from internet: app + DB live here)
# - Internet Gateway  (the door to the internet)
# - NAT Gateway       (lets private subnets reach internet safely)
# - Route Tables      (traffic signs telling packets where to go)
# ─────────────────────────────────────────────────

# The VPC — your isolated network bubble
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name    = "${var.project_name}-vpc"
    Project = var.project_name
  }
}

# ── PUBLIC SUBNETS ──────────────────────────────
# These have direct access to the internet
# Load balancer (ALB) will live here

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name                                              = "${var.project_name}-public-${count.index + 1}"
    Project                                           = var.project_name
    "kubernetes.io/role/elb"                          = "1"
    "kubernetes.io/cluster/${var.project_name}-cluster" = "shared"
  }
}

# ── PRIVATE SUBNETS ─────────────────────────────
# Hidden from internet — app pods and RDS live here

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name                                              = "${var.project_name}-private-${count.index + 1}"
    Project                                           = var.project_name
    "kubernetes.io/role/internal-elb"                 = "1"
    "kubernetes.io/cluster/${var.project_name}-cluster" = "shared"
  }
}

# ── INTERNET GATEWAY ────────────────────────────
# The front door — connects your VPC to the internet

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name    = "${var.project_name}-igw"
    Project = var.project_name
  }
}

# ── ELASTIC IP for NAT Gateway ──────────────────
# A fixed public IP address for outbound traffic

resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name    = "${var.project_name}-nat-eip"
    Project = var.project_name
  }
}

# ── NAT GATEWAY ─────────────────────────────────
# Lets private subnets reach the internet (one-way)
# Your app pods can download packages but can't be reached directly

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name    = "${var.project_name}-nat"
    Project = var.project_name
  }

  depends_on = [aws_internet_gateway.main]
}

# ── ROUTE TABLE: PUBLIC ─────────────────────────
# Traffic rule: anything going outside → use internet gateway

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name    = "${var.project_name}-public-rt"
    Project = var.project_name
  }
}

# ── ROUTE TABLE: PRIVATE ────────────────────────
# Traffic rule: anything going outside → use NAT gateway

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name    = "${var.project_name}-private-rt"
    Project = var.project_name
  }
}

# ── ROUTE TABLE ASSOCIATIONS ────────────────────
# Glue: connect each subnet to its route table

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
