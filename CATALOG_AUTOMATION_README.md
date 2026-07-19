# Databricks Catalog Automation - Setup Guide

## 🎯 Overview

This automation enables new teams to request and deploy Databricks catalogs with proper access controls through a structured GitHub issue workflow.

## ✨ What This Solution Provides

### 1. **Issue-Based Catalog Requests**
- Teams create an issue using a standardized template
- All required information is captured in one place
- Clear naming conventions and validation rules

### 2. **Automated Validation**
- Catalog name format validation (lowercase, numbers, underscores only)
- Duplicate catalog detection
- Required field verification
- Access group validation

### 3. **Configuration Generation**
- Automatic Terraform configuration generation
- Proper HCL syntax with correct structure
- Support for both group-based and service principal access

### 4. **GitOps Workflow**
- Changes tracked in Git
- Pull request based approvals
- Full audit trail of all catalog requests
- Easy rollback if needed

---

## 📁 Files Created

### In `databricks-catalog-access-submodule`

```
.github/ISSUE_TEMPLATE/
└── new-catalog-request.md          # GitHub issue template
```

**Purpose**: Provides a standardized form for teams to request new catalogs with guided fields and validation instructions.

### In `databricks-catalog-access-main`

```
.github/workflows/
└── process-catalog-request.yml     # GitHub Actions workflow

scripts/
├── validate_catalog.py             # Python validation script
└── generate_catalog_template.sh    # Shell template generator

CATALOG_REQUEST_GUIDE.md           # Comprehensive user guide
```

**Purpose**: 
- Workflow automates the entire validation and processing pipeline
- Scripts provide reusable validation and generation utilities
- Guide helps teams understand the process

---

## 🚀 How It Works

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Team Creates Issue (Issues → New Issue → Catalog Request)│
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. GitHub Actions Workflow Triggered                         │
│    - Parses issue body                                       │
│    - Validates all fields                                    │
│    - Checks for duplicates                                   │
└────────────┬────────────────────────────────────────────────┘
             │
        ┌────┴────┐
        │          │
   ✘ FAILED   ✅ VALID
        │          │
        ↓          ↓
   Add Error   Check for
   Labels &   Duplicates
   Comment
        │          │
        │     ┌────┴────┐
        │     │          │
        │  DUPLICATE  UNIQUE
        │     │          │
        │     ↓          ↓
        │  Add Warning  Generate
        │  Comment      TF Config
        │     │          │
        └─────┴──────────┴──────→ Comment with Generated Config
                                  Add 'validated' Label
```

---

## 📋 Field Requirements

### Required (Mandatory)
| Field | Type | Example |
|-------|------|----------|
| Catalog Name | lowercase_letters_numbers_underscores | `data_team_prod` |
| Owner | email/principal | `owner@company.com` |
| Tag | dev/staging/prod | `prod` |
| Reader Groups | list (min 1) | `["team-readers@company.com"]` |

### Optional
| Field | Type | Example |
|-------|------|----------|
| Editor Groups | list | `["team-editors@company.com"]` |
| SPN Readers | list | `["app@company.com"]` |
| SPN Editors | list | `["app-admin@company.com"]` |

---

## 🔍 Naming Conventions

### Catalog Names
✅ **VALID**
- `data_team_catalog`
- `analytics_prod_2024`
- `ml_team_dev`
- `proj123_staging`

❌ **INVALID**
- `DataTeam` (uppercase not allowed)
- `data-team` (hyphens not allowed)
- `data team` (spaces not allowed)
- `dt` (too short, min 3 chars)

### Access Levels

**Reader** - `USE_CATALOG`
- View catalogs and objects
- Cannot create or modify

**Editor** - `USE_CATALOG`, `CREATE_SCHEMA`, `CREATE_VOLUME`
- View, create, and modify
- Full administrative access

---

## 💻 Usage Example

### Scenario: Data Team Requests Prod Catalog

**Team fills out issue:**
```markdown
Catalog Name: data_team_prod
Owner: data-lead@company.com
Tag: prod

Reader Groups:
- data-readers@company.com

Editor Groups:
- data-engineers@company.com

SPN Readers:
- data-pipeline@company.com
```

**Workflow automatically:**
1. ✅ Validates catalog name format
2. ✅ Checks catalog doesn't already exist
3. ✅ Verifies required fields
4. 📋 Generates Terraform config
5. 💬 Comments with generated config
6. 🏷️ Adds "validated" label

**Generated Configuration:**
```hcl
  data_team_prod = {
    group_name = {
      reader = ["data-readers@company.com"]
      editor = ["data-engineers@company.com"]
    }
    spn = {
      reader = ["data-pipeline@company.com"]
      editor = []
    }
  }
```

---

## 🛠️ Manual Integration Steps

### For Administrators

1. **Merge generated config** into `catalog.auto.tfvars`:
   ```hcl
   catalog = {
     # ... existing catalogs ...
     
     data_team_prod = {
       group_name = {
         reader = ["data-readers@company.com"]
         editor = ["data-engineers@company.com"]
       }
       spn = {
         reader = ["data-pipeline@company.com"]
       }
     }
   }
   ```

2. **Run Terraform validation**:
   ```bash
   terraform plan
   terraform apply
   ```

3. **Update issue** - Mark as complete with PR link

---

## 🔧 Validation Scripts

### Python Validator

**Location**: `scripts/validate_catalog.py`

**Usage**:
```bash
python3 scripts/validate_catalog.py '{
  "catalog_name": "my_catalog",
  "owner": "owner@company.com",
  "tag": "dev",
  "reader_groups": ["readers@company.com"],
  "editor_groups": [],
  "existing_catalogs": ["other_catalog"]
}'
```

**Output**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

### Template Generator

**Location**: `scripts/generate_catalog_template.sh`

**Usage**:
```bash
./scripts/generate_catalog_template.sh my_catalog owner@company.com dev
```

**Output**: HCL template ready to customize

---

## 🎯 Automation Features

### 1. **Issue Label Management**
- `catalog-request` - Initial request label
- `validation-failed` - Validation errors found
- `validated` - Passed validation
- `duplicate` - Catalog name already exists

### 2. **Automatic Comments**
- ✘ Validation errors with fixes needed
- ⚠️ Duplicate catalog warnings
- ✅ Success confirmation
- 📋 Generated Terraform configuration

### 3. **Error Detection**
- Invalid catalog name format
- Missing required fields
- Duplicate catalog names
- Empty reader groups
- Invalid environment tags

---

## 📊 Current Catalog Structure

Based on your existing configuration:

```hcl
catalog_url = ""              # Databricks workspace URL
owner       = "dev_owner"      # Default catalog owner
tag         = ""               # Environment tag

catalog = {
  ad_catalog = {
    group_name = {
      reader = ["ad_readr_group_dev"]
      editor = ["ad_editr_group_dev"]
    }
    spn = {
      reader = ["dev.user1", "dev.user2"]
    }
  }
  
  ad_catalog_backup = {
    group_name = {
      reader = ["ad_readr_group_dev"]
      editor = ["ad_editr_group_dev"]
    }
    spn = {
      reader = ["dev.user1", "dev.user2"]
    }
  }
}
```

**New catalogs will be added to this structure** following the same pattern.

---

## 🚨 Common Issues & Fixes

### Issue: "Catalog name must contain only lowercase letters"
**Fix**: Remove uppercase letters, hyphens, and spaces
- ❌ `DataTeam` → ✅ `data_team`
- ❌ `data-team` → ✅ `data_team`

### Issue: "Catalog already exists"
**Fix**: Use a unique name or verify with team lead
- Check existing catalogs in configuration
- Choose a different catalog name

### Issue: "At least one reader group required"
**Fix**: Add minimum one reader group
- Reader groups are mandatory
- At least one Azure AD group must have read access

---

## 🔐 Access Control Logic

The system maps GitHub issue groups to Databricks grants:

```
Group/SPN in Issue → Terraform Variable → Databricks Grant
    ↓
reader_groups[0] → group_name.reader[0] → USE_CATALOG
    ↓
editor_groups[0] → group_name.editor[0] → USE_CATALOG + CREATE_SCHEMA + CREATE_VOLUME
    ↓
spn_readers[0] → spn.reader[0] → USE_CATALOG (SPN)
```

---

## 📚 Directory Structure

```
databricks-catalog-access-main/
├── .github/
│   └── workflows/
│       └── process-catalog-request.yml    # Main automation
├── scripts/
│   ├── validate_catalog.py                # Validation logic
│   └── generate_catalog_template.sh       # Template generation
├── main.tf                                 # Terraform resources
├── variable.tf                             # Variable definitions
├── provider.tf                             # Databricks provider config
└── CATALOG_REQUEST_GUIDE.md                # User documentation

databricks-catalog-access-submodule/
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── new-catalog-request.md         # Issue template
├── catalog.auto.tfvars                    # Catalog configurations (source)
├── main.tf                                 # Module reference
├── variable.tf                             # Variables
└── provider.tf                             # Provider config
```

---

## ✅ Workflow Checklist

- [x] Issue template created
- [x] GitHub Actions workflow implemented
- [x] Catalog validation script written
- [x] Template generation script created
- [x] Comprehensive documentation provided
- [x] Error handling and duplicate detection
- [x] Automatic comment generation
- [x] Label management

---

## 🎓 Next Steps

1. **For Teams**: Go to Issues → New Issue → Select "New Catalog Request"
2. **For Admins**: Monitor validated issues and merge configs to `catalog.auto.tfvars`
3. **For DevOps**: Run `terraform plan` and `terraform apply` when ready

---

## 📖 Additional Resources

- **[CATALOG_REQUEST_GUIDE.md](CATALOG_REQUEST_GUIDE.md)** - Detailed user guide
- **[Databricks Documentation](https://docs.databricks.com/en/data-governance/unity-catalog/)** - Official docs
- **[Terraform Provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs)** - Terraform reference

---

**Created**: 2026-07-18  
**Version**: 1.0  
**Status**: ✅ Ready for Production
