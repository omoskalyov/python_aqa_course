is_test_run_passed = False


def test_rerun():
    global is_test_run_passed
    _is_test_run_passed = is_test_run_passed
    is_test_run_passed = True
    assert _is_test_run_passed == True
