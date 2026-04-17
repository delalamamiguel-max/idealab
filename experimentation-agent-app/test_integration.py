#!/usr/bin/env python3
"""
Simple integration test for the thinking agent.
"""

import os
import sys
from unittest.mock import Mock, MagicMock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_thinking_agent_import():
    """Test that we can import the thinking agent."""
    try:
        from thinking_agent import ThinkingAgent, AgentMode
        print("✅ ThinkingAgent import successful")
        return True
    except ImportError as e:
        print(f"❌ ThinkingAgent import failed: {e}")
        return False

def test_thinking_agent_initialization():
    """Test that we can initialize the thinking agent."""
    try:
        from thinking_agent import ThinkingAgent
        
        # Mock OpenAI client
        mock_client = Mock()
        
        agent = ThinkingAgent(mock_client, model="gpt-4o", temperature=0.4)
        
        assert agent.model == "gpt-4o"
        assert agent.temperature == 0.4
        assert len(agent.thinking_history) == 0
        
        print("✅ ThinkingAgent initialization successful")
        return True
    except Exception as e:
        print(f"❌ ThinkingAgent initialization failed: {e}")
        return False

def test_agent_config_import():
    """Test that we can import agent config."""
    try:
        from agent_config import build_full_context, get_experiment_count
        print("✅ Agent config import successful")
        return True
    except ImportError as e:
        print(f"❌ Agent config import failed: {e}")
        return False

def test_app_import():
    """Test that the main app can be imported (syntax check)."""
    try:
        # Just check if the file compiles
        import py_compile
        py_compile.compile('app.py', doraise=True)
        print("✅ App.py syntax check successful")
        return True
    except Exception as e:
        print(f"❌ App.py syntax check failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running integration tests...\n")
    
    tests = [
        test_thinking_agent_import,
        test_thinking_agent_initialization,
        test_agent_config_import,
        test_app_import,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration looks good.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())