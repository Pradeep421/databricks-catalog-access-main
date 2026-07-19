#!/bin/bash

# Generate Catalog Template Script
# Creates a new terraform catalog configuration block

set -e

CATALOG_NAME="${1:-}"
OWNER="${2:-}"
TAG="${3:-}"

if [ -z "$CATALOG_NAME" ] || [ -z "$OWNER" ] || [ -z "$TAG" ]; then
    echo "Usage: $0 <catalog_name> <owner> <tag>"
    echo "Example: $0 my_catalog 'owner@company.com' 'dev'"
    exit 1
fi

# Validate catalog name
if ! [[ "$CATALOG_NAME" =~ ^[a-z0-9_]+$ ]]; then
    echo "Error: Catalog name must contain only lowercase letters, numbers, and underscores"
    exit 1
fi

# Generate HCL block
cat << EOF
  $CATALOG_NAME = {
    group_name = {
      reader = [
        # Add reader groups here
        # Example: "team-readers@company.com"
      ]
      editor = [
        # Add editor groups here (optional)
        # Example: "team-editors@company.com"
      ]
    }
    spn = {
      reader = [
        # Add reader SPNs here (optional)
        # Example: "app-service-principal@company.com"
      ]
      editor = [
        # Add editor SPNs here (optional)
        # Example: "app-service-principal-admin@company.com"
      ]
    }
  }
EOF

echo ""
echo "# To add this catalog, append the above block to catalog.auto.tfvars"
echo "# Make sure to populate the reader groups (mandatory) and any optional SPN access."
