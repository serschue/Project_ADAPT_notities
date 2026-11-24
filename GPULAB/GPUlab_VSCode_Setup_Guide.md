# GPUlab + VS Code Remote SSH + Jupyter: setup and reconnect guide

This guide documents the configuration that worked on my Linux laptop to access an imec iLab.t GPUlab job through the bastion host, then open notebooks and project data in VS Code.

> **Important:** The GPUlab job ID, container, hostname and SSH port may change when a job is restarted or replaced. Never upload or commit the `.pem` certificate to Git.

## A. Quick reconnect (next time)

1. **Make sure the GPUlab job is running.** On the local laptop:

   ```bash
   source ~/.venvs/gpulab/bin/activate  # only if CLI was installed in this venv
   gpulab-cli --cert ~/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem jobs
   ```

   If you configured `GPULAB_CERT`, `gpulab-cli jobs` may suffice.

2. **Check the current SSH host aliases:**

   ```bash
   grep '^Host ' ~/.ssh/gpulab_hosts_config
   ```

   Previously the working alias was `gpulab-c23f47d3-proxy`; **use the alias for the currently running job**. A new job may have a different alias.

3. **Check the certificate paths** if the CLI regenerated `~/.ssh/gpulab_hosts_config`. Both the `IdentityFile` and the `-i` argument inside `ProxyCommand` must point to the real certificate location, preferably an absolute path:

   ```text
   /home/sarah/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem
   ```

4. **Optional: test SSH from the laptop:**

   ```bash
   ssh gpulab-c23f47d3-proxy  # replace with current alias
   ```

   Enter the PEM key passphrase if prompted. A successful connection gives a remote prompt similar to `root@<container-id>:~#`. Type `exit` to return to your laptop.

5. **Connect in VS Code:** Open VS Code → `Ctrl+Shift+P` → **Remote-SSH: Connect to Host...** → choose the current `gpulab-...-proxy` alias. Enter your certificate passphrase when prompted.

6. **Open your project and notebook:** **File → Open Folder...** → your project directory on GPUlab → open the `.ipynb` file → **Select Kernel** and choose the Python environment containing your packages. The Python and Jupyter extensions should be installed in the remote VS Code environment.

If the existing job is still running and the SSH config is intact, steps 1, 5 and 6 are usually enough.

## B. One-time setup on a new Linux laptop

### 1. Install GPUlab CLI

Install Python 3 and create a dedicated virtual environment:

```bash
python3 -m venv ~/.venvs/gpulab
source ~/.venvs/gpulab/bin/activate
pip install imecilabt-gpulab-cli
gpulab-cli --help
```

### 2. Download and protect the login certificate

Download your login certificate (`.pem`) from your imec iLab.t account and store it locally:

```bash
mkdir -p ~/.ssh
# Replace SOURCE with the actual downloaded file path:
cp 'SOURCE/login_ilabt_imec_be_serschue@ugent.be.pem' ~/.ssh/
chmod 700 ~/.ssh
chmod 600 ~/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem
```

The `.pem` file is sensitive: keep it private and do not put it in your project directory or a repository.

### 3. Confirm GPUlab CLI authentication

```bash
gpulab-cli --cert ~/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem jobs
```

This lists jobs. Start a GPUlab job through your usual GPUlab workflow if none is running.

### 4. Include the GPUlab SSH hosts file

The CLI may generate `~/.ssh/gpulab_hosts_config`. Check it:

```bash
ls -l ~/.ssh/gpulab_hosts_config
cat ~/.ssh/gpulab_hosts_config
```

Ensure `~/.ssh/config` includes the file:

```sshconfig
Include ~/.ssh/gpulab_hosts_config
```

If the file has not been generated, consult the GPUlab CLI documentation for your installed version; do not guess the job host or port.

### 5. Fix certificate paths in the generated SSH configuration

In the working setup, the direct alias and proxy alias looked approximately like this (host and port are **examples from one specific job**):

```sshconfig
Host gpulab-c23f47d3
    HostName n053-02.wall1.ilabt.imec.be
    Port 5005
    User root
    IdentityFile /home/sarah/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem
    IdentitiesOnly yes

Host gpulab-c23f47d3-proxy
    HostName n053-02.wall1.ilabt.imec.be
    Port 5005
    User root
    ProxyCommand ssh -i /home/sarah/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem -o Port=22 fffserschue@bastion.ilabt.imec.be -W %h:%p
    IdentityFile /home/sarah/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem
    IdentitiesOnly yes
```

**Do not replace the job-specific hostname, port, user or alias with these example values.** Retain those values from your own generated configuration. The critical fix was changing both certificate references to absolute paths, especially the `-i` path inside `ProxyCommand` (which otherwise looked in the current directory).

Edit with:

```bash
nano ~/.ssh/gpulab_hosts_config
```

The CLI can regenerate this file, so you may need to reapply the certificate-path fix after creating new jobs.

### 6. Test the proxy connection

```bash
ssh gpulab-c23f47d3-proxy  # replace with the current proxy alias
```

On first connection, SSH may ask you to trust the bastion and compute-node host keys. **Verify their fingerprints against an official trusted source or administrator before accepting.** You may be prompted twice for the certificate passphrase (bastion and job).

A prompt like `root@3e3efb1d0b19:~#` indicates you reached the GPUlab container. Type `exit` to disconnect.

### 7. Configure VS Code

1. Install VS Code locally.
2. Install the Microsoft **Remote - SSH** extension.
3. Use `Ctrl+Shift+P` → **Remote-SSH: Connect to Host...** → select the current `gpulab-...-proxy` alias.
4. Once connected, install the Microsoft **Python** and **Jupyter** extensions on the remote side if prompted.
5. Choose **File → Open Folder...** and open the project directory containing the notebooks and data.
6. Open the `.ipynb` notebook and select the correct remote Python kernel.

If no usable kernel exists, and your job environment permits creating a venv:

```bash
python3 -m venv ~/jupyter-env
source ~/jupyter-env/bin/activate
python -m pip install ipykernel jupyter numpy pandas matplotlib
python -m ipykernel install --user --name gpulab-env --display-name 'Python (GPUlab)'
```

Install any other project-specific packages in that environment. Environments created only inside an ephemeral container may disappear when the job ends.

## C. Find the notebook and data on GPUlab

In the **remote** VS Code terminal:

```bash
pwd
ls -lah
find / -name '*.ipynb' 2>/dev/null
```

Open the directory containing the notebook with **File → Open Folder...**. Inside the notebook, check its current working directory:

```python
import os
print(os.getcwd())
print(os.listdir('.'))
```

Example of loading a file from the project directory:

```python
import pandas as pd
df = pd.read_csv('data.csv')
display(df.head())
```

JupyterHub and GPUlab containers may not always share the same mounted storage. If a notebook or dataset is missing, confirm which project directory is mounted into the current job before moving files.

## D. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `Network is unreachable` for `n053-02.wall1...:5005` | Direct compute-node access is unavailable | Use the `gpulab-...-proxy` SSH alias instead of the direct alias. |
| `Identity file ... not accessible` | Relative or incorrect certificate path | Fix both `IdentityFile` and the `ProxyCommand ssh -i` path to the absolute `.pem` path. |
| `Permission denied (publickey)` on bastion | Missing, wrong or inaccessible key (or account issue) | Check the `.pem` file path, permissions, username and certificate validity. |
| SSH asks for passphrase twice | Authentication to bastion and container | This can be normal. |
| Old SSH alias stops working | Job was replaced, stopped or SSH config regenerated | Run `gpulab-cli ... jobs`, inspect current aliases, and fix regenerated key paths. |
| VS Code cannot install its server | Remote container environment or SSH compatibility issue | Inspect **Remote - SSH** output; confirm ordinary SSH works first. |
| Notebook opens but imports fail | Wrong kernel or missing packages | Select the correct remote Python environment and install dependencies there. |
| Notebook cannot find CSV/data | Wrong working directory or unmounted storage | Inspect `os.getcwd()`, `ls`, and the actual mounted project directory. |

## E. Useful commands

```bash
# LOCAL: list GPUlab jobs
gpulab-cli --cert ~/.ssh/login_ilabt_imec_be_serschue@ugent.be.pem jobs

# LOCAL: list configured SSH aliases
grep '^Host ' ~/.ssh/gpulab_hosts_config

# LOCAL: connect to the job through bastion
ssh gpulab-c23f47d3-proxy  # use the CURRENT alias

# REMOTE: see your current folder and its files
pwd
ls -lah

# REMOTE: disconnect
exit
```

**Reminder:** SSH access and VS Code are tied to the currently running GPUlab job. Your project data persists only if it is stored on persistent/shared storage, not merely in the container's temporary filesystemggpyu
