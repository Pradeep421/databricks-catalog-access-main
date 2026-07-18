locals {
  access_privileges = {
    reader = ["USE_CATALOG"]
    editor = ["USE_CATALOG", "CREATE_SCHEMA", "CREATE_VOLUME"]
  }

  catalog_grants = flatten([
    for catalog_name, catalog_config in var.catalog : concat(
      [
        for principal in try(catalog_config.group_name.reader, []) : {
          catalog_name = catalog_name
          principal    = principal
          access_type  = "reader"
        }
      ],
      [
        for principal in try(catalog_config.group_name.editor, []) : {
          catalog_name = catalog_name
          principal    = principal
          access_type  = "editor"
        }
      ],
      [
        for principal in try(catalog_config.spn.reader, []) : {
          catalog_name = catalog_name
          principal    = principal
          access_type  = "reader"
        }
      ],
      [
        for principal in try(catalog_config.spn.editor, []) : {
          catalog_name = catalog_name
          principal    = principal
          access_type  = "editor"
        }
      ]
    )
  ])
}

resource "databricks_catalog" "this" {
  for_each = var.catalog

  name  = each.key
  owner = var.owner

  properties = {
    tag = var.tag
  }
}

resource "databricks_grants" "catalog" {
  for_each = var.catalog

  catalog = databricks_catalog.this[each.key].name

  dynamic "grant" {
    for_each = {
      for grant_config in local.catalog_grants :
      "${grant_config.catalog_name}.${grant_config.access_type}.${grant_config.principal}" => grant_config
      if grant_config.catalog_name == each.key
    }

    content {
      principal  = grant.value.principal
      privileges = local.access_privileges[grant.value.access_type]
    }
  }
}
