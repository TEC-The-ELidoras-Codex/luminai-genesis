# .NET Recovery Cheatsheet

Use this guide when you need to restore `dotnet` from a live USB / recovery environment.

Steps (fast):

1. Boot from a live USB (Ubuntu or similar).
2. Open a terminal.
3. Mount your root filesystem to `/mnt/sysroot` (example):

```bash
sudo mkdir -p /mnt/sysroot
# Find your root device (example /dev/mapper/rpool-root)
sudo mount /dev/mapper/rpool-root /mnt/sysroot
# If /home is a separate dataset/partition, mount it as well (example):
# sudo mount /dev/mapper/rpool-userdata-home /mnt/sysroot/home
```

4. Copy the recovery script from your project (if present) or create it under the live environment. If your project is on an external drive or already accessible, use it. Otherwise copy the script contents into a file called `recover_dotnet.sh` and make it executable.

```bash
# From within the repository on the live USB (if present)
cd /path/to/luminai-genesis/scripts
sudo chmod +x recover_dotnet.sh
sudo ./recover_dotnet.sh /mnt/sysroot <username> --copy
```

5. What the script does:
- Copies or symlinks `/home/<username>/.dotnet/dotnet` into `/usr/local/bin/dotnet` on the mounted root (the `--copy` flag forces copying, which is safe if you want `dotnet` available even if `/home` is not mounted at boot).
- Adds the PATH export to `/home/<username>/.bashrc` inside the mounted root if missing.

6. After the script finishes:
- Unmount and reboot into your system normally.

7. Quick verification after boot:

```bash
dotnet --info
```

Notes:
- If your system uses ZFS, ensure you mount the correct dataset(s). Adjust mount points accordingly.
- Copy mode (`--copy`) is recommended if you want `dotnet` available without mounting the home dataset at boot.
- The script must be run with `sudo` in the live environment so it can write to the mounted root.
