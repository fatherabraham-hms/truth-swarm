#!/usr/bin/env python3
"""
Simple runner script for the meTTa eval agent
"""

import sys
import os

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run the agent
from meTTa_eval_agent_refactored import crypto_detection_agent

if __name__ == "__main__":
    crypto_detection_agent.run()
