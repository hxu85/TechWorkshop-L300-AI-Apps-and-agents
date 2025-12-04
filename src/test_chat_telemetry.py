#!/usr/bin/env python3
"""
Send a test message to the chat application via WebSocket
"""
import asyncio
import websockets
import json

async def test_chat():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to chat application")
            
            # Send a simple test message
            test_message = {
                "message": "Hello, this is a telemetry test",
                "image": ""
            }
            await websocket.send(json.dumps(test_message))
            print(f"✓ Sent message: {test_message['message']}")
            
            # Wait for response
            print("Waiting for response...")
            response = await asyncio.wait_for(websocket.recv(), timeout=30)
            print(f"✓ Received response (first 200 chars): {response[:200]}...")
            
            print("\n✓ Test message sent successfully!")
            print("This should have generated telemetry in Application Insights")
            
    except asyncio.TimeoutError:
        print("⚠ Timeout waiting for response, but message was sent")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat())
