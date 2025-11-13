import os
import shutil
import subprocess
from flask import Flask, render_template
from flask import request
import string
from flask import request, render_template, redirect, url_for
import docker
import random
import glob

client = docker.from_env()

app = Flask(__name__)


def get_os_family():
    if os.path.exists("/etc/debian_version"):
        return "debian"
    elif os.path.exists("/etc/redhat-release"):
        return "redhat"
    else:
        return "unknown"



def install_package(tool, os_family):
    package_map = {
        "docker": "docker.io" if os_family == "debian" else "docker",
        "pip3": "python3-pip",
        "python3-venv": "python3-venv",
        "docker-compose": None  # We'll handle it manually
    }

    package_name = package_map.get(tool, tool)

    try:
        if os_family == "debian":
            subprocess.run(["sudo", "apt", "update"], check=True)

            if tool == "terraform":
                subprocess.run(["sudo", "apt", "install", "-y", "wget", "gnupg", "software-properties-common", "curl"], check=True)
                subprocess.run([
                    "wget", "-O", "hashicorp.gpg", "https://apt.releases.hashicorp.com/gpg"
                ], check=True)
                subprocess.run([
                    "gpg", "--dearmor", "--output", "hashicorp-archive-keyring.gpg", "hashicorp.gpg"
                ], check=True)
                subprocess.run([
                    "sudo", "mv", "hashicorp-archive-keyring.gpg", "/usr/share/keyrings/hashicorp-archive-keyring.gpg"
                ], check=True)

                codename = subprocess.check_output(["lsb_release", "-cs"], text=True).strip()
                apt_line = (
                    f"deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] "
                    f"https://apt.releases.hashicorp.com {codename} main\n"
                )
                with open("hashicorp.list", "w") as f:
                    f.write(apt_line)
                subprocess.run(["sudo", "mv", "hashicorp.list", "/etc/apt/sources.list.d/hashicorp.list"], check=True)

                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "terraform"], check=True)

            elif tool == "docker-compose":
                subprocess.run(["sudo", "apt", "install", "-y", "docker-compose"], check=True)

            else:
                subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)

        elif os_family == "redhat":
            if tool == "terraform":
                subprocess.run(["sudo", "yum", "install", "-y", "yum-utils"], check=True)
                subprocess.run([
                    "sudo", "yum-config-manager", "--add-repo",
                    "https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo"
                ], check=True)
                subprocess.run(["sudo", "yum", "install", "-y", "terraform"], check=True)

            elif tool == "docker-compose":
                subprocess.run(["sudo", "yum", "install", "-y", "docker-compose"], check=True)

            else:
                subprocess.run(["sudo", "yum", "install", "-y", package_name], check=True)

        else:
            return False, "Unsupported OS"

        return True, None

    except Exception as e:
        return False, str(e)




@app.route("/pre-req")
def prereq():
    tools = ["pip3", "openssl", "docker", "terraform","docker-compose"]
    results = {}
    os_family = get_os_family()

    for tool in tools:
        if shutil.which(tool):
            results[tool] = "✅ Installed"
        else:
            success, error = install_package(tool, os_family)
            if success:
                results[tool] = "❌ Not Found → 🛠️ Installed"
            else:
                results[tool] = f"❌ Not Found → ❌ Error: {error}"



    docker_installed = shutil.which("docker") is not None
    return render_template("prereq.html", results=results, os_family=os_family, docker_installed=docker_installed)












# Check if Portainer is actually installed and running (or exists as a container)
def is_portainer_installed():
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "portainer"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.stdout.strip() in ["true", "false"]
    except Exception:
        return False

# Actually run Portainer
def run_portainer():
    try:
        subprocess.run(["docker", "volume", "create", "portainer_data"], check=True)
        subprocess.run([
            "docker", "run", "-d",
            "-p", "9443:9443", "-p", "9000:9000",
            "--name", "portainer",
            "--restart=always",
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            "-v", "portainer_data:/data",
            "portainer/portainer-ce:latest"
        ], check=True)
        return True, "✅ Portainer installed successfully."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Docker Error: {str(e)}"



# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/install_portainer", methods=["GET", "POST"])
def install_portainer_route():
    installed = is_portainer_installed()
    portainer_url = "https://localhost:9443"
    message = None

    if request.method == "POST":
        if not installed:
            success, message = run_portainer()
            installed = success
        else:
            message = "ℹ️ Portainer is already installed."

    return render_template("portainer.html", installed=installed, message=message, url=portainer_url)




##########################################  metric #############################################################################################


@app.route("/observability")
def observability_info():
    return render_template("observability_info.html")


@app.route("/metrics")
def metrics_landing():
    return render_template("metrics.html")


REPO_URL = "https://github.com/arunvel1988/Prometheus-docker"
REPO_DIR = "Prometheus-docker"





@app.route("/metrics/install")
def install_metrics_stack():
    if not os.path.exists(REPO_DIR):
        subprocess.run(["git", "clone", REPO_URL])
    subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=REPO_DIR)
    return render_template("install_metrics.html")


@app.route("/metrics/delete")
def delete_metrics_stack():
    if os.path.exists(REPO_DIR):
        subprocess.run(["docker-compose", "down"], cwd=REPO_DIR)
    return render_template("delete.html")



@app.route("/metrics/status")
def metrics_status():
    try:
        output = subprocess.check_output([
            "docker", "ps", "--format", "{{.Names}}|{{.Ports}}"
        ]).decode("utf-8").splitlines()

        services = []
        for line in output:
            name, ports = line.split("|", 1)
            exposed_ports = []

            for port_map in ports.split(","):
                port_map = port_map.strip()
                if "->" in port_map and ":" in port_map:
                    host_port = port_map.split("->")[0].split(":")[-1]
                    exposed_ports.append(host_port)

            services.append((name, exposed_ports))
    except subprocess.CalledProcessError:
        services = []

    return render_template("status_metrics.html", services=services)

##########################################  metric #############################################################################################

##### logs###############


@app.route("/logs")
def logs_landing():
    return render_template("logs.html")

@app.route("/logs/loki")
def loki_landing():
    return render_template("loki.html")
    
REPO_URL_LOGS = "https://github.com/arunvel1988/elk-devops-demo"
REPO_DIR_LOGS = "elk-devops-demo"

@app.route("/logs/install")
def install_logs_stack():
    if not os.path.exists(REPO_DIR_LOGS):
        subprocess.run(["git", "clone", REPO_URL_LOGS])
    subprocess.run(["sudo", "chown", "root:root", "./filebeat.yml"], cwd=REPO_DIR_LOGS)
    subprocess.run(["sudo", "chmod", "go-w", "./filebeat.yml"], cwd=REPO_DIR_LOGS)
    subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=REPO_DIR_LOGS)
    return render_template("install_logs.html")

@app.route("/logs/delete")
def delete_logs_stack():
    if os.path.exists(REPO_DIR_LOGS):
        subprocess.run(["docker-compose", "down"], cwd=REPO_DIR_LOGS)
    return render_template("delete_logs.html")

@app.route("/logs/status")
def logs_status():
    try:
        output = subprocess.check_output([
            "docker", "ps", "--format", "{{.Names}}|{{.Ports}}"
        ]).decode("utf-8").splitlines()

        services = []
        for line in output:
            name, ports = line.split("|", 1)
            exposed_ports = []

            for port_map in ports.split(","):
                port_map = port_map.strip()
                if "->" in port_map and ":" in port_map:
                    host_port = port_map.split("->")[0].split(":")[-1]
                    exposed_ports.append(host_port)

            services.append((name, exposed_ports))
    except subprocess.CalledProcessError:
        services = []

    return render_template("status_logs.html", services=services)
 
 ##########################################################################################################
# loki logs ################################################

@app.route("/loki/install")
def install_loki_stack():
    if not os.path.exists(REPO_DIR_LOGS):
        subprocess.run(["git", "clone", REPO_URL_LOGS])
    subprocess.run(["mkdir", "-p", "./loki_data/index"], cwd=REPO_DIR_LOGS)
    subprocess.run(["mkdir", "-p", "./loki_data/cache"], cwd=REPO_DIR_LOGS)
    subprocess.run(["mkdir", "-p", "./loki_data/chunks"], cwd=REPO_DIR_LOGS)
    subprocess.run(["mkdir", "-p", "./loki_data/compactor"], cwd=REPO_DIR_LOGS)
    subprocess.run(["mkdir", "-p", "./loki_data/wal"], cwd=REPO_DIR_LOGS)

    # Change ownership to Loki user (UID 10001)
    subprocess.run(["sudo", "chown", "-R", "10001:10001", "./loki_data"], cwd=REPO_DIR_LOGS)

    # Set permissions
    subprocess.run(["sudo", "chmod", "-R", "775", "./loki_data"], cwd=REPO_DIR_LOGS)

    # Start Loki + Grafana with docker-compose
    subprocess.run(
        ["docker-compose", "-f", "docker-compose-grafana-loki.yml", "up", "-d", "--build"],
        cwd=REPO_DIR_LOGS
    )

    return render_template("install_loki.html")


@app.route("/loki/delete")
def delete_loki_stack():
    if os.path.exists(REPO_DIR_LOGS):
        subprocess.run(
            ["docker-compose", "-f", "docker-compose-grafana-loki.yml", "down", "--remove-orphans"],
            cwd=REPO_DIR_LOGS
        )
    return render_template("delete_loki.html")



@app.route("/loki/status")
def loki_status():
    try:
        output = subprocess.check_output([
            "docker", "ps", "--format", "{{.Names}}|{{.Ports}}"
        ]).decode("utf-8").splitlines()

        services = []
        for line in output:
            name, ports = line.split("|", 1)
            exposed_ports = []

            for port_map in ports.split(","):
                port_map = port_map.strip()
                if "->" in port_map and ":" in port_map:
                    host_port = port_map.split("->")[0].split(":")[-1]
                    exposed_ports.append(host_port)

            services.append((name, exposed_ports))
    except subprocess.CalledProcessError:
        services = []

    return render_template("status_loki.html", services=services)

##########################################logs ####################################################################################
    

##### traces ###############


@app.route("/traces")
def traces_landing():
    return render_template("traces.html")

    
REPO_URL_TRACES = "https://github.com/arunvel1988/observability-jaeger-demo"
REPO_DIR_TRACES = "observability-jaeger-demo"

@app.route("/traces/install")
def install_traces_stack():
    if not os.path.exists(REPO_DIR_TRACES):
        subprocess.run(["git", "clone", REPO_URL_TRACES])

    subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=REPO_DIR_TRACES)
    return render_template("install_traces.html")

@app.route("/traces/delete")
def delete_traces_stack():
    if os.path.exists(REPO_DIR_LOGS):
        subprocess.run(["docker-compose", "down"], cwd=REPO_DIR_TRACES)
    return render_template("delete_traces.html")

@app.route("/traces/status")
def traces_status():
    try:
        output = subprocess.check_output([
            "docker", "ps", "--format", "{{.Names}}|{{.Ports}}"
        ]).decode("utf-8").splitlines()

        services = []
        for line in output:
            name, ports = line.split("|", 1)
            exposed_ports = []

            for port_map in ports.split(","):
                port_map = port_map.strip()
                if "->" in port_map and ":" in port_map:
                    host_port = port_map.split("->")[0].split(":")[-1]
                    exposed_ports.append(host_port)

            services.append((name, exposed_ports))
    except subprocess.CalledProcessError:
        services = []

    return render_template("status_traces.html", services=services)
 
 


##########################################logs ####################################################################################
##################### k8s lgtm ####################################################


@app.route("/k8s")
def k8s_landing():
    return render_template("k8s.html")




# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR_UI = os.path.join(BASE_DIR, "kubernetes/alloy")

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------
def apply_k8s_files(file_range):
    """Apply YAMLs from a numeric range (e.g., 1–6)."""
    subprocess.run(["kubectl", "apply", "-f", f"{REPO_DIR_UI}/1_namespace.yaml"], check=False)
    for i in file_range:
        yaml_pattern = f"{REPO_DIR_UI}/{i}_*.yaml"
        subprocess.run(["bash", "-c", f"kubectl apply -f {yaml_pattern}"], check=False)


def delete_k8s_files(file_range):
    """Delete YAMLs from a numeric range."""
    for i in file_range:
        yaml_pattern = f"{REPO_DIR_UI}/{i}_*.yaml"
        subprocess.run(
            ["bash", "-c", f"kubectl delete -f {yaml_pattern} --ignore-not-found"],
            check=False
        )


def get_k8s_status(namespace="logging"):
    """Return pod and service status."""
    try:
        pods = subprocess.check_output(
            ["kubectl", "get", "pods", "-n", namespace, "-o", "wide"]
        ).decode("utf-8")
        svcs = subprocess.check_output(
            ["kubectl", "get", "svc", "-n", namespace]
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        pods = "Error retrieving pods."
        svcs = "Error retrieving services."
    return pods, svcs


def list_yaml_files():
    """List all YAML files inside kubernetes/alloy."""
    files = sorted(glob.glob(os.path.join(REPO_DIR_UI, "*.yaml")))
    return [os.path.basename(f) for f in files]

# ------------------------------------------------------------
# View & Apply/Delete Individual Files
# ------------------------------------------------------------
@app.route("/k8s/files")
def view_k8s_files():
    files = list_yaml_files()
    return render_template("view_files.html", files=files)


@app.route("/k8s/view", methods=["GET"])
def view_single_file():
    filename = request.args.get("filename")
    if not filename:
        return "No file specified"
    file_path = os.path.join(REPO_DIR_UI, filename)

    if not os.path.exists(file_path):
        return f"<h3>❌ File not found: {filename}</h3><a href='/k8s/files'>⬅️ Back</a>"

    with open(file_path, "r") as f:
        content = f.read()

    return f"""
    <h2>📄 Viewing File: {filename}</h2>
    <pre style='background:#f0f0f0; padding:15px; border-radius:8px; width:90%; margin:auto; overflow:auto;'>
{content}
    </pre>
    <div style='text-align:center; margin-top:20px;'>
        <a href='/k8s/files'>⬅️ Back to File List</a>
    </div>
    """


@app.route("/k8s/apply", methods=["POST"])
def apply_single_file():
    filename = request.form.get("filename")
    if not filename:
        return "No file specified"
    file_path = os.path.join(REPO_DIR_UI, filename)
    output = subprocess.getoutput(f"kubectl apply -f {file_path}")
    return f"<h3>Applied: {filename}</h3><pre>{output}</pre><a href='/k8s/files'>⬅️ Back</a>"

@app.route("/k8s/delete", methods=["POST"])
def delete_single_file():
    filename = request.form.get("filename")
    if not filename:
        return "No file specified"
    file_path = os.path.join(REPO_DIR_UI, filename)
    output = subprocess.getoutput(f"kubectl delete -f {file_path} --ignore-not-found")
    return f"<h3>Deleted: {filename}</h3><pre>{output}</pre><a href='/k8s/files'>⬅️ Back</a>"

# ------------------------------------------------------------
# Stack Management Endpoints
# ------------------------------------------------------------
# --------------- NORMAL LOGS ------------------
@app.route("/k8s/logs/install")
def install_normal_logs():
    apply_k8s_files(range(1, 7))
    return render_template("install_logs_k8s.html")

@app.route("/k8s/logs/delete")
def delete_normal_logs():
    delete_k8s_files(range(1, 7))
    return render_template("delete_logs_k8s.html")

@app.route("/k8s/logs/status")
def status_normal_logs():
    pods, svcs = get_k8s_status()
    return render_template("status_logs_k8s.html", pods=pods, svcs=svcs)

# --------------- OTEL LOGS ------------------
@app.route("/k8s/otel/logs/install")
def install_otel_logs():
    apply_k8s_files(range(7, 11))
    return render_template("install_otel_logs.html")

@app.route("/k8s/otel/logs/delete")
def delete_otel_logs():
    delete_k8s_files(range(7, 11))
    return render_template("delete_otel_logs.html")

@app.route("/k8s/otel/logs/status")
def status_otel_logs():
    pods, svcs = get_k8s_status()
    return render_template("status_otel_logs.html", pods=pods, svcs=svcs)

# --------------- OTEL TRACES ------------------
@app.route("/k8s/otel/traces/install")
def install_otel_traces():
    apply_k8s_files(range(11, 16))
    return render_template("install_otel_traces.html")

@app.route("/k8s/otel/traces/delete")
def delete_otel_traces():
    delete_k8s_files(range(11, 16))
    return render_template("delete_otel_traces.html")

@app.route("/k8s/otel/traces/status")
def status_otel_traces():
    pods, svcs = get_k8s_status()
    return render_template("status_otel_traces.html", pods=pods, svcs=svcs)

# --------------- OTEL LGTM ------------------
@app.route("/k8s/otel/lgtm/install")
def install_otel_lgtm():
    apply_k8s_files(range(16, 21))
    return render_template("install_otel_lgtm.html")

@app.route("/k8s/otel/lgtm/delete")
def delete_otel_lgtm():
    delete_k8s_files(range(16, 21))
    return render_template("delete_otel_lgtm.html")

@app.route("/k8s/otel/lgtm/status")
def status_otel_lgtm():
    pods, svcs = get_k8s_status()
    return render_template("status_otel_lgtm.html", pods=pods, svcs=svcs)








    ##################################### k8s lgtm - end #######################################

##########################################OTEL (OPEN TELEMETRY) ################################################

@app.route("/otel")
def otel_landing():
    return render_template("otel.html")

    
REPO_URL_OTEL = "https://github.com/arunvel1988/opentelemetry-demo"
REPO_DIR_OTEL = "opentelemetry-demo"

@app.route("/otel/install")
def install_otel_stack():
    if not os.path.exists(REPO_DIR_OTEL):
        subprocess.run(["git", "clone", REPO_URL_OTEL])

    subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=REPO_DIR_OTEL)
    return render_template("install_otel.html")

@app.route("/otel/delete")
def delete_otel_stack():
    if os.path.exists(REPO_DIR_OTEL):
        subprocess.run(["docker-compose", "down"], cwd=REPO_DIR_OTEL)
    return render_template("delete_otel.html")

@app.route("/otel/status")
def otel_status():
    # Hardcoded services with their base ports or URLs
    services = [
        ("Web Store", ["8080/"]),
        ("Grafana", ["8080/grafana/"]),
        ("Load Generator UI", ["8080/loadgen/"]),
        ("Jaeger UI", ["8080/jaeger/ui/"]),
        ("Tracetest UI", ["11633/"]),
        ("Flagd Configurator UI", ["8080/feature"]),
    ]
    return render_template("status_otel.html", services=services)

  
 

###################################################################################################################


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
