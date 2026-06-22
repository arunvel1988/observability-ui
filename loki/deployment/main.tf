module "kubernetes" {
  source  = "git::https://github.com/arunvel1988/terraform-kubernetes-kind-module.git?ref=v1.0.0"

  cluster_name    = "test-cluster"
  workers         = 3
  cluster_version = "v1.27.1"
  kubeconfig_file = "/tmp/kube.config"
}