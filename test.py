def can_place_in_window(window, new_distance):
    """Check if we can place the new distance in this window without violating the sliding window constraint."""
    window.sort()  # Ensure sorted order
    window.append(new_distance)  # Temporarily add the new distance
    window.sort()  # Sort again to keep it in order

    # Check the sliding window rule: no more than 4 elements within 10 units of each other
    for i in range(len(window) - 4 + 1):
        if window[i + 3] - window[i] > 10:
            window.remove(new_distance)  # Undo the addition
            return False
    return True


def max_objects_recursive(
    objects, n_windows, assigned_windows, current_window=0, memo={}
):
    """Recursive function to find the maximum number of objects placed across all windows."""
    # If we've processed all objects, return the current count
    if not objects:
        return 0

    # Memoization to avoid recalculating the same state
    memo_key = (tuple(tuple(window) for window in assigned_windows), current_window)
    if memo_key in memo:
        return memo[memo_key]

    # Try to place the current object in each window
    max_placed = 0
    for window_idx in range(n_windows):
        # Check if we can place the current object in the window
        if can_place_in_window(assigned_windows[window_idx], objects[0][window_idx]):
            # Temporarily place the object in this window
            assigned_windows[window_idx].append(objects[0][window_idx])
            # Recur for the rest of the objects
            placed = 1 + max_objects_recursive(
                objects[1:], n_windows, assigned_windows, current_window + 1, memo
            )
            # Backtrack (remove the object from this window)
            assigned_windows[window_idx].remove(objects[0][window_idx])
            # Track the maximum number of objects placed
            max_placed = max(max_placed, placed)

    # Memoize the result for the current state
    memo[memo_key] = max_placed
    return max_placed


def test_one_object_per_window():
    objects = [[10], [20], [30], [40]]  # One distance per object
    result = max_objects_recursive(objects, 1, [[] for _ in range(1)])
    assert result == 4, f"Expected 4, but got {result}"


test_one_object_per_window()
