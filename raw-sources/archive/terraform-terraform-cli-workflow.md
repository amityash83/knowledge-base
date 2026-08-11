---
title: Terraform CLI Workflow
tags: [terraform, cli, snippets, iac]
domain: terraform
difficulty: beginner
created: 2026-04-09
updated: 2026-04-09
---

# Terraform CLI Workflow

## Summary
This snippet note contains the standard Terraform command sequence used to format, initialize, validate, plan, and apply infrastructure changes in a controlled way.

## Concepts
- The Terraform CLI workflow should be repeatable and reviewable.
- Validation and planning reduce change risk before apply.
- Snippets help maintain team consistency across environments.

## Commands / Code
```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform show
```

## Architecture / Flow
1. Normalize formatting.
2. Initialize the working directory.
3. Validate configuration quality.
4. Generate and review a plan file.
5. Apply only the approved plan.

## Use Cases
- Daily infrastructure changes.
- Team onboarding into Terraform workflows.
- Repeatable execution in CI or local environments.

## Related Topics
- [[terraform-infrastructure-workflows]]
- [[devops-lab-platform-foundation]]
- [[platform-reference-map]]

## Tags
#terraform #cli #snippets #iac
