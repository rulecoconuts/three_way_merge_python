from merge import MergeResult

with open("test_original.txt", "r") as original_file, open(
    "test_a.txt", "r"
) as a_file, open("test_b.txt", "r") as b_file, open("test_merged.txt", "w") as out:
    result = MergeResult.merge(
        original_file.readlines(), a_file.readlines(), b_file.readlines()
    )
    result.write_to_file(out)
