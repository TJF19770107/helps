# example_client.py

原始格式: Python

```python
#!/usr/bin/env python3
"""
Example Client Agent for Community Knowledge Base

This script demonstrates how to create a simple client agent that can
participate in the community knowledge base network.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the OpenAgents source to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from openagents.agents.worker_agent import WorkerAgent, ChannelMessageContext, EventContext
from openagents.config.globals import DEFAULT_TRANSPORT_ADDRESS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommunityMemberAgent:
    """Simple agent that participates in the community knowledge base."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.client = AgentClient(agent_id=agent_id)
        self.adapter = ThreadMessagingAgentAdapter()
        
        # Register the thread messaging adapter
        self.client.register_mod_adapter(self.adapter)
        
        # Set up message handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up message and event handlers."""
        
        def message_handler(content, sender_id):
            """Handle incoming messages."""
            logger.info(f"[{self.agent_id}] Received message from {sender_id}: {content.get('text', '')}")
            
            # Respond to mentions
            text = content.get('text', '').lower()
            if f"@{self.agent_id}" in text:
                asyncio.create_task(self._handle_mention(content, sender_id))
        
        def reaction_handler(message_id, agent_id, reaction_type, action):
            """Handle reactions to messages."""
            logger.info(f"[{self.agent_id}] {agent_id} reacted with {reaction_type} to message {message_id}")
        
        # Register handlers for all channels
        channels = ["general", "ai-news", "research", "tools", "announcements"]
        for channel in channels:
            self.adapter.register_message_handler(channel, message_handler)
            self.adapter.register_reaction_handler(channel, reaction_handler)
    
    async def _handle_mention(self, content, sender_id):
        """Handle when this agent is mentioned."""
        text = content.get('text', '').lower()
        
        if "hello" in text or "hi" in text:
            await self.adapter.send_broadcast_thread_message(
                content={"text": f"Hello {sender_id}! 👋 I'm a community member interested in AI developments."},
                channel="general"
            )
        elif "help" in text:
            await self.adapter.send_broadcast_thread_message(
                content={"text": f"Hi {sender_id}! I'm here to participate in AI discussions. Try asking @ai-news-bot for the latest updates!"},
                channel="general"
            )
        else:
            await self.adapter.send_broadcast_thread_message(
                content={"text": f"Thanks for mentioning me, {sender_id}! I'm always interested in AI discussions."},
                channel="general"
            )
    
    async def connect(self, host="localhost", port=DEFAULT_TRANSPORT_ADDRESS['http']['port']):
        """Connect to the community network."""
        try:
            success = await self.client.connect_to_server(host=host, port=port)
            if success:
                logger.info(f"✅ {self.agent_id} connected to community network")
                
                # Send introduction message
                await self.adapter.send_broadcast_thread_message(
                    content={"text": f"👋 Hello community! {self.agent_id} has joined the network. Excited to learn about AI developments!"},
                    channel="general"
                )
                
                return True
            else:
                logger.error(f"❌ Failed to connect {self.agent_id}")
                return False
        except Exception as e:
            logger.error(f"❌ Connection error for {self.agent_id}: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the network."""
        try:
            # Send goodbye message
            await self.adapter.send_broadcast_thread_message(
                content={"text": f"👋 {self.agent_id} is leaving the network. Thanks for the great discussions!"},
                channel="general"
            )
            
            await asyncio.sleep(1)  # Give time for message to send
            await self.client.disconnect()
            logger.info(f"✅ {self.agent_id} disconnected")
        except Exception as e:
            logger.error(f"❌ Disconnect error for {self.agent_id}: {e}")
    
    async def participate(self):
        """Simulate participation in the community."""
        # Wait a bit after connecting
        await asyncio.sleep(5)
        
        # Ask the AI bot for a summary
        await self.adapter.send_broadcast_thread_message(
            content={"text": "@ai-news-bot summary"},
            channel="general"
        )
        
        await asyncio.sleep(10)
        
        # Share interest in a topic
        await self.adapter.send_broadcast_thread_message(
            content={"text": "I'm really interested in the latest developments in multimodal AI. Has anyone seen interesting papers recently?"},
            channel="research"
        )
        
        await asyncio.sleep(15)
        
        # Search for specific content
        await self.adapter.send_broadcast_thread_message(
            content={"text": "@ai-news-bot search transformer models"},
            channel="research"
        )


async def main():
    """Run the example client agent."""
    print("🤖 Starting Community Member Agent Example...")
    print("=" * 60)
    
    # Create a community member agent
    agent = CommunityMemberAgent("community-member-1")
    
    try:
        # Connect to the network
        print("🔌 Connecting to Community Knowledge Base network...")
        connected = await agent.connect()
        
        if not connected:
            print("❌ Failed to connect to network. Make sure the network is running!")
            print("💡 Start the network with: openagents launch-network network_config.yaml")
            return 1
        
        print("✅ Connected successfully!")
        print("🎭 Participating in community discussions...")
        
        # Participate in the community
        await agent.participate()
        
        # Keep running to receive messages
        print("👂 Listening for community messages...")
        print("🛑 Press Ctrl+C to disconnect")
        
        # Run for a while to demonstrate interaction
        for i in range(60):  # Run for 1 minute
            await asyncio.sleep(1)
            if i % 10 == 0:
                print(f"⏱️  Running... ({i+1}/60 seconds)")
        
        print("✅ Example completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping agent...")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Disconnect
        await agent.disconnect()
        print("👋 Agent disconnected")
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

```
