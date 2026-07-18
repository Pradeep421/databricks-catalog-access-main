variable "catalog_url" {
  description = "Databricks workspace URL used by the caller's Databricks provider configuration."
  type        = string
}

variable "owner" {
  description = "Catalog owner."
  type        = string
}

variable "tag" {
  description = "Environment or ownership tag value applied to each catalog."
  type        = string
}

variable "catalog" {
  description = "Catalog access map. Each catalog can define group_name and spn principals by access level."
  type = map(object({
    group_name = optional(object({
      reader = optional(list(string), [])
      editor = optional(list(string), [])
    }), {})
    spn = optional(object({
      reader = optional(list(string), [])
      editor = optional(list(string), [])
    }), {})
  }))
}
