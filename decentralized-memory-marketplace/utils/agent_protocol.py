from uagents import Protocol
from datetime import datetime
from typing import Literal, TypedDict, Dict, List, Union
import uuid
from pydantic.v1 import UUID4, Field
from uagents_core.models import Model
from uagents_core.protocol import ProtocolSpecification

class Metadata(TypedDict, total=False):
    mime_type: str
    role: str

class TextContent(Model):
    type: Literal["text"] = "text"
    text: str

class Resource(Model):
    uri: str
    metadata: dict[str, str]

class ResourceContent(Model):
    type: Literal["resource"] = "resource"
    resource_id: UUID4 = Field(default_factory=uuid.uuid4)
    resource: Resource | list[Resource]

class MetadataContent(Model):
    type: Literal["metadata"] = "metadata"
    metadata: dict[str, str]

class StartSessionContent(Model):
    type: Literal["start-session"] = "start-session"

class EndSessionContent(Model):
    type: Literal["end-session"] = "end-session"

class StartStreamContent(Model):
    type: Literal["start-stream"] = "start-stream"
    stream_id: UUID4 = Field(default_factory=uuid.uuid4)

class EndStreamContent(Model):
    type: Literal["end-stream"] = "end-stream"
    stream_id: UUID4

AgentContent = Union[
    TextContent,
    ResourceContent,
    MetadataContent,
    StartSessionContent,
    EndSessionContent,
    StartStreamContent,
    EndStreamContent,
]

class AgentMessage(Model):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    msg_id: UUID4 = Field(default_factory=uuid.uuid4)
    content: list[AgentContent]

class AgentAcknowledgement(Model):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_msg_id: UUID4
    metadata: dict[str, str] | None = None

agent_protocol_spec = ProtocolSpecification(
    name="MemoryMarketplaceProtocol",
    version="1.0.0",
    interactions={
        AgentMessage: {AgentAcknowledgement},
        AgentAcknowledgement: set(),
    },
)

agent_proto = Protocol(spec=agent_protocol_spec)

def create_text_message(text: str) -> AgentMessage:
    return AgentMessage(content=[TextContent(text=text)])

def create_metadata_message(metadata: Dict[str, str]) -> AgentMessage:
    return AgentMessage(content=[MetadataContent(metadata=metadata)])

@agent_proto.on_message(AgentMessage)
async def handle_agent_message(ctx, sender, msg: AgentMessage):
    ctx.logger.info(f"Received message from {sender}")
    await ctx.send(sender, AgentAcknowledgement(acknowledged_msg_id=msg.msg_id))

@agent_proto.on_message(AgentAcknowledgement)
async def handle_acknowledgement(ctx, sender, msg: AgentAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")