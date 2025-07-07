import csv
import json
from datetime import datetime
import os

# Sample incident structure
class Incident:
    def __init__(self, timestamp, source, attack_type, severity, status):
        self.timestamp = timestamp
        self.source = source
        self.attack_type = attack_type
        self.severity = severity
        self.status = status

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "source": self.source,
            "attack_type": self.attack_type,
            "severity": self.severity,
            "status": self.status
        }

# Core function to handle exporting and alerting
def process_and_export_incidents(incidents, export_dir="logs"):
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(export_dir, exist_ok=True)

    csv_path = os.path.join(export_dir, f"incidents_{date_str}.csv")
    json_path = os.path.join(export_dir, f"incidents_{date_str}.json")

    alerts = []

    # Write CSV
    with open(csv_path, mode='w', newline='') as csv_file:
        fieldnames = ["timestamp", "source", "attack_type", "severity", "status"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for incident in incidents:
            writer.writerow(incident.to_dict())

    # Write JSON
    with open(json_path, mode='w') as json_file:
        json.dump([incident.to_dict() for incident in incidents], json_file, indent=4)

    # Trigger alerts
    for incident in incidents:
        if incident.severity.lower() == "high" or incident.attack_type.lower() == "unknown":
            alerts.append(incident)

    if alerts:
        print("\n🔔 ALERT TRIGGERED:")
        for incident in alerts:
            print(f"[{incident.timestamp}] {incident.source} → {incident.attack_type} ({incident.severity.upper()})")
    else:
        print("\n✅ No critical alerts detected.")

    print(f"\n✔️ CSV exported to: {csv_path}")
    print(f"✔️ JSON exported to: {json_path}")


# Example usage
if __name__ == "__main__":
    sample_incidents = [
        Incident("2025-04-07 10:15:00", "Firewall", "SQL Injection", "High", "Blocked"),
        Incident("2025-04-07 10:16:45", "Web Server", "XSS", "Medium", "Mitigated"),
        Incident("2025-04-07 10:18:12", "Proxy", "Unknown", "Low", "Logged"),
    ]
    process_and_export_incidents(sample_incidents)
