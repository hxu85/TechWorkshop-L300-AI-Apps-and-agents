# GitHub Actions Deployment Setup

This guide explains how to configure the GitHub Actions workflow to deploy your application to Azure Container Registry (ACR).

## Prerequisites

1. An Azure Container Registry (ACR) instance
2. Admin access to your GitHub repository to configure secrets
3. Service Principal or ACR admin credentials for authentication

## Required GitHub Secrets

You need to configure the following secrets in your GitHub repository:

### 1. `ACR_USERNAME`
Your Azure Container Registry username (service principal ID or admin username)

### 2. `ACR_PASSWORD`
Your Azure Container Registry password (service principal secret or admin password)

### 3. `ENV`
The complete contents of your `.env` file. This will be securely injected into the Docker image during build.

## Setup Instructions

### Step 1: Get ACR Credentials

**Option A: Using Admin Account (Quick Setup)**
```bash
# Enable admin account (if not already enabled)
az acr update --name <your-acr-name> --admin-enabled true

# Get credentials
az acr credential show --name <your-acr-name>
```

**Option B: Using Service Principal (Recommended for Production)**
```bash
# Create service principal with push access
az ad sp create-for-rbac \
  --name "github-actions-acr-push" \
  --role "AcrPush" \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ContainerRegistry/registries/<acr-name>

# Output will contain appId (username) and password (password)
```

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

   - **Name:** `ACR_USERNAME`  
     **Value:** Your ACR admin username or service principal app ID

   - **Name:** `ACR_PASSWORD`  
     **Value:** Your ACR admin password or service principal password

   - **Name:** `ENV`  
     **Value:** Complete contents of your `.env` file (copy/paste all lines)

### Step 3: Update Workflow Configuration

Edit `.github/workflows/deploy-to-acr.yml` and update:

```yaml
env:
  REGISTRY_NAME: your-registry-name  # Replace with your ACR name (without .azurecr.io)
  IMAGE_NAME: chat-app                # Optionally customize the image name
```

**Example:**
```yaml
env:
  REGISTRY_NAME: mycompanyacr
  IMAGE_NAME: shopping-assistant
```

### Step 4: Test the Workflow

1. Commit and push your changes to the `main` branch:
   ```bash
   git add .github/workflows/deploy-to-acr.yml
   git commit -m "Add ACR deployment workflow"
   git push origin main
   ```

2. Monitor the workflow:
   - Go to **Actions** tab in your GitHub repository
   - Watch the "Deploy to Azure Container Registry" workflow run
   - Check for any errors in the logs

### Step 5: Verify Deployment

After successful workflow completion:

```bash
# List images in your ACR
az acr repository list --name <your-acr-name> --output table

# Show tags for your image
az acr repository show-tags --name <your-acr-name> --repository chat-app --output table
```

You should see two tags:
- `latest` - Always points to the most recent build
- `<commit-sha>` - Specific version tied to the git commit

## Security Notes

✅ **Protected:**
- `.env` file is in `.gitignore` and will never be committed
- GitHub secrets are encrypted and only accessible during workflow execution
- `.env` file is created temporarily during build and cleaned up immediately after

❌ **Never do this:**
- Commit `.env` files to the repository
- Hardcode secrets in the workflow file
- Share your GitHub secrets or ACR credentials publicly

## Workflow Triggers

The workflow runs automatically when:
- Code is pushed to the `main` branch
- Files in the `src/` directory are modified
- The workflow file itself is updated

## Manual Trigger (Optional)

To enable manual workflow runs, add this to the workflow:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'src/**'
  workflow_dispatch:  # Add this line
```

Then you can manually trigger from the Actions tab.

## Troubleshooting

### Authentication Failed
- Verify `ACR_USERNAME` and `ACR_PASSWORD` secrets are correct
- Ensure service principal has `AcrPush` role
- Check if ACR admin account is enabled (if using admin credentials)

### Build Failed
- Check Dockerfile syntax in `src/Dockerfile`
- Verify all required files are present in `src/` directory
- Review build logs in GitHub Actions

### .env Issues
- Ensure `ENV` secret contains complete `.env` file contents
- Verify format: `KEY=value` with one entry per line
- Check for special characters that might need escaping

## Additional Resources

- [Azure Container Registry Documentation](https://docs.microsoft.com/azure/container-registry/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Docker Build Documentation](https://docs.docker.com/engine/reference/commandline/build/)
