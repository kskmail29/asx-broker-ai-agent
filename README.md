# asx-broker-ai-agent
To create the 

README.md

 file with the provided content and push it to your repository, follow these steps:

1. Create the 

README.md

 file in the root of your repository.
2. Add the provided content to the file.
3. Commit and push the changes to your GitHub repository.

Here are the commands to execute in your terminal:

```bash
# Navigate to the repository
cd /Users/shyamkompally/Myproject/asx-broker-ai-agent

# Create the README.md file
cat > README.md << 'EOF'
# ASX Alpha Broker: Full Setup Handbook

This repository contains a professional ASX Stock Analysis Agent. 
- **Frontend:** Streamlit (Hosted on Streamlit Cloud)
- **Backend:** Agno Agent (Hosted on Oracle Cloud Infrastructure)

---

## Phase 1: Oracle Cloud Infrastructure (OCI) Setup
Before running any code, the "Virtual Door" to the server must be opened.

1. **Ingress Rules:**
   - Go to **Networking** > **Virtual Cloud Networks** > **Your VCN** > **Security Lists**.
   - Add an **Ingress Rule**:
     - **Source CIDR:** `0.0.0.0/0`
     - **IP Protocol:** `TCP`
     - **Destination Port Range:** `8000`
2. **Internal Firewall:**
   Open the port inside the Ubuntu OS by running:
   ```bash
   sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
   sudo netfilter-persistent save
   ```

---

## Phase 2: Server Environment Preparation
Connect to your Oracle instance via SSH and run these commands to prepare the Python environment.

1. **Install System Dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv python-is-python3
   ```
2. **Create a Virtual Environment:**
   (Required to avoid the "externally-managed-environment" error)
   ```bash
   cd ~/asx-broker-ai-agent
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Python Libraries:**
   ```bash
   pip install agno yfinance anthropic "fastapi[standard]" uvicorn
   ```

---

## Phase 3: Running the Agent (broker.py)
The `broker.py` file acts as the API server.

1. **Agent Configuration:**
   Ensure the `Agent` ID in `broker.py` matches the `AGENT_ID` in `app.py`:
   ```python
   agent = Agent(id="asx-alpha-broker", ...)
   ```
2. **Run 24/7 with PM2:**
   To keep the agent running even after you disconnect your terminal:
   ```bash
   # Install PM2
   sudo apt install -y nodejs npm
   sudo npm install -g pm2

   # Start the broker
   pm2 start "python broker.py" --name asx-broker
   
   # Ensure it starts on reboot
   pm2 save
   pm2 startup
   ```

---

## Phase 4: Frontend Deployment (Streamlit)
1. Push your `app.py` and `requirements.txt` to GitHub.
2. Connect your repository to **Streamlit Cloud**.
3. **Important:** Add your `ANTHROPIC

_API

_KEY` to the Streamlit "Secrets" settings.

---

## Troubleshooting Handbook

### 1. "404 Not Found" in Streamlit
- **Cause:** Mismatch between the Agent ID requested by Streamlit and the ID served by Oracle.
- **Fix:** Check `broker.py` has `id="asx-alpha-broker"` and `app.py` has `AGENT_ID = "asx-alpha-broker"`.

### 2. "ModuleNotFoundError: No module named 'agno' (or fastapi)"
- **Cause:** Running the script outside the virtual environment.
- **Fix:** Always run `source venv/bin/activate` before starting the script, or ensure PM2 is pointing to the version of Python inside the `venv` folder.

### 3. "Connection Timeout"
- **Cause:** Oracle Ingress rules or `iptables` are blocking Port 8000.
- **Fix:** Re-run the `iptables` commands in Phase 1 and verify the Security List in the Oracle Console.

### 4. "Externally Managed Environment" Error
- **Cause:** Modern Ubuntu (23.04+) prevents global `pip` installs to protect the OS.
- **Fix:** You **must** use a Virtual Environment (`python -m venv venv`) as detailed in Phase 2.

---

## Useful Commands for Maintenance
- **Check Agent Status:** `pm2 status`
- **View Live Logs:** `pm2 logs asx-broker`
- **Restart Agent:** `pm2 restart asx-broker`
- **Check if Port 8000 is open:** `sudo netstat -tulpn | grep 8000`
EOF

# Stage the file
git add README.md

# Commit the changes
git commit -m "Add README.md with full setup handbook"

# Push to the repository
git push origin main
```

This will create the 

README.md

 file with the provided content and push it to your repository.
