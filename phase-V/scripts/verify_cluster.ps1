$ErrorActionPreference = "Continue"

function Write-Info {
    param([string]$Message)
    Write-Output "[INFO] $Message"
}

function Write-Success {
    param([string]$Message)
    Write-Output "[OK] $Message"
}

function Write-Fail {
    param([string]$Message)
    Write-Output "[FAIL] $Message"
}

Write-Output ""
Write-Output "==============================================="
Write-Output "   Phase V Part B - Cluster Verification       "
Write-Output "==============================================="
Write-Output ""

$pass = 0
$fail = 0

# -- 1. Namespace --
Write-Info "Checking namespace..."
$ns = kubectl get namespace todo-app -o jsonpath='{.metadata.name}' 2>$null
if ($ns -eq "todo-app") { Write-Success "Namespace 'todo-app' exists"; $pass++ }
else { Write-Fail "Namespace 'todo-app' not found"; $fail++ }

# -- 2. Dapr System --
Write-Info "Checking Dapr system pods..."
$daprPods = kubectl get pods -n dapr-system --no-headers 2>$null | Measure-Object -Line
$lines = $daprPods.Lines
if ($lines -ge 3) {
    Write-Success "Dapr system pods running ($lines pods)"
    $pass++
} else {
    Write-Fail "Dapr system pods: expected >= 3, got $lines"
    $fail++
}

# -- 3. Dapr Components --
Write-Info "Checking Dapr components..."
$components = @("kafka-pubsub", "statestore", "todo-cron", "kubernetes-secrets")
foreach ($comp in $components) {
    $found = kubectl get component $comp -n todo-app -o jsonpath='{.metadata.name}' 2>$null
    if ($found -eq $comp) {
        Write-Success "Dapr component: $comp"
        $pass++
    } else {
        Write-Fail "Dapr component missing: $comp"
        $fail++
    }
}

# -- 4. Application Pods --
Write-Info "Checking application pods..."
$services = @(
    @{Name="todo-app-backend"; Label="todo-app"},
    @{Name="todo-app-frontend"; Label="todo-app"},
    @{Name="notification-service"; Label="notification-service"},
    @{Name="recurring-task-service"; Label="recurring-task-service"}
)
foreach ($svc in $services) {
    $svcName = $svc.Name
    $appLabel = $svc.Label
    # Try both app and app.kubernetes.io/name selectors
    $pod = kubectl get pods -n todo-app -l app.kubernetes.io/name=$appLabel --no-headers 2>$null | Select-String $svcName
    if (-not $pod) {
        $pod = kubectl get pods -n todo-app -l app=$appLabel --no-headers 2>$null | Select-String $svcName
    }
    
    if ($pod -match "Running") {
        if ($pod -match "2/2") {
            Write-Success "Pod ${svcName}: Running with Dapr sidecar (2/2)"
            $pass++
        } else {
            Write-Info "Pod ${svcName}: Running (sidecar may still be starting)"
            $pass++
        }
    } else {
        Write-Fail "Pod ${svcName}: Not running"
        $fail++
    }
}

# -- 5. Services --
Write-Info "Checking Kubernetes services..."
foreach ($svc in $services) {
    $svcName = $svc.Name
    $svcFound = kubectl get svc $svcName -n todo-app -o jsonpath='{.metadata.name}' 2>$null
    if ($svcFound -eq $svcName) {
        Write-Success "Service: $svcName"
        $pass++
    } else {
        Write-Fail "Service missing: $svcName"
        $fail++
    }
}

# -- 6. Health Endpoints --
Write-Info "Checking health endpoints..."
$healthChecks = @(
    @{Name="todo-app-backend"; Port=8000; Path="/health/ready"},
    @{Name="notification-service"; Port=8000; Path="/health/live"},
    @{Name="recurring-task-service"; Port=8000; Path="/health/live"}
)

foreach ($check in $healthChecks) {
    $cName = $check.Name
    $cPort = $check.Port
    $cPath = $check.Path
    $containerName = $cName
    
    # In values.yaml or defaults, the container name is just 'backend' or 'frontend', etc
    if ($cName -match "backend") { $containerName = "backend" }
    elseif ($cName -match "frontend") { $containerName = "frontend" }
    elseif ($cName -match "notification") { $containerName = "notification-service" }
    elseif ($cName -match "recurring") { $containerName = "recurring-task-service" }

    try {
        $result = kubectl exec -n todo-app deploy/$cName -c $containerName -- curl -s "http://localhost:${cPort}${cPath}" 2>$null
        if ($result -match "ok") {
            Write-Success "Health check ${cName}${cPath}: OK"
            $pass++
        } else {
            Write-Fail "Health check ${cName}${cPath}: unexpected response '$result'"
            $fail++
        }
    } catch {
        Write-Fail "Health check ${cName}${cPath}: failed"
        $fail++
    }
}

# -- 7. Dapr Pub/Sub Test --
Write-Info "Testing Dapr Pub/Sub (publish test event)..."
try {
    $pubResult = kubectl exec -n todo-app deploy/todo-app-backend -c backend -- curl -s -w "%{http_code}" -o /dev/null -X POST "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events" -H "Content-Type: application/json" -d '{\"event_type\":\"test\",\"task_id\":0}' 2>$null
    if ($pubResult -match "2\d\d") {
        Write-Success "Dapr Pub/Sub publish: Success (HTTP $pubResult)"
        $pass++
    } else {
        Write-Fail "Dapr Pub/Sub publish: HTTP $pubResult"
        $fail++
    }
} catch {
    Write-Fail "Dapr Pub/Sub publish: failed"
    $fail++
}

# -- 8. Dapr Service Invocation Test --
Write-Info "Testing Dapr Service Invocation (backend -> backend)..."
try {
    # frontend container doesn't have curl, so we test backend -> backend
    $invokeResult = kubectl exec -n todo-app deploy/todo-app-backend -c backend -- curl -s "http://localhost:3500/v1.0/invoke/todo-app-backend/method/health/live" 2>$null
    if ($invokeResult -match "ok") {
        Write-Success "Dapr Service Invocation: backend -> backend OK"
        $pass++
    } else {
        Write-Fail "Dapr Service Invocation: unexpected response '$invokeResult'"
        $fail++
    }
} catch {
    Write-Fail "Dapr Service Invocation: failed"
    $fail++
}

# -- Summary --
Write-Output ""
Write-Output "-----------------------------------------------"
Write-Output "  Results: $pass passed, $fail failed"
Write-Output "-----------------------------------------------"

if ($fail -eq 0) {
    Write-Output ""
    Write-Success "All Phase V Part B verification checks passed!"
    Write-Output ""
} else {
    Write-Output ""
    Write-Fail "$fail check(s) failed. Review the output above for details."
    Write-Output ""
}
