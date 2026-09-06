"""
Example usage of Automated Program Repair AST Patcher Skill.
"""

from client import AutomatedProgramRepair


def main():
    print("=== Automated Program Repair AST Patcher Demonstration ===")
    apr = AutomatedProgramRepair()

    # Buggy code with off-by-one boundary: `i < len(arr)` vs `i <= len(arr)`
    buggy_code = (
        "def find_last_index(arr, target):\n"
        "    result = -1\n"
        "    for i in range(len(arr)):\n"
        "        if arr[i] < target:\n"
        "            result = i\n"
        "    return result\n"
    )

    print("Buggy Source Code (Fault at line 4):")
    print(buggy_code)

    candidates = apr.generate_candidate_patches(buggy_code, faulty_line=4)
    print(f"Generated {len(candidates)} Candidate Patches:")

    for idx, c in enumerate(candidates, 1):
        print(f"\nCandidate #{idx} (Mutation Operator: {c['operator']}):")
        print(c["patched_code"])

    # Test patch validation
    def test_case(ns):
        fn = ns.get("find_last_index")
        return fn([10, 20, 30], 20) == 1

    for idx, c in enumerate(candidates, 1):
        passed = apr.validate_patch(c["patched_code"], test_case)
        print(f"Candidate #{idx} Test Execution: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
