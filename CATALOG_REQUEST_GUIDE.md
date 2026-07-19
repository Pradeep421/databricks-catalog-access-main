# Databricks Catalog Request Guide

This guide explains how to request a new Databricks catalog using the automated GitHub issue workflow.

## Overview

When a new team needs to join or requires a new catalog:

1. **Create an Issue**: Go to the [Issues](https://github.com/Pradeep421/databricks-catalog-access-submodule/issues) page and select **"New Catalog Request"**
2. **Fill in the Template**: Complete all required fields and any optional fields
3. **Automated Validation**: The system automatically validates your request
4. **Review Generated Config**: If validation passes, terraform configuration is generated
5. **Merge to Main**: Once approved, configuration is merged and deployed

---

## Naming Conventions

### Catalog Names
- **Format**: `lowercase_letters_numbers_underscores`
- **Length**: 3-64 characters
- **Examples**:
  - ✅ `data_team_catalog`
  - ✅ `analytics_prod_2024`
  - ✅ `ml_team_dev`
  - ❌ `DataTeam` (uppercase not allowed)
  - ❌ `data-team` (hyphens not allowed)
  - ❌ `dt` (too short)

### Group Names
Use your Azure AD group names exactly as they appear in your organization:
- Example: `team-readers@company.com`
- Example: `data-engineers@company.com`

### Service Principal Names (SPNs)
Use the full SPN identifier:
- Example: `app-service-principal@company.com`
- Example: `databricks-app-001@company.com`

---

## Field Requirements

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| **Catalog Name** | string | Unique identifier for the catalog (lowercase, numbers, underscores only) |
| **Owner** | string | Email or name of the principal who owns the catalog |
| **Tag** | enum | Environment identifier: `dev`, `staging`, or `prod` |
| **Reader Groups** | list | At least one Azure AD group with read access |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| **Editor Groups** | list | Azure AD groups with read/write access |
| **SPN Readers** | list | Service principals with read-only access |
| **SPN Editors** | list | Service principals with read/write access |

---

## Access Levels Explained

### Reader Access
**Permissions**: `USE_CATALOG`
- View catalog and its contents
- Cannot create schemas or volumes
- Cannot modify any objects

### Editor Access
**Permissions**: `USE_CATALOG`, `CREATE_SCHEMA`, `CREATE_VOLUME`
- View catalog and its contents
- Create and manage schemas
- Create and manage volumes
- Administer catalog objects

---

## Step-by-Step Example

### Scenario
The Data Team needs a new production catalog with:
- **Readers**: `data-readers@company.com` (Azure AD group)
- **Editors**: `data-engineers@company.com` (Azure AD group)
- **Service Principal**: `data-pipeline-prod@company.com` (read-only)

### Issue Template Filled In

```markdown
### Catalog Name (Required)
Catalog Name: data_team_prod

### Catalog Owner (Required)
Owner: data-team-lead@company.com

### Environment Tag (Required)
Tag: prod

### Group-Based Access (Mandatory)

#### Readers (Required)
Reader Groups:
- data-readers@company.com

#### Editors (Optional)
Editor Groups:
- data-engineers@company.com

### Service Principal Access (Optional)

#### SPN Readers (Optional)
SPN Readers:
- data-pipeline-prod@company.com

#### SPN Editors (Optional)
SPN Editors:
```

### Generated Configuration

Once validated, the system generates:

```hcl
  data_team_prod = {
    group_name = {
      reader = ["data-readers@company.com"]
      editor = ["data-engineers@company.com"]
    }
    spn = {
      reader = ["data-pipeline-prod@company.com"]
      editor = []
    }
  }
```

---

## Validation Checklist

Before submitting your request, verify:

- [ ] Catalog name contains only lowercase letters, numbers, and underscores
- [ ] Catalog name is between 3-64 characters
- [ ] Catalog name is unique (not already in use)
- [ ] At least one reader group is specified
- [ ] Owner email/name is valid
- [ ] Tag is one of: `dev`, `staging`, `prod`
- [ ] All group names and SPN identifiers are accurate
- [ ] No special characters in any field

---

## Common Issues and Resolutions

### ❌ "Catalog name must contain only lowercase letters, numbers, and underscores"

**Cause**: Your catalog name contains invalid characters (uppercase, hyphens, spaces, etc.)

**Solution**: 
- Replace uppercase letters with lowercase
- Replace hyphens with underscores
- Remove any spaces

**Example**: 
- ❌ `Data-Team` → ✅ `data_team`

### ❌ "Catalog already exists"

**Cause**: The catalog name you requested already exists in the configuration

**Solution**:
- Choose a different, unique catalog name
- Check with your team lead if this should use an existing catalog

### ❌ "At least one reader group is required"

**Cause**: No reader groups were specified

**Solution**:
- Add at least one Azure AD group under Reader Groups
- This is mandatory for all catalogs

### ❌ "Owner field is required"

**Cause**: The owner field is empty

**Solution**:
- Provide the email or name of the catalog owner
- This should be a valid Azure AD principal

---

## File Structure

The automation creates/modifies these files:

```
databricks-catalog-access-submodule/
├── catalog.auto.tfvars          # Your new catalog is added here
├── main.tf
├── provider.tf
└── variable.tf

databricks-catalog-access-main/
├── main.tf                       # Contains catalog and grant resources
├── variable.tf
└── provider.tf
```

---

## Approval Process

1. **Submission**: You create an issue with the template
2. **Automated Validation**: The workflow validates:
   - Catalog name format
   - Required fields presence
   - No duplicates
3. **Manual Review**: A team member reviews the configuration
4. **Approval**: Once approved, a PR is created
5. **Merge**: Configuration is merged to main
6. **Deployment**: Terraform applies the changes

---

## Manual Configuration (Advanced)

If you need to configure multiple catalogs or have complex requirements, you can manually edit:

```hcl
# In catalog.auto.tfvars
catalog_url = "https://your-workspace.databricks.com"
owner       = "catalog-owner"
tag         = "environment-tag"

catalog = {
  catalog_name_1 = {
    group_name = {
      reader = ["group1@company.com", "group2@company.com"]
      editor = ["admin-group@company.com"]
    }
    spn = {
      reader = ["app1@company.com"]
      editor = ["app-admin@company.com"]
    }
  }
  
  catalog_name_2 = {
    group_name = {
      reader = ["another-group@company.com"]
      editor = []
    }
    spn = {
      reader = []
      editor = []
    }
  }
}
```

---

## Support

For issues or questions:
1. Check this guide for common problems
2. Review your GitHub issue comments for validation errors
3. Contact your infrastructure team

---

## Related Documentation

- [Databricks Catalog Documentation](https://docs.databricks.com/en/data-governance/unity-catalog/)
- [Terraform Databricks Provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs)
- [Azure AD Groups Integration](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/auth#service-principal-authentication)
