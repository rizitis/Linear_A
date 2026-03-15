
\version "2.24.3"
\header {
  title = "ΔΙΣΚΟΣ ΤΗΣ ΦΑΙΣΤΟΥ"
  subtitle = "Πυρρίχιος Χορός τῶν Κουρήτων"
  composer = "~1700 π.Χ. — Φαιστός, Κρήτη"
  tagline = "Αμφίδρομη σπιραλική ανάγνωση: Α΄ έξω→κέντρο → Β΄ κέντρο→έξω"
}

\paper {
  #(set-paper-size "a4")
  indent = 20\mm
  system-system-spacing.basic-distance = #18
  score-system-spacing.basic-distance = #20
  top-margin = 12\mm
  bottom-margin = 12\mm
  left-margin = 10\mm
  right-margin = 10\mm
}

#(set-global-staff-size 16)

\layout {
  \context {
    \Score
    \override BarNumber.font-size = #-1
  }
}

melody = {
  \clef treble
  \key a \minor
  \mark \markup { \bold "ΕΙΣΟΔΟΣ — Πλευρά Α΄" }
  \time 5/4
  r4\mp r4 gis4 cis4 e4 | % 1. A1
  \time 3/4
  e4 d4 r4 | % 2. A2
  cis4 f4 a4 | % 3. A3
  cis4 cis4 bes4 | % 4. A4
  \time 5/4
  r4 r4 d4 d4 bes,4 | % 5. A5
  \time 4/4
  d4 f4 a4 r4 | % 6. A6
  \time 3/4
  d4 gis4 e4 | % 7. A7
  \time 4/4
  r4 r4 cis4 e4 | % 8. A8
  \time 3/4
  gis4 f4 d4 | % 9. A9
  \time 5/4
  r4 r4 f4 d4 d4 | % 10. A10
  \time 4/4
  cis4\mf f4 d4 a4 | % 11. A11
  \time 5/4
  r4 r4 a4 e4 cis'4 | % 12. A12
  \time 2/4
  bes4 bes4 | % 13. A13
  \time 6/4
  r4 d4 a4 gis4 e4 e4 | % 14. A14
  \time 2/4
  cis4 cis4 | % 15. A15
  \mark \markup { \bold "★ ΚΟΡΥΦΩΣΗ" }
  \time 4/4
  r4\f r4 gis4\accent f4\accent | % ★ REFRAIN Α΄ % 16. A16
  \time 7/4
  r4 r4 d4 d4 d4 f4 cis'4 | % 17. A17
  \time 2/4
  bes,4 e4 | % 18. A18
  \time 4/4
  r4 r4 gis4\accent f4\accent | % ★ REFRAIN Α΄ % 19. A19
  \time 6/4
  r4 d4 a4 gis4 e4 e4 | % 20. A20
  \time 2/4
  cis4 cis4 | % 21. A21
  \time 4/4
  r4 r4 gis4\accent f4\accent | % ★ REFRAIN Α΄ % 22. A22
  \time 7/4
  r4\mf r4 d4 e4 a4 e4 d4 | % 23. A23
  \time 4/4
  cis4 e4 e4 d4 | % 24. A24
  \time 3/4
  gis4 f4 r4 | % 25. A25
  \time 4/4
  r4 r4 gis4 cis4 | % 26. A26
  \time 3/4
  e4 d4 d4 | % 27. A27
  gis4 bes,4 cis'4 | % 28. A28
  \time 7/4
  r4 r4 d4 d4 d4 f4 cis'4 | % 29. A29
  \time 2/4
  gis4 cis4 | % 30. A30
  \mark \markup { \bold "→ ΚΕΝΤΡΟ" }
  \time 3/4
  gis4 bes,4 cis'4 | % 31. A31
  \time 4/4
  r1\fermata | % ΚΕΝΤΡΟ — σιωπή (πόδια μόνο)
  \mark \markup { \bold "ΑΝΑΔΥΣΗ — Πλευρά Β΄" }
  \time 2/4
  f4\pp a4 | % 32. B30
  \time 4/4
  cis4 bes4 e4 a4 | % 33. B29
  \time 5/4
  r4 cis4 d4 e4 a4 | % 34. B28
  f4 f4 bes4 e4 a4 | % 35. B27
  \mark \markup { \bold "★ Χρυσή Τομή" }
  bes,4\accent\mf cis4\accent gis4 a4 e4 | % ★ REFRAIN Β΄ % 36. B26
  \time 4/4
  a4 e4 e4 e4 | % 37. B25
  \time 3/4
  a4 f4 a4 | % 38. B24
  a4 e4 d4 | % 39. B23
  \time 4/4
  d4 bes4 e4 a4 | % 40. B22
  \time 5/4
  bes,4\accent cis4\accent gis4 a4 e4 | % ★ REFRAIN Β΄ % 41. B21
  \time 3/4
  cis4\mp f4 a4 | % 42. B20
  cis4 e4 gis4 | % 43. B19
  \time 4/4
  cis4 gis4 a4 e4 | % 44. B18
  r4 f4 d4 cis4 | % 45. B17
  \time 5/4
  cis4 d4 a4 bes4 bes,4 | % 46. B16
  \time 3/4
  cis4 bes,4 cis4 | % 47. B15
  d4 e4 e4 | % 48. B14
  \time 5/4
  cis4 e4 e4 cis4 d4 | % 49. B13
  \time 4/4
  d4 a4 cis'4 cis4 | % 50. B12
  r4 f4 gis4 d4 | % 51. B11
  a4 e4 d4 d4 | % 52. B10
  bes,4 f4 e4 a4 | % 53. B9
  \time 5/4
  gis4 a4 gis4 cis4 e4 | % 54. B8
  \time 4/4
  gis4 cis4 bes4 bes,4 | % 55. B7
  d4 e4 e4 d4 | % 56. B6
  \mark \markup { \bold "ΕΠΙΣΤΡΟΦΗ" }
  bes,4\mf e4 cis4 r4 | % 57. B5
  \time 3/4
  bes,4 a4 d4 | % 58. B4
  \time 4/4
  r4 f4 e4 a4 | % 59. B3
  d4 f4 a4 d4 | % 60. B2
  \time 5/4
  r4 r4 bes,4 d4 a4 | % 61. B1
  \bar "|."
}



percussion = {
  \clef percussion
  \time 5/4
  g'4 c'4 e4 e4 e4 | % 1. A1
  \time 3/4
  e4 e4 c'4 | % 2. A2
  e4 e4 e4 | % 3. A3
  e4 e4 e4 | % 4. A4
  \time 5/4
  g'4 c'4 e4 e4 e4 | % 5. A5
  \time 4/4
  e4 e4 e4 c'4 | % 6. A6
  \time 3/4
  e4 e4 e4 | % 7. A7
  \time 4/4
  g'4 c'4 e4 e4 | % 8. A8
  \time 3/4
  e4 e4 e4 | % 9. A9
  \time 5/4
  g'4 c'4 e4 e4 e4 | % 10. A10
  \time 4/4
  e4 e4 e4 e4 | % 11. A11
  \time 5/4
  g'4 c'4 e4 e4 e4 | % 12. A12
  \time 2/4
  e4 e4 | % 13. A13
  \time 6/4
  g'4 e4 e4 e4 e4 e4 | % 14. A14
  \time 2/4
  e4 e4 | % 15. A15
  \time 4/4
  g'4 c'4\accent e4 e4 | % ★ REFRAIN Α΄ % 16. A16
  \time 7/4
  g'4 c'4 e4 e4 e4 e4 e4 | % 17. A17
  \time 2/4
  e4 e4 | % 18. A18
  \time 4/4
  g'4 c'4\accent e4 e4 | % ★ REFRAIN Α΄ % 19. A19
  \time 6/4
  g'4 e4 e4 e4 e4 e4 | % 20. A20
  \time 2/4
  e4 e4 | % 21. A21
  \time 4/4
  g'4 c'4\accent e4 e4 | % ★ REFRAIN Α΄ % 22. A22
  \time 7/4
  g'4 c'4 e4 e4 e4 e4 e4 | % 23. A23
  \time 4/4
  e4 e4 e4 e4 | % 24. A24
  \time 3/4
  e4 e4 c'4 | % 25. A25
  \time 4/4
  g'4 c'4 e4 e4 | % 26. A26
  \time 3/4
  e4 e4 e4 | % 27. A27
  e4 e4 e4 | % 28. A28
  \time 7/4
  g'4 c'4 e4 e4 e4 e4 e4 | % 29. A29
  \time 2/4
  e4 e4 | % 30. A30
  \time 3/4
  e4 e4 e4 | % 31. A31
  \time 4/4
  e4 e4 e4 e4\fermata | % ΚΕΝΤΡΟ — πόδια μόνο
  \time 2/4
  e4 e4 | % 32. B30
  \time 4/4
  e4 e4 e4 e4 | % 33. B29
  \time 5/4
  g'4 e4 e4 e4 e4 | % 34. B28
  e4 e4 e4 e4 e4 | % 35. B27
  e4 e4 e4 e4 e4 | % ★ REFRAIN Β΄ % 36. B26
  \time 4/4
  e4 e4 e4 e4 | % 37. B25
  \time 3/4
  e4 e4 e4 | % 38. B24
  e4 e4 e4 | % 39. B23
  \time 4/4
  e4 e4 e4 e4 | % 40. B22
  \time 5/4
  e4 e4 e4 e4 e4 | % ★ REFRAIN Β΄ % 41. B21
  \time 3/4
  e4 e4 e4 | % 42. B20
  e4 e4 e4 | % 43. B19
  \time 4/4
  e4 e4 e4 e4 | % 44. B18
  g'4 e4 e4 e4 | % 45. B17
  \time 5/4
  e4 e4 e4 e4 e4 | % 46. B16
  \time 3/4
  e4 e4 e4 | % 47. B15
  e4 e4 e4 | % 48. B14
  \time 5/4
  e4 e4 e4 e4 e4 | % 49. B13
  \time 4/4
  e4 e4 e4 e4 | % 50. B12
  g'4 e4 e4 e4 | % 51. B11
  e4 e4 e4 e4 | % 52. B10
  e4 e4 e4 e4 | % 53. B9
  \time 5/4
  e4 e4 e4 e4 e4 | % 54. B8
  \time 4/4
  e4 e4 e4 e4 | % 55. B7
  e4 e4 e4 e4 | % 56. B6
  e4 e4 e4 c'4 | % 57. B5
  \time 3/4
  e4 e4 e4 | % 58. B4
  \time 4/4
  g'4 e4 e4 e4 | % 59. B3
  e4 e4 e4 e4 | % 60. B2
  \time 5/4
  g'4 c'4 e4 e4 e4 | % 61. B1
  \bar "|."
}



\score {
  <<
    \new Staff \with {
      instrumentName = \markup { \column { "Λύρα" "(Κόχλος)" } }
      shortInstrumentName = "Λ."
      \override StaffSymbol.line-count = #5
    } {
      \melody
    }
    \new DrumStaff \with {
      instrumentName = \markup { \column { "Κρουστά" "(Ασπ.+Φωνή" "+Πόδια)" } }
      shortInstrumentName = "Κρ."
      drumStyleTable = #percussion-style
      \override StaffSymbol.line-count = #3
    } {
      \percussion
    }
  >>
  \layout { }
}
