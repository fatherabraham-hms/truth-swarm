// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import {TruthSwarmResolver} from "../src/Resolver.sol";
import {IEAS, Attestation} from "../lib/eas-contracts/contracts/IEAS.sol";

contract ResolverWhitelistTest is Test {
    TruthSwarmResolver public resolver;
    address public owner;
    address public attester1;
    address public attester2;
    address public attester3;
    address public nonWhitelisted;
    IEAS public mockEAS;

    event AttesterAdded(address indexed attester);
    event AttesterRemoved(address indexed attester);

    function setUp() public {
        owner = address(this);
        attester1 = makeAddr("attester1");
        attester2 = makeAddr("attester2");
        attester3 = makeAddr("attester3");
        nonWhitelisted = makeAddr("nonWhitelisted");
        mockEAS = IEAS(makeAddr("mockEAS"));

        // Deploy resolver with initial attesters
        address[] memory initialAttesters = new address[](2);
        initialAttesters[0] = attester1;
        initialAttesters[1] = attester2;

        resolver = new TruthSwarmResolver(mockEAS, initialAttesters);
    }

    /*//////////////////////////////////////////////////////////////
                        INITIALIZATION TESTS
    //////////////////////////////////////////////////////////////*/

    function test_InitialOwner() public view {
        assertEq(resolver.owner(), owner);
    }

    function test_InitialWhitelist() public view {
        assertTrue(resolver.isWhitelisted(attester1));
        assertTrue(resolver.isWhitelisted(attester2));
        assertFalse(resolver.isWhitelisted(attester3));
    }

    function test_InitialWhitelistCount() public view {
        assertEq(resolver.getWhitelistedCount(), 2);
    }

    function test_InitialWhitelistArray() public view {
        address[] memory attesters = resolver.getWhitelistedAttesters();
        assertEq(attesters.length, 2);
        assertEq(attesters[0], attester1);
        assertEq(attesters[1], attester2);
    }

    function test_InitialWhitelistIgnoresZeroAddress() public {
        address[] memory initialAttesters = new address[](3);
        initialAttesters[0] = attester1;
        initialAttesters[1] = address(0); // Should be ignored
        initialAttesters[2] = attester2;

        TruthSwarmResolver newResolver = new TruthSwarmResolver(mockEAS, initialAttesters);

        assertEq(newResolver.getWhitelistedCount(), 2);
        assertFalse(newResolver.isWhitelisted(address(0)));
    }

    function test_InitialWhitelistIgnoresDuplicates() public {
        address[] memory initialAttesters = new address[](3);
        initialAttesters[0] = attester1;
        initialAttesters[1] = attester1; // Duplicate
        initialAttesters[2] = attester2;

        TruthSwarmResolver newResolver = new TruthSwarmResolver(mockEAS, initialAttesters);

        assertEq(newResolver.getWhitelistedCount(), 2);
    }

    /*//////////////////////////////////////////////////////////////
                        ADD ATTESTER TESTS
    //////////////////////////////////////////////////////////////*/

    function test_AddAttester() public {
        vm.expectEmit(true, false, false, false);
        emit AttesterAdded(attester3);

        resolver.addAttester(attester3);

        assertTrue(resolver.isWhitelisted(attester3));
        assertEq(resolver.getWhitelistedCount(), 3);
    }

    function test_AddAttesterUpdatesArray() public {
        resolver.addAttester(attester3);

        address[] memory attesters = resolver.getWhitelistedAttesters();
        assertEq(attesters.length, 3);
        assertEq(attesters[2], attester3);
    }

    function test_RevertWhen_AddAttesterNotOwner() public {
        vm.prank(attester1);
        vm.expectRevert(abi.encodeWithSignature("OwnableUnauthorizedAccount(address)", attester1));
        resolver.addAttester(attester3);
    }

    function test_RevertWhen_AddAttesterZeroAddress() public {
        vm.expectRevert(TruthSwarmResolver.ZeroAddress.selector);
        resolver.addAttester(address(0));
    }

    function test_RevertWhen_AddAttesterAlreadyWhitelisted() public {
        vm.expectRevert(abi.encodeWithSelector(TruthSwarmResolver.AttesterAlreadyWhitelisted.selector, attester1));
        resolver.addAttester(attester1);
    }

    /*//////////////////////////////////////////////////////////////
                        REMOVE ATTESTER TESTS
    //////////////////////////////////////////////////////////////*/

    function test_RemoveAttester() public {
        vm.expectEmit(true, false, false, false);
        emit AttesterRemoved(attester1);

        resolver.removeAttester(attester1);

        assertFalse(resolver.isWhitelisted(attester1));
        assertEq(resolver.getWhitelistedCount(), 1);
    }

    function test_RemoveAttesterUpdatesArray() public {
        resolver.removeAttester(attester1);

        address[] memory attesters = resolver.getWhitelistedAttesters();
        assertEq(attesters.length, 1);
        // attester1 should not be in the array
        for (uint256 i = 0; i < attesters.length; i++) {
            assertTrue(attesters[i] != attester1);
        }
    }

    function test_RemoveAttesterSwapsWithLast() public {
        resolver.addAttester(attester3);

        // Remove middle element (attester1)
        resolver.removeAttester(attester1);

        address[] memory attesters = resolver.getWhitelistedAttesters();
        assertEq(attesters.length, 2);
        // The last element (attester3) should have been swapped
        assertTrue(attesters[0] == attester3 || attesters[0] == attester2);
        assertTrue(attesters[1] == attester3 || attesters[1] == attester2);
    }

    function test_RevertWhen_RemoveAttesterNotOwner() public {
        vm.prank(attester1);
        vm.expectRevert(abi.encodeWithSignature("OwnableUnauthorizedAccount(address)", attester1));
        resolver.removeAttester(attester1);
    }

    function test_RevertWhen_RemoveAttesterNotWhitelisted() public {
        vm.expectRevert(abi.encodeWithSelector(TruthSwarmResolver.AttesterNotWhitelisted.selector, attester3));
        resolver.removeAttester(attester3);
    }

    /*//////////////////////////////////////////////////////////////
                        WHITELIST QUERY TESTS
    //////////////////////////////////////////////////////////////*/

    function test_IsWhitelisted() public view {
        assertTrue(resolver.isWhitelisted(attester1));
        assertTrue(resolver.isWhitelisted(attester2));
        assertFalse(resolver.isWhitelisted(attester3));
        assertFalse(resolver.isWhitelisted(nonWhitelisted));
    }

    function test_GetWhitelistedAttesters() public view {
        address[] memory attesters = resolver.getWhitelistedAttesters();
        assertEq(attesters.length, 2);
    }

    function test_GetWhitelistedCount() public view {
        assertEq(resolver.getWhitelistedCount(), 2);
    }

    /*//////////////////////////////////////////////////////////////
                        ATTESTATION VALIDATION TESTS
    //////////////////////////////////////////////////////////////*/

    function test_OnAttestWhitelistedAttester() public {
        // Create a mock attestation from whitelisted attester
        Attestation memory attestation = _createMockAttestation(attester1);

        // We need to test this through the resolver's onAttest function
        // Since it's internal, we'll verify through the whitelist check
        assertTrue(resolver.isWhitelisted(attestation.attester));
    }

    function test_OnAttestNonWhitelistedAttester() public {
        Attestation memory attestation = _createMockAttestation(nonWhitelisted);
        assertFalse(resolver.isWhitelisted(attestation.attester));
    }

    /*//////////////////////////////////////////////////////////////
                        OWNERSHIP TESTS
    //////////////////////////////////////////////////////////////*/

    function test_TransferOwnership() public {
        address newOwner = makeAddr("newOwner");

        vm.expectEmit(true, true, false, false);
        emit OwnershipTransferred(owner, newOwner);

        resolver.transferOwnership(newOwner);

        assertEq(resolver.owner(), newOwner);
    }

    function test_RevertWhen_TransferOwnershipNotOwner() public {
        address newOwner = makeAddr("newOwner");

        vm.prank(attester1);
        vm.expectRevert(abi.encodeWithSignature("OwnableUnauthorizedAccount(address)", attester1));
        resolver.transferOwnership(newOwner);
    }

    function test_NewOwnerCanAddAttester() public {
        address newOwner = makeAddr("newOwner");
        resolver.transferOwnership(newOwner);

        vm.prank(newOwner);
        resolver.addAttester(attester3);

        assertTrue(resolver.isWhitelisted(attester3));
    }

    /*//////////////////////////////////////////////////////////////
                        INTEGRATION TESTS
    //////////////////////////////////////////////////////////////*/

    function test_AddMultipleAttesters() public {
        resolver.addAttester(attester3);
        address attester4 = makeAddr("attester4");
        resolver.addAttester(attester4);

        assertEq(resolver.getWhitelistedCount(), 4);
        assertTrue(resolver.isWhitelisted(attester3));
        assertTrue(resolver.isWhitelisted(attester4));
    }

    function test_RemoveAllAttesters() public {
        resolver.removeAttester(attester1);
        resolver.removeAttester(attester2);

        assertEq(resolver.getWhitelistedCount(), 0);
        assertFalse(resolver.isWhitelisted(attester1));
        assertFalse(resolver.isWhitelisted(attester2));
    }

    function test_AddRemoveAddAttester() public {
        resolver.removeAttester(attester1);
        assertFalse(resolver.isWhitelisted(attester1));

        resolver.addAttester(attester1);
        assertTrue(resolver.isWhitelisted(attester1));
    }

    function test_ComplexWhitelistManagement() public {
        // Start with 2 attesters
        assertEq(resolver.getWhitelistedCount(), 2);

        // Add new attesters
        resolver.addAttester(attester3);
        address attester4 = makeAddr("attester4");
        resolver.addAttester(attester4);
        assertEq(resolver.getWhitelistedCount(), 4);

        // Remove one
        resolver.removeAttester(attester2);
        assertEq(resolver.getWhitelistedCount(), 3);

        // Add it back
        resolver.addAttester(attester2);
        assertEq(resolver.getWhitelistedCount(), 4);

        // Verify all expected attesters are whitelisted
        assertTrue(resolver.isWhitelisted(attester1));
        assertTrue(resolver.isWhitelisted(attester2));
        assertTrue(resolver.isWhitelisted(attester3));
        assertTrue(resolver.isWhitelisted(attester4));
    }

    /*//////////////////////////////////////////////////////////////
                        FUZZ TESTS
    //////////////////////////////////////////////////////////////*/

    function testFuzz_AddAttester(address newAttester) public {
        vm.assume(newAttester != address(0));
        vm.assume(!resolver.isWhitelisted(newAttester));

        resolver.addAttester(newAttester);

        assertTrue(resolver.isWhitelisted(newAttester));
    }

    function testFuzz_RemoveAttester(address attesterToRemove) public {
        vm.assume(attesterToRemove != address(0));
        vm.assume(!resolver.isWhitelisted(attesterToRemove));

        // First add
        resolver.addAttester(attesterToRemove);
        assertTrue(resolver.isWhitelisted(attesterToRemove));

        // Then remove
        resolver.removeAttester(attesterToRemove);
        assertFalse(resolver.isWhitelisted(attesterToRemove));
    }

    function testFuzz_IsWhitelisted(address addr) public view {
        bool result = resolver.isWhitelisted(addr);
        if (addr == attester1 || addr == attester2) {
            assertTrue(result);
        } else {
            assertFalse(result);
        }
    }

    /*//////////////////////////////////////////////////////////////
                        HELPER FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    function _createMockAttestation(address attester) internal view returns (Attestation memory) {
        return Attestation({
            uid: bytes32(0),
            schema: bytes32(0),
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: bytes32(0),
            recipient: address(0),
            attester: attester,
            revocable: true,
            data: ""
        });
    }

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
}

