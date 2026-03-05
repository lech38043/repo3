# dodatek do kazdej zmiennej
variable "suffix" {
  description = "Nazwa grupy zasobów w Azure"
  type        = string
  default     = "-repo3" # rg_name:repo3-rg-38043, itd
}

variable "rg_name" {
  description = "Nazwa grupy zasobów w Azure"
  type        = string
  default     = "rg-38043"
}

variable "rg_location" {
  description = "Region dla zasobów Azure"
  type        = string
  default     = "francecentral" # westeurope"
}

variable "mssql_server_name" {
  description = "Nazwa serwera MSSQL"
  type        = string
  default     = "sqlserver-38043"
}

variable "database_name" {
  description = "Nazwa bazy danych"
  type        = string
  default     = "sqldb"
}

variable "sql_admin_login" {
  description = "Login administratora MSSQL"
  type        = string
}

variable "sql_admin_password" {
  description = "Hasło administratora MSSQL"
  type        = string
  sensitive   = true
}