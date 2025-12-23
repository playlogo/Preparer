```bash
sudo nano /etc/udev/rules.d/99-devmem.rules
KERNEL=="mem", MODE="0777"
sudo udevadm control --reload-rules
sudo udevadm trigger
```

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/worker.service
systemctl --user daemon-reload
systemctl --user enable worker.service
systemctl --user start worker.service

systemctl --user status worker.service
journalctl --user -u worker.service

```
