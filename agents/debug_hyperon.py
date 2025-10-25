#!/usr/bin/env python3
"""
Debug script to test hyperon/meTTa installation and functionality
"""

import sys
import traceback
import os

def test_hyperon_import():
    """Test if hyperon can be imported"""
    try:
        print("🔍 Testing hyperon import...")
        import hyperon
        print(f"✅ hyperon imported successfully: {hyperon.__version__}")
        return True
    except Exception as e:
        print(f"❌ hyperon import failed: {e}")
        traceback.print_exc()
        return False

def test_hyperon_basic():
    """Test basic hyperon functionality"""
    try:
        print("🔍 Testing basic hyperon functionality...")
        import hyperon
        from hyperon import MeTTa
        
        # Create a simple MeTTa instance
        metta = MeTTa()
        print("✅ MeTTa instance created successfully")
        
        # Test basic evaluation
        result = metta.run("(= (+ 1 2) 3)")
        print(f"✅ Basic evaluation successful: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Basic hyperon functionality failed: {e}")
        traceback.print_exc()
        return False

def test_hyperon_symbols():
    """Test hyperon symbol functions"""
    try:
        print("🔍 Testing hyperon symbol functions...")
        import hyperon
        from hyperon import S, E, G, V
        
        # Test S (Symbol) function
        symbol = S("test")
        print(f"✅ S() function works: {symbol}")
        
        # Test E (Expression) function
        expr = E(S("test"), S("value"))
        print(f"✅ E() function works: {expr}")
        
        # Test G (Grounding) function - needs an object with copy method
        class TestObject:
            def copy(self):
                return TestObject()
        
        test_obj = TestObject()
        grounding = G(test_obj)
        print(f"✅ G() function works: {grounding}")
        
        # Test V (Variable) function
        variable = V("test")
        print(f"✅ V() function works: {variable}")
        
        return True
    except Exception as e:
        print(f"❌ Symbol functions test failed: {e}")
        traceback.print_exc()
        return False

def test_hyperon_grounding():
    """Test hyperon grounding space"""
    try:
        print("🔍 Testing hyperon grounding space...")
        import hyperon
        from hyperon import MeTTa, GroundingSpace
        
        metta = MeTTa()
        space = GroundingSpace()
        
        # Check available methods
        print(f"🔍 GroundingSpace methods: {[m for m in dir(space) if not m.startswith('_')]}")
        
        # Try different methods
        if hasattr(space, 'add_atom'):
            space.add_atom(metta.parse_single("(= (+ 1 2) 3)")[0])
            print("✅ Grounding space add_atom successful")
        elif hasattr(space, 'add'):
            parsed = metta.parse_single("(= (+ 1 2) 3)")
            if isinstance(parsed, list) and len(parsed) > 0:
                space.add(parsed[0])
                print("✅ Grounding space add successful")
            else:
                space.add(parsed)
                print("✅ Grounding space add successful (direct)")
        else:
            print("⚠️ No add method found for GroundingSpace")
        
        return True
    except Exception as e:
        print(f"❌ Grounding space test failed: {e}")
        traceback.print_exc()
        return False

def test_memory_usage():
    """Test memory usage"""
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"🔍 Current memory usage: {memory_mb:.2f} MB")
        
        if memory_mb > 500:  # More than 500MB
            print(f"⚠️ High memory usage detected: {memory_mb:.2f} MB")
            return False
        else:
            print(f"✅ Memory usage is reasonable: {memory_mb:.2f} MB")
            return True
    except ImportError:
        print("⚠️ psutil not available, cannot check memory usage")
        return True
    except Exception as e:
        print(f"❌ Memory check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Hyperon/meTTa Debug Test")
    print("=" * 50)
    
    tests = [
        ("Hyperon Import", test_hyperon_import),
        ("Basic Functionality", test_hyperon_basic),
        ("Symbol Functions", test_hyperon_symbols),
        ("Grounding Space", test_hyperon_grounding),
        ("Memory Usage", test_memory_usage)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed! Hyperon/meTTa is working correctly.")
    else:
        print("\n⚠️ Some tests failed. This may explain the Railway deployment issues.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
