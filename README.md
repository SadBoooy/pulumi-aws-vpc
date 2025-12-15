專案目標

使用 Pulumi（Python） 管理 AWS Infrastructure

建立符合最佳實務的 Public / Private Subnet 架構

透過 Pulumi preview 在部署前確認基礎架構變更

設計 GitLab CI/CD Pipeline，降低 Infrastructure 變更風險

架構說明（AWS VPC）

本專案建立以下 AWS 資源：

VPC

CIDR：10.0.0.0/16

Public Subnet

CIDR：10.0.1.0/24

對外連線（Internet Gateway）

Private Subnet

CIDR：10.0.2.0/24

不直接暴露於 Internet

Internet Gateway（IGW）

提供 Public Subnet 對外連線

NAT Gateway（含 Elastic IP）

允許 Private Subnet 對外連線（僅 outbound）

Route Tables

Public Subnet → IGW

Private Subnet → NAT Gateway

此架構為 AWS 上常見的網路隔離設計，可降低內部資源直接暴露的風險。

專案結構
pulumi-aws-vpc/
├── __main__.py           # Pulumi Infrastructure 定義（Python）
├── Pulumi.yaml           # Pulumi 專案設定
├── Pulumi.dev.yaml       # dev stack 設定
├── requirements.txt      # Python 套件依賴
├── .gitlab-ci.yml        # GitLab CI/CD Pipeline
├── README.md
└── .gitignore

Pulumi 環境配置與設定
1. 需求工具

Python 3.x

AWS CLI

Pulumi CLI

Git

2. 建立 Python 虛擬環境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. AWS 認證設定（建議使用 Profile）

本專案 不將 AWS Access Key 寫入程式碼或 repo，
而是透過 AWS CLI profile 管理認證資訊。

aws configure --profile pulumi-dev
export AWS_PROFILE=pulumi-dev


確認認證是否正確：

aws sts get-caller-identity

4. Pulumi Stack 設定

設定 AWS Region（以 ap-northeast-1 為例）：

pulumi config set aws:region ap-northeast-1

5. Pulumi 操作指令
預覽變更（不會實際修改 AWS）
pulumi preview

部署基礎架構（實際修改 AWS）
pulumi up

移除資源（清理環境）
pulumi destroy

Pulumi Preview 與 Deploy 的差異

pulumi preview

僅顯示「如果部署會發生什麼變化」

不會修改 AWS

用於風險評估與審查

pulumi up

實際建立 / 修改 AWS 資源

具備風險，需謹慎執行

GitLab CI/CD Pipeline 設計

本專案包含一條示範用的 GitLab CI/CD Pipeline（.gitlab-ci.yml），
用於展示 Infrastructure as Code 的常見流程。

Pipeline Stages
validate → preview → deploy

各 Stage 說明
1. validate（CI）

檢查 Python 語法是否正確

不存取 AWS

最快速、最安全的檢查階段

2. preview（CI）

僅在 Merge Request（MR） 階段執行

使用 pulumi preview 顯示 Infrastructure 變更內容

不實際部署資源

供團隊審查 Infrastructure 影響

3. deploy（CD）

僅允許在 main branch 執行

必須手動觸發（manual approval）

執行 pulumi up，實際修改 AWS

CI/CD 設計理念

Infrastructure 變更風險高，不應自動部署

Preview 階段用於「讓人理解變更」

Deploy 階段需人為確認，避免誤操作造成事故

Secrets（Pulumi Token、AWS Key）應存放於 GitLab CI Variables

為什麼 Deploy 要手動觸發？

CI 為自動化工具，無法判斷風險

Infrastructure 錯誤可能導致整個系統中斷

Manual Deploy 確保每次部署都有明確負責人

總結

本專案示範：

使用 Pulumi（Python）實作 Infrastructure as Code

建立安全的 AWS VPC 網路架構

在部署前透過 Preview 降低風險

設計符合實務的 GitLab CI/CD Pipeline

避免將認證資訊寫入程式碼

 # AWS Python S3 Bucket Pulumi Template

 A minimal Pulumi template for provisioning a single AWS S3 bucket using Python.

 ## Overview

 This template provisions an S3 bucket (`pulumi_aws.s3.BucketV2`) in your AWS account and exports its ID as an output. It’s an ideal starting point when:
  - You want to learn Pulumi with AWS in Python.
  - You need a barebones S3 bucket deployment to build upon.
  - You prefer a minimal template without extra dependencies.

 ## Prerequisites

 - An AWS account with permissions to create S3 buckets.
 - AWS credentials configured in your environment (for example via AWS CLI or environment variables).
 - Python 3.6 or later installed.
 - Pulumi CLI already installed and logged in.

 ## Getting Started

 1. Generate a new project from this template:
    ```bash
    pulumi new aws-python
    ```
 2. Follow the prompts to set your project name and AWS region (default: `us-east-1`).
 3. Change into your project directory:
    ```bash
    cd <project-name>
    ```
 4. Preview the planned changes:
    ```bash
    pulumi preview
    ```
 5. Deploy the stack:
    ```bash
    pulumi up
    ```
 6. Tear down when finished:
    ```bash
    pulumi destroy
    ```

 ## Project Layout

 After running `pulumi new`, your directory will look like:
 ```
 ├── __main__.py         # Entry point of the Pulumi program
 ├── Pulumi.yaml         # Project metadata and template configuration
 ├── requirements.txt    # Python dependencies
 └── Pulumi.<stack>.yaml # Stack-specific configuration (e.g., Pulumi.dev.yaml)
 ```

 ## Configuration

 This template defines the following config value:

 - `aws:region` (string)
   The AWS region to deploy resources into.
   Default: `us-east-1`

 View or update configuration with:
 ```bash
 pulumi config get aws:region
 pulumi config set aws:region us-west-2
 ```

 ## Outputs

 Once deployed, the stack exports:

 - `bucket_name` — the ID of the created S3 bucket.

 Retrieve outputs with:
 ```bash
 pulumi stack output bucket_name
 ```

## CI/CD
This repository includes a sample GitLab CI/CD pipeline (.gitlab-ci.yml)
demonstrating infrastructure validation, preview on merge requests,
and manual deployment on the main branch.

 ## Next Steps

 - Customize `__main__.py` to add or configure additional resources.
 - Explore the Pulumi AWS SDK: https://www.pulumi.com/registry/packages/aws/
 - Break your infrastructure into modules for better organization.
 - Integrate into CI/CD pipelines for automated deployments.

 ## Help and Community

 If you have questions or need assistance:
 - Pulumi Documentation: https://www.pulumi.com/docs/
 - Community Slack: https://slack.pulumi.com/
 - GitHub Issues: https://github.com/pulumi/pulumi/issues

 Contributions and feedback are always welcome!