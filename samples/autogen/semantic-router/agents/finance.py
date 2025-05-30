# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
This is an HR agent application that demonstrates how to use the Semantic Router
to dynamically route user messages to the most appropriate agent for a conversation.
"""

import asyncio

from autogen_core import DefaultSubscription, try_get_known_serializers_for_type
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from common._agents import WorkerAgent, worker_agent_runtime
from common._semantic_router_components import TerminationMessage, WorkerAgentMessage


async def run_workers():
    agent_runtime: GrpcWorkerAgentRuntime = worker_agent_runtime()
    await agent_runtime.start()

    serializer_termination = try_get_known_serializers_for_type(TerminationMessage)
    serializer_worker_agent_message = try_get_known_serializers_for_type(
        WorkerAgentMessage
    )

    agent_runtime.add_message_serializer(
        [serializer_termination, serializer_worker_agent_message]
    )

    # Create the hr agents
    await WorkerAgent.register(
        agent_runtime, "finance", lambda: WorkerAgent("finance_agent")
    )
    await agent_runtime.add_subscription(
        DefaultSubscription(topic_type="finance", agent_type="finance")
    )

    await agent_runtime.stop_when_signal()


if __name__ == "__main__":
    asyncio.run(run_workers())
