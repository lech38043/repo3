# main.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "rg-local" {
  name     = "${var.rg_name}${var.suffix}"
  location = var.rg_location
}

# SQL Server
resource "azurerm_mssql_server" "sqlserver" {
  name                         = var.mssql_server_name # "sqlserver-repo38043"
  resource_group_name          = azurerm_resource_group.rg-local.name
  location                     = azurerm_resource_group.rg-local.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
  public_network_access_enabled = true
}

# SQL Database (Basic tier)
resource "azurerm_mssql_database" "sqldb" {
  name      = "${var.database_name}${var.suffix}" # "sqldb-repo38043"
  server_id = azurerm_mssql_server.sqlserver.id
  sku_name  = "Basic"
  max_size_gb = 2
}

# pobranei do obiektu "http"
data "http" "my_ip" {
  url = "https://api.ipify.org"
}

resource "azurerm_mssql_firewall_rule" "allow_my_ip" {
  name      = "AllowMyCurrentIP"
  server_id = azurerm_mssql_server.sqlserver.id

  start_ip_address = chomp(data.http.my_ip.response_body)
  end_ip_address   = chomp(data.http.my_ip.response_body)
}