#!/usr/bin/env python3
"""
Test script to verify Application Insights telemetry is working
"""
import os
import time
from dotenv import load_dotenv
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

# Load environment
load_dotenv()

# Configure telemetry
app_insights_conn = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
if not app_insights_conn:
    print("❌ APPLICATIONINSIGHTS_CONNECTION_STRING not found!")
    exit(1)

print(f"✓ Connection string found: {app_insights_conn[:50]}...")

# Configure Azure Monitor
configure_azure_monitor(connection_string=app_insights_conn)
print("✓ Azure Monitor configured")

# Instrument OpenAI
OpenAIInstrumentor().instrument()
print("✓ OpenAI instrumented")

# Get tracer
tracer = trace.get_tracer(__name__)

# Create some test traces
print("\nGenerating test traces...")
for i in range(3):
    with tracer.start_as_current_span(f"test_trace_{i}") as span:
        span.set_attribute("test.number", i)
        span.set_attribute("test.type", "telemetry_verification")
        print(f"  Created trace {i}")
        time.sleep(0.1)

print("\n✓ Test traces created!")
print("\nNow testing OpenAI call...")

try:
    from openai import AzureOpenAI
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("gpt_deployment")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    if not all([endpoint, api_key, deployment]):
        print("⚠ OpenAI credentials not complete, skipping OpenAI test")
    else:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Say 'Hello, telemetry test!'"}],
            max_tokens=20
        )
        
        print(f"✓ OpenAI call successful: {response.choices[0].message.content}")
        
except Exception as e:
    print(f"⚠ OpenAI test failed: {e}")

print("\n" + "="*60)
print("Telemetry test complete!")
print("="*60)
print("\nWait 2-5 minutes, then check Application Insights for:")
print("  - Custom traces named 'test_trace_0', 'test_trace_1', 'test_trace_2'")
print("  - OpenAI operation traces (if OpenAI test succeeded)")
print("\nNote: There is typically a 2-5 minute delay before data appears")
print("in Application Insights.")
