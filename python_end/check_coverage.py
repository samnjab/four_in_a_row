
if __name__ == '__main__':
    import coverage
    import pytest
    from python_ta import contracts
    cov = coverage.Coverage(include=['four_in_a_row.py'])
    cov.start()

    # call your code for coverage
    pytest.main(["test_class_def.py"])

    cov.stop()
    cov.save()

    # generate the html report (similar to what pyTA does)
    # and print the coverage percentage
    percent_covered = cov.html_report()

    print(f'Code coverage: {percent_covered :.2f}%')

    # code below will open up the detailed report in the browser (like pyTA).
    import webbrowser
    import os.path

    webbrowser.open(f'file://{os.path.dirname(__file__)}/htmlcov/index.html')
