import pulumi
import pulumi_aws as aws

# 建立 VPC
vpc = aws.ec2.Vpc("custom-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "pulumi-vpc"})

# 建立 public subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-northeast-1a",
    tags={"Name": "public-subnet"})

# 建立 Internet Gateway
igw = aws.ec2.InternetGateway("igw",
    vpc_id=vpc.id,
    tags={"Name": "pulumi-igw"})

# 建立 Route Table 並加路由到 IGW
route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "gateway_id": igw.id,
    }],
    tags={"Name": "public-route-table"})

# Route Table 與 Subnet 關聯
route_table_assoc = aws.ec2.RouteTableAssociation("public-route-table-assoc",
    subnet_id=public_subnet.id,
    route_table_id=route_table.id)

# 輸出 VPC ID
pulumi.export("vpc_id", vpc.id)
