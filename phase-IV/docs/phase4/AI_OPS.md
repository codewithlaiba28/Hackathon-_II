# Phase 4: AI Ops & Cloud Native Intelligence

This document fulfills the **AI Ops** requirements for Hackathon II, Phase 4. It covers the setup and usage of **Docker AI (Gordon)**, **kubectl-ai**, and **kagent**.

## 1. Docker AI (Gordon)
**Requirement:** Use Docker AI Agent for intelligent Docker operations.

### Setup
1.  **Update Docker Desktop**: Ensure you are running Docker Desktop version **4.33** or later.
2.  **Enable Beta Features**:
    - Go to **Settings** > **Features in development** (or Beta features).
    - Toggle **Docker AI** / **Gordon** to ON.
    - Restart Docker Desktop if prompted.
3.  **Access**: Open the Docker Dashboard. You should see a generic "AI" or "Gordon" icon/chat interface, usually in the bottom right or a dedicated tab.

### Usage Examples
You can ask Gordon questions about your containers directly in the Docker Dashboard:

> "How do I build the backend image using the Dockerfile in the current directory?"
> "Why is my todo-backend container crashing?"
> "Explain the multi-stage build in my frontend Dockerfile."

**Hackathon Evidence**:
Take a screenshot of a conversation with Gordon optimizing your Dockerfile or debugging a container and save it to `docs/phase4/evidence/gordon_chat.png`.

---

## 2. kubectl-ai
**Requirement:** Use `kubectl-ai` for AI-assisted Kubernetes operations.
`kubectl-ai` is a kubectl plugin that generates and applies Kubernetes manifests using OpenAI GPT models.

### Installation
**Prerequisites**: You must have an `OPENAI_API_KEY` environment variable set.

**Install via Krew (Recommended)**:
1.  Install [Krew](https://krew.sigs.k8s.io/) (Plugin manager for kubectl).
2.  Run:
    ```bash
    kubectl krew install ai
    ```

**Manual Installation (Windows)**:
1.  Download the latest release binary from the [kubectl-ai GitHub repo](https://github.com/sozercan/kubectl-ai).
2.  Rename it to `kubectl-ai.exe`.
3.  Add it to your system PATH.

### Usage
```bash
# Generate a deployment
kubectl ai "create a deployment for nginx with 3 replicas"

# Apply directly (use with caution)
kubectl ai "scale the todo-backend deployment to 5 replicas" --apply
```

---

## 3. Kagent
**Requirement:** Use `kagent` for advanced agentic Kubernetes operations.
`kagent` acts as an autonomous agent that can investigate cluster issues.

### Installation
(Refer to the specific `kagent` repository provided in the Hackathon resources, as multiple tools share similar names. Assuming standard open-source agent.)

Typically installed as a CLI tool or a cluster operator.

### Usage Scenario
```bash
# Analyze cluster health
kagent "diagnose why my frontend pod is restarting"

# Optimize resources
kagent "suggest resource limits for the backend deployment based on usage"
```

---

## 4. Verification
To verify that these tools are integrated into your workflow:
1.  **Gordon**: Use it to explain `backend/Dockerfile`.
2.  **kubectl-ai**: Use it to generate a test pod: `kubectl ai "run a busybox pod and keep it running"`.
3.  **Logs**: Keep a log of your prompts and the AI's responses in `docs/phase4/ai_ops_logs.md`.
