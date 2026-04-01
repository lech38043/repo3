# dodatek do kazdej zmiennej
variable "suffix" {
  description = "suffix dla instancji"
  type        = string
  default     = "38043" # ex. rg_name:rg38043, itd
}

# variable "index" {
#   description = "index dla instancji"
#   type        = string
#   default     = "38043" 
# }

variable "rg_name" {
  description = "Nazwa grupy zasobów w Azure"
  type        = string
  default     = "rg"
}

variable "rg_location" {
  description = "Region dla zasobów Azure"
  type        = string
  default     = "francecentral" # westeurope"
}

variable "mssql_server" {
  description = "Nazwa serwera MSSQL"
  type        = string
  default     = "sqlserver"
}

variable "sql_database" {
  description = "Nazwa bazy danych"
  type        = string
  #  default     = "sqldb"
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