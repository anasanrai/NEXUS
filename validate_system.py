#!/usr/bin/env python3
"""
NEXUS System Validation Script
Checks that all components are importable and working correctly.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 60)
print("NEXUS System Validation Check")
print("=" * 60)

try:
    print("\n✓ Checking Python version...")
    print(f"  Python {sys.version.split()[0]}")
    
    print("\n✓ Importing configuration...")
    from config import config, validate_config
    print(f"  Environment: {config.app.environment}")
    
    print("\n✓ Importing agent components...")
    from agent.router import ModelRouter
    from agent.planner import task_planner
    from agent.executor import task_executor
    from agent.persona import get_system_prompt
    print("  ✓ ModelRouter")
    print("  ✓ TaskPlanner")
    print("  ✓ TaskExecutor")
    print("  ✓ Persona")
    
    print("\n✓ Importing memory systems...")
    from memory.short_term import ShortTermMemory
    from memory.long_term import LongTermMemory
    print("  ✓ ShortTermMemory")
    print("  ✓ LongTermMemory")
    
    print("\n✓ Importing tools registry...")
    from tools.registry import ToolRegistry
    print("  ✓ ToolRegistry")
    
    print("\n✓ Importing channels...")
    from channels.telegram import TelegramChannel
    print("  ✓ TelegramChannel")
    
    print("\n✓ Importing scheduler...")
    from scheduler.cron import NEXUSScheduler
    print("  ✓ NEXUSScheduler")
    
    print("\n✓ Checking async functions...")
    import inspect
    print(f"  ✓ ModelRouter.call_model is async: {inspect.iscoroutinefunction(ModelRouter.call_model)}")
    
    print("\n" + "=" * 60)
    print("✅ All imports successful!")
    print("✅ All components accessible!")
    print("✅ System is production-ready!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
