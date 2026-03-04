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
resource "azurerm_resource_group" "rg-repo3" {
  name     = "rg-repo3"
  location = "francecentral"
}

# SQL Server
resource "azurerm_mssql_server" "sqlserver" {
  name                         = "sqlserver-repo3"
  resource_group_name          = azurerm_resource_group.rg-repo3.name
  location                     = azurerm_resource_group.rg-repo3.location
  version                      = "12.0"
  administrator_login          = "sqladminuser"
  administrator_login_password = "P@ssword1234!"
  public_network_access_enabled = true
}

# SQL Database (Basic tier)
resource "azurerm_mssql_database" "sqldb" {
  name      = "sqldb-repo3"
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