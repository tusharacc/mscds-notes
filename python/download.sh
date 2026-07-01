#!/bin/bash

# ============================================================
# LMS Video Downloader - IIITH MDS102
# Python Core and Applied Concepts for Reliable Data Science
# ============================================================

SESSION_ID="1|tfox9717nld80nrlwjw22yehaexc7nyo|4YGJLOi0qNwU|ImU0MTM2OGZmM2NlNTVmYTkwNzRkMjcxOGRmNzVlMmU2NTkxNmI2ZGQ5NmRmN2E1ODY5M2Q3ZjE2MzUzMTQ1ODci:1wbFvv:8WTXwsVQYu6llbF-nY-Bg3ShqblPFUPPQqmidWI_OU4"
COOKIE="sessionid=${SESSION_ID}"
BASE_URL="https://dfl-courses.iiit.ac.in"

download_video() {
  local week_dir="$1"
  local filename="$2"
  local url="$3"

  mkdir -p "$week_dir"

  echo "Downloading: $filename -> $week_dir/"
  curl -L \
    --cookie "$COOKIE" \
    --output "${week_dir}/${filename}" \
    --progress-bar \
    --retry 3 \
    --retry-delay 5 \
    "$url"

  if [ $? -eq 0 ]; then
    echo "  ✓ Done: ${week_dir}/${filename}"
  else
    echo "  ✗ Failed: ${week_dir}/${filename}"
  fi
}

# ============================================================
# WEEK 1
# ============================================================
download_video "week1" "1.1.1._Act_of_Programming.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.1.1._Act_of_Programming.mp4"

download_video "week1" "1.1.2._Syntax_and_Semantics.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.1.2._Syntax_and_Semantics.mp4"

download_video "week1" "1.1.3._Programming_Errors.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.1.3._Programming_Errors.mp4"

download_video "week1" "1.1.4._Python_Features_and_Course_Overview.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.1.4._Python_Features_and_Course_Overview.mp4"

download_video "week1" "1.2.1._Variables_as_Abstractions.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.2.1._Variables_as_Abstractions.mp4"

download_video "week1" "1.2.2._Types_in_Python_PL.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@1.2.2._Types_in_Python_PL.mp4"

# ============================================================
# WEEK 2
# ============================================================
download_video "week2" "2.1.1._Expressions_and_Operators.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@2.1.1._Expressions_and_Operators.mp4"

download_video "week2" "2.1.2._Walrus_and_Assignment_Expressions.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@2.1.2._Walrus_and_Assignment_Expressions.mp4"

download_video "week2" "2.2.1._Lambda_Expressions.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@2.2.1._Lamba_Expressions.mp4"

# ============================================================
# WEEK 3
# ============================================================
download_video "week3" "3.1.1._Reasoning_About_Assignment.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@3.1.1._Reasoning_About_Assignment.mp4"

download_video "week3" "3.2.1._Syntax_and_Semantics_of_Conditional_Branching.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@3.2.1._Syntax_and_Semantics_of_Conditional_Branching.mp4"

# ============================================================
# WEEK 6
# ============================================================
download_video "week6" "6.1.1._Shallow_Copy_vs_Deep_Copy.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@6.1.1._Shallow_Copy_vs_Deep_Copy.mp4"

download_video "week6" "6.2.1._Functions_as_Abstraction.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@6.2.1._Functions_as_Abstraction.mp4"

# ============================================================
# WEEK 7
# ============================================================
download_video "week7" "7.1.1._Function_Calls_and_Default_Values.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@7.1.1._Function_Calls_and_Default_Values.mp4"

download_video "week7" "7.2.1._Function_Calls_and_Return_Values.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@7.2.1._Function_Calls_and_Return_Values.mp4"

# ============================================================
# WEEK 8
# ============================================================
# NOTE: 8.1.1 is a YouTube embed (https://www.youtube.com/watch?v=jqGnHIwFJ1Y)
# It cannot be downloaded with curl. Use yt-dlp if needed:
# mkdir -p week8 && yt-dlp -o "week8/8.1.1._Docstrings_and_Higher_Order_Functions.mp4" "https://www.youtube.com/watch?v=jqGnHIwFJ1Y"

download_video "week8" "8.2.1._Dictionaries_in_Python.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@8.2.1._Dictionaries_in_Python.mp4"

# ============================================================
# WEEK 9
# ============================================================
download_video "week9" "9.1.1._Recursion_and_BST_Part_1.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@9.1.1._Recursion_and_BST_Part_1.mp4"

download_video "week9" "9.1.2._Recursion_and_BST_Part_2.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@9.1.2._Recursion_and_BST_Part_2.mp4"

download_video "week9" "9.2.1._AVL_Height_Balanced_Trees.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@9.2.1_AVL__Height_Balanced__Trees.mp4"

# ============================================================
# WEEK 10
# ============================================================
download_video "week10" "10.1.1._Intro_to_Spectral_Soil_Modeler_Project.mp4" \
  "${BASE_URL}/asset-v1:IIITH+MDS102+2026_04+type@asset+block@10.1.1._Intro_to_Spectral_Soil_Modeler_Project.mp4"

echo ""
echo "============================================================"
echo "All downloads complete!"
echo "============================================================"