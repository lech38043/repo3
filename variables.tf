# dodatek do kazdej zmiennej
variable "suffix" {
  description = "Nazwa grupy zasobów w Azure"
  type        = string
  default     = "-repo3" # rg_name:repo3-rg-38043, itd
}

# Nazwa grupy zasobów
variable "rg_name" {
  description = "Nazwa grupy zasobów w Azure"
  type        = string
  default     = "rg-38043"
}

# Lokalizacja zasobów
variable "rg_location" {
  description = "Region dla zasobów Azure"
  type        = string
  default     = "francecentral" #"westeurope"
}

# Nazwa serwera MSSQL
variable "mssql_server_name" {
  description = "Nazwa serwera MSSQL"
  type        = string
  default     = "sqlserver-38043"
}

# Nazwa bazy danych
variable "database_name" {
  description = "Nazwa bazy danych"
  type        = string
  default     = "sqldb"
}

# Login administratora SQL
variable "sql_admin_login" {
  description = "Login administratora MSSQL"
  type        = string

}

# Hasło administratora SQL
variable "sql_admin_password" {
  description = "Hasło administratora MSSQL"
  type        = string
  sensitive   = true

}