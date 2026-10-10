# Pocket DevStation waker (MicroPython, ESP32-S3).
# Waits for /wake from you on Telegram, then sends the Wake-on-LAN
# magic packet to the laptop from inside the home network.
import json
import socket
import ssl
import time

import machine
import network
import ntptime

import config

HOST = "api.telegram.org"
POLL_SECONDS = 25  # how long Telegram holds each request open waiting for a message


def magic_packet(mac):
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    return b"\xff" * 6 + mac_bytes * 16


def wake_laptop():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for _ in range(3):  # a single UDP packet can get lost; repeats are harmless
        s.sendto(magic_packet(config.LAPTOP_MAC), ("255.255.255.255", 9))
        time.sleep_ms(100)
    s.close()


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        for _ in range(40):  # wait up to 20 seconds
            if wlan.isconnected():
                break
            time.sleep_ms(500)
    return wlan.isconnected()


def make_tls():
    # Only talk to the real Telegram: its certificate must chain to ca.der.
    # If Telegram ever changes certificate provider, this board goes quiet;
    # re-save ca.der from the laptop to fix it.
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.verify_mode = ssl.CERT_REQUIRED
    with open("ca.der", "rb") as f:
        ctx.load_verify_locations(cadata=f.read())
    return ctx


TLS = make_tls()


def api(method, query=""):
    addr = socket.getaddrinfo(HOST, 443)[0][-1]
    s = socket.socket()
    s.settimeout(POLL_SECONDS + 15)
    try:
        s.connect(addr)
        s = TLS.wrap_socket(s, server_hostname=HOST)
        # HTTP/1.0 so the server closes the connection when the reply is complete
        s.write("GET /bot%s/%s?%s HTTP/1.0\r\nHost: %s\r\n\r\n"
                % (config.BOT_TOKEN, method, query, HOST))
        raw = b""
        while True:
            chunk = s.read(1024)
            if not chunk:
                break
            raw += chunk
    finally:
        s.close()
    return json.loads(raw.split(b"\r\n\r\n", 1)[1])


def quote(text):
    out = ""
    for b in text.encode():
        if 48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122:
            out += chr(b)
        else:
            out += "%%%02X" % b
    return out


def send(chat_id, text):
    api("sendMessage", "chat_id=%d&text=%s" % (chat_id, quote(text)))


def handle(message, booted_at):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip().lower()
    if chat_id is None:
        return
    if not config.ALLOWED_CHAT_ID:
        send(chat_id, "Setup mode. Your chat ID is %d. Put it in config.py." % chat_id)
    elif chat_id != config.ALLOWED_CHAT_ID:
        return  # strangers get no reply and no action
    elif text.startswith("/wake"):
        wake_laptop()
        send(chat_id, "Wake signal sent.")
    elif text.startswith("/ping"):
        send(chat_id, "ESP32 online, up %d min." % ((time.time() - booted_at) // 60))
    else:
        send(chat_id, "Commands: /wake  /ping")


def main():
    assert len(magic_packet(config.LAPTOP_MAC)) == 102  # 6 + 16 * 6 bytes
    wdt = machine.WDT(timeout=120000)  # restart the board if the loop hangs for 2 minutes
    offset = None  # None = just booted
    booted_at = 0
    while True:
        wdt.feed()
        try:
            if not connect_wifi():
                raise OSError("no Wi-Fi")
            if offset is None:
                ntptime.settime()  # certificate checks need the real date
                booted_at = time.time()
                # Skip commands sent while the board was off, so an old /wake
                # does not fire after a power cut.
                last = api("getUpdates", "offset=-1")["result"]
                offset = last[-1]["update_id"] + 1 if last else 0
            updates = api("getUpdates", "timeout=%d&offset=%d" % (POLL_SECONDS, offset))["result"]
            for update in updates:
                offset = update["update_id"] + 1
                handle(update.get("message") or {}, booted_at)
        except Exception as e:
            print("error:", repr(e))
            time.sleep(5)


if __name__ == "__main__":  # runs at power-on; lets tests import the functions without starting the loop
    main()
