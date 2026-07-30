terraform {
  backend "s3" {
    assume_role = {
      role_arn = "arn:aws:iam::311462405659:role/opg-data-lpa-terraform-state-access"
    }
    bucket       = "opg.terraform.state"
    encrypt      = true
    key          = "opg-data-lpa/account/terraform.tfstate"
    region       = "eu-west-1"
    use_lockfile = true
  }
}

provider "aws" {
  assume_role {
    role_arn     = "arn:aws:iam::${local.account.account_id}:role/${var.default_role}"
    session_name = "terraform-session"
  }
  default_tags {
    tags = local.default_tags
  }
}

provider "aws" {
  alias = "management"

  assume_role {
    role_arn     = "arn:aws:iam::311462405659:role/${var.management_role}"
    session_name = "terraform-session"
  }
  default_tags {
    tags = local.default_tags
  }
}
