"""Hebrew transcription regressions.

Run from the repository root:
    python -m unittest discover -s test/writing -p "test*.py" -v

The word fixtures come from BHSA 2021, commit
4db00e2157915495e1a4d3d57e41223df24775da.
"""

import unittest

from tf.writing.transcription import Transcription


class HebrewTranscriptionTest(unittest.TestCase):
    def testPsalm72Qere(self):
        """Psalm 72:17, word 322495: convert the accent and final nun."""
        word, trailer = Transcription.suffix_and_finales("JIN.O97WN")
        self.assertEqual(word, "JIN.O97Wn")
        self.assertEqual(trailer, " ")
        expected = "\u05d9\u05b4\u05e0\u05bc\u05b9\u05a2\u05d5\u05df"
        self.assertEqual(Transcription.to_hebrew(word), expected)

    def testOrdinaryWord(self):
        """Psalm 1:1, word 310660, agrees with BHSA g_word_utf8."""
        self.assertEqual(
            Transcription.to_hebrew("<:AYA97T"),
            "\u05e2\u05b2\u05e6\u05b7\u05a2\u05ea",
        )

    def testReverseConversion(self):
        """The qere word also converts back to its ETCBC transcription."""
        word = "\u05d9\u05b4\u05e0\u05bc\u05b9\u05a2\u05d5\u05df"
        self.assertEqual(Transcription().from_hebrew(word), "JIN.O97Wn")

    def testRelatedAccentsRemainDistinct(self):
        tr = Transcription()
        for token, accent in (("97", "\u05a2"), ("93", "\u05aa")):
            with self.subTest(token=token):
                self.assertEqual(Transcription.to_hebrew(token), accent)
                self.assertEqual(tr.from_hebrew(accent), token)

    def testConversionWithoutAccentReordering(self):
        self.assertEqual(
            Transcription.to_hebrew_x("JIN.O97Wn"),
            "\u05d9\u05b4\u05e0\u05bc\u05b9\u05a2\u05d5\u05df",
        )

    def testAccentStripping(self):
        self.assertEqual(
            Transcription.to_hebrew_v("JIN.O97Wn"),
            "\u05d9\u05b4\u05e0\u05bc\u05b9\u05d5\u05df",
        )
        self.assertEqual(
            Transcription.to_hebrew_c("JIN.O97Wn"),
            "\u05d9\u05e0\u05d5\u05e0",
        )

    def testUnknownTokenIsPreserved(self):
        self.assertEqual(
            Transcription.to_hebrew("JIN.O99Wn"),
            "\u05d9\u05b4" "\u05e0\u05bc\u05b9" "99" "\u05d5\u05df",
        )


if __name__ == "__main__":
    unittest.main()
