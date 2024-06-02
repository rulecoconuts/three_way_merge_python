from typing import Self
from io import TextIOWrapper

class MergeResult:
    def __init__(self, original :list[str], a:list[str], b:list[str], merged_from_a: set[int], merged_from_b: set[int]):
        self.original = original
        self.a = a
        self.b = b
        self.merged_from_a = merged_from_a
        self.merged_from_b = merged_from_b

    def contains_conflicts(self)->bool:
        return MergeResult.__contains_conflicts(self.a, self.merged_from_a) or MergeResult.__contains_conflicts(self.b, self.merged_from_b)
    
    def write_to_file(self, file: TextIOWrapper):
        index = 0
        a_len = len(self.a)
        b_len = len(self.b)
        a_marker = "<" * 11
        b_marker = ">" * 11
        a = self.a
        b=self.b
        merged_from_a = self.merged_from_a
        merged_from_b = self.merged_from_b

        while index < a_len or index < b_len:
            line = ""
            if index < a_len and index < b_len:
                if index in merged_from_a and index in merged_from_b:
                    # line unchanged in both versions
                    line = a[index]
                elif index in merged_from_a:
                    # line was changed only in a
                    line = a[index]
                elif index in merged_from_b:
                    # line was changed only in b
                    line = b[index]
                else:
                    line = a_marker + a[index] + "\n" + b_marker + b[index]
            elif index < a_len:
                # only a is valid
                line = a[index]
            elif index < b_len:
                # only b is valid
                line = b[index]
                
            file.write(line)
            index+=1



    @staticmethod
    def __contains_conflicts(v:list[str], merged:set[int])->bool:
        return len(MergeResult.__get_conflicts(v, merged))>0

    @staticmethod
    def __get_conflicts(v:list[str], merged:set[int])->set[int]:
        all_set = set(range(len(v)))
        return all_set.difference(merged)
    
    @classmethod
    def merge(cls, original: list[str], a:list[str], b:list[str]) -> Self:
        merged_from_a:set[int] = set()
        merged_from_b:set[int] = set()
        a_len = len(a)
        b_len = len(b)
        original_len = len(original)
        max_len_to_check = max(original_len, a_len, b_len)
        for line in range(max_len_to_check):
            original_line = None if line >= original_len else original[line]
            a_line = None if line >= a_len else a[line]
            b_line = None if line >= b_len else b[line]

            if original_line is not None and a_line is not None and b_line is not None:
                if original_line == a_line and original_line == b_line:
                    # The line in original has not changed. Take the change from both versions
                    merged_from_a.add(line)
                    merged_from_b.add(line)
                elif original_line == a_line and original_line != b_line:
                    # only version b was changed. Take change from b
                    merged_from_b.add(line)
                elif original_line == b_line and original_line != a_line:
                    # only version a was changed. Take change from a
                    merged_from_a.add(line)
                elif original_line != b_line and original_line != a_line and a_line == b_line:
                    # both versions made the same change
                    merged_from_a.add(line)
                    merged_from_b.add(line)
            elif a_line is not None and b_line is not None:
                # both versions have grown larger than the lines in original
                if a_line == b_line:
                    # both versions made the same change
                    merged_from_a.add(line)
                    merged_from_b.add(line)
            elif original_line is not None and b_line is not None:
                # the change only exists in version a
                merged_from_a.add(line)
            elif original_line is not None and a_line is not None:
                # the change only exists in version b
                merged_from_b.add(line)


        return cls(original, a, b, merged_from_a, merged_from_b)