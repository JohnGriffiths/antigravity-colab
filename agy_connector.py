import os
from google.colab import drive

def _common_ssh_setup(persist_dir, public_key):
    # 1. MOUNT & PERSISTENCE
    drive.mount('/content/drive')

    os.makedirs(f"{persist_dir}/antigravity", exist_ok=True)
    os.makedirs(f"{persist_dir}/gemini", exist_ok=True)
    os.makedirs(f"{persist_dir}/ssh", exist_ok=True)

    # Symlink hidden folders so they persist across VM resets
    # Using os.system() for shell commands as they are executed in the Colab environment
    os.system(f"rm -rf ~/.antigravity ~/.gemini ~/.ssh")
    os.system(f"ln -s {persist_dir}/antigravity ~/.antigravity")
    os.system(f"ln -s {persist_dir}/gemini ~/.gemini")
    os.system(f"ln -s {persist_dir}/ssh ~/.ssh")

    # 2. SSH SERVER & KEY SETUP
    with open(f"{persist_dir}/ssh/authorized_keys", "w") as f:
        f.write(public_key)

    os.system("apt-get update && apt-get install -y openssh-server")
    os.system("mkdir -p /var/run/sshd")
    os.system(f"chmod 700 {persist_dir}/ssh")
    os.system(f"chmod 600 {persist_dir}/ssh/authorized_keys")
    os.system("sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config")
    os.system("service ssh start")

    print("Common SSH setup completed.")

def connect_cloudflare(persist_dir, public_key, password='password', verbose=False):
    from colab_ssh import launch_ssh_cloudflared # Import moved inside function
    _common_ssh_setup(persist_dir, public_key)
    print("\n🚀 Launching Cloudflare tunnel...")
    launch_ssh_cloudflared(password=password, verbose=verbose)
    print("✅ Cloudflare tunnel launched. You can now connect via SSH.")

def connect_ngrok(persist_dir, public_key, ngrok_token, password='password', verbose=False):
    from colab_ssh import launch_ssh_ngrok # Import moved inside function
    _common_ssh_setup(persist_dir, public_key)
    print("\n🚀 Launching Ngrok tunnel...")
    launch_ssh_ngrok(ngrok_token=ngrok_token, password=password, verbose=verbose)
    print("✅ Ngrok tunnel launched. You can now connect via SSH.")
