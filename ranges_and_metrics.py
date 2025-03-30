def sum_of_ranges(ranges):
    return sum(end - start for start, end in ranges)

def union_ranges(ranges):
    # Sort ranges based on the starting index
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    # Initialize with the first range
    merged_ranges = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged_ranges[-1]

        # Check if the current range overlaps or is contiguous with the last range in the merged list
        if current_start <= last_end:
            # Merge the two ranges
            merged_ranges[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add the current range as new
            merged_ranges.append((current_start, current_end))

    return merged_ranges


def intersect_two_ranges(range1, range2):
    # Unpack the ranges
    start1, end1 = range1
    start2, end2 = range2

    # Calculate the maximum of the starting indices and the minimum of the ending indices
    intersect_start = max(start1, start2)
    intersect_end = min(end1, end2)

    # Check if the intersection is valid (the start is less than or equal to the end)
    if intersect_start <= intersect_end:
        return (intersect_start, intersect_end)
    else:
        return None  # Return an None if there is no intersection

def intersect_two_lists_of_ranges(ranges1, ranges2):
    intersection = []
    idx1 = 0
    idx2 = 0

    while idx1 < len(ranges1) and idx2 < len(ranges2):
        start1, end1 = ranges1[idx1]
        start2, end2 = ranges2[idx2]
        local_intersection = intersect_two_ranges(ranges1[idx1], ranges2[idx2])

        if local_intersection:
            intersection.append(local_intersection)

        if end1 < end2:
            idx1 += 1
        else:
            idx2 += 1

    return intersection

def precision(chunk_ranges, references) -> float:
    return sum_of_ranges(intersect_two_lists_of_ranges(chunk_ranges, references)) / sum_of_ranges(chunk_ranges)


def recall(chunk_ranges, references) -> float:
    return sum_of_ranges(intersect_two_lists_of_ranges(chunk_ranges, references)) / sum_of_ranges(references)
