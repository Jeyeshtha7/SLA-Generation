# Simple SLA generator using templates and a default LLM call (langchain). For MVP we produce text locally.
from typing import List
import textwrap

def generate_sla_from_form(service_name, uptime, response_time, penalty, compliance, extra_notes):
    sla = f"Service Level Agreement for {service_name}\n\n"
    sla += f"Guaranteed Uptime: {uptime}%\n"
    sla += f"Response Time for P1: {response_time} hours\n"
    sla += f"Penalty per hour of downtime: {penalty}\n"
    if compliance:
        sla += "Compliance Standards: " + ", ".join(compliance) + "\n"
    if extra_notes:
        sla += f"Extra Notes:\n{extra_notes}\n"
    return sla
