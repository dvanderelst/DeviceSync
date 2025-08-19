# port_menu.py
import sys
import serial.tools.list_ports as lp

def scan_for_ports():
    ports = []
    for p in lp.comports():
        ports.append({
            "device": p.device,
            "description": p.description or "",
            "manufacturer": getattr(p, "manufacturer", None),
            "product": getattr(p, "product", None),
            "vid": f"{p.vid:04X}" if getattr(p, "vid", None) is not None else None,
            "pid": f"{p.pid:04X}" if getattr(p, "pid", None) is not None else None,
            "serial_number": getattr(p, "serial_number", None),
        })
    # stable order: by device path then description
    ports.sort(key=lambda d: (d["device"] or "", d["description"]))
    return ports

def format_menu_entry(entry, idx):
    vidpid = f"{entry['vid']}:{entry['pid']}" if entry["vid"] and entry["pid"] else "----:----"
    man = entry["manufacturer"] or ""
    prod = entry["product"] or ""
    desc = entry["description"] or ""
    extra = " • ".join([s for s in (man, prod, desc) if s])
    return f"[{idx}] {entry['device']}  ({vidpid})  {extra}"

def select_port(allow_refresh=True, default_first_if_single=True):
    """
    Shows a small numeric menu of serial devices and returns the chosen device path (str) or None.
    - 'r' refreshes the list (if allow_refresh=True)
    - 'q' cancels and returns None
    - If exactly one device is found and default_first_if_single=True, it's auto-selected
    """
    while True:
        ports = scan_for_ports()
        if not ports:
            print("No serial devices found.")
            return None

        print("\nSelect a device:")
        for i, e in enumerate(ports):
            print(format_menu_entry(e, i))
        prompt = "Enter number"
        if allow_refresh: prompt += " | r=refresh"
        prompt += " | q=cancel: "

        choice = input(prompt).strip().lower()

        if choice == "q": return None
        if allow_refresh and choice == "r": continue
        if choice.isdigit():
            i = int(choice)
            if 0 <= i < len(ports): return ports[i]
        print("Invalid choice. Try again.")

if __name__ == "__main__":
    sel = select_port()
    print("Selected:", sel)
