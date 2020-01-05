from blog.preprocessors.backtick import BacktickTest
from blog.preprocessors.emoji import EmojiTest

Tests=[BacktickTest,
       EmojiTest]

def init_suite(tests):
    import unittest
    suite=unittest.TestSuite()
    result=unittest.TestResult()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))
    runner=unittest.TextTestRunner()
    return runner.run(suite)

if __name__=="__main__":
    init_suite(Tests)

