# Setting Up the GitHub App

Follow these steps to register MaintainerCopilot as a GitHub App on your account or organization.

---

## Step 1 — Create the GitHub App

1. Go to **GitHub → Settings → Developer settings → GitHub Apps → New GitHub App**  
   (or `https://github.com/settings/apps/new`)

2. Fill in the form:

| Field | Value |
|---|---|
| **GitHub App name** | `MaintainerCopilot` (or any unique name) |
| **Homepage URL** | Your repo URL or `https://example.com` |
| **Webhook URL** | Your server URL + `/webhook` (e.g. `https://your-ngrok-url.ngrok.io/webhook`) |
| **Webhook secret** | A strong random string — copy it to `GITHUB_WEBHOOK_SECRET` in `.env` |

3. Under **Permissions → Repository permissions**, grant:

| Permission | Level |
|---|---|
| Issues | Read & Write |
| Pull requests | Read & Write |
| Contents | Read-only |
| Metadata | Read-only |

4. Under **Subscribe to events**, check:
   - `Issues`
   - `Issue comment`
   - `Pull request`
   - `Push`

5. Under **Where can this GitHub App be installed?**, choose:
   - `Any account` for public use
   - `Only on this account` for private/testing

6. Click **Create GitHub App**.

---

## Step 2 — Download the Private Key

1. On the app page, scroll to **Private keys** and click **Generate a private key**.
2. Save the downloaded `.pem` file as `github_private_key.pem` in the project root.
3. This file is already in `.gitignore` — **never commit it**.

---

## Step 3 — Copy Your App ID

On the app page, note the **App ID** (a number like `12345`).  
Add it to `.env` as `GITHUB_APP_ID=12345`.

---

## Step 4 — Install the App on a Repository

1. On the app page, click **Install App**.
2. Choose your account and select the repository to install on.
3. Click **Install**.

---

## Step 5 — Expose Your Webhook with ngrok (Local Dev)

```bash
# Start with the dev profile to launch ngrok automatically:
docker compose --profile dev up

# The ngrok dashboard is available at http://localhost:4040
# Copy the public HTTPS URL and set it as your webhook URL in the GitHub App settings.
```

---

## Step 6 — Verify

Open an issue on the installed repository. Within a few seconds you should see a triage comment from MaintainerCopilot.

Check logs with:
```bash
docker compose logs -f maintainer-copilot
```
