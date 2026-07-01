#!/bin/bash

# ============================================================
# Whisper Transcript Generator - IIITH MDS102
# Generates .txt, .srt, and .vtt transcripts for all videos
# ============================================================

# Change model as needed: tiny, base, small, medium, large
MODEL="base"

run_whisper() {
  local filepath="$1"
  local outdir="$(dirname "$filepath")"

  echo "Transcribing: $filepath"
  whisper "$filepath" \
    --model "$MODEL" \
    --output_format all \
    --output_dir "$outdir" \
    --language English
  echo "  ✓ Done: $filepath"
  echo ""
}

# ============================================================
# WEEK 1
# ============================================================
run_whisper "week1/1.1.1._Act_of_Programming.mp4"
run_whisper "week1/1.1.2._Syntax_and_Semantics.mp4"
run_whisper "week1/1.1.3._Programming_Errors.mp4"
run_whisper "week1/1.1.4._Python_Features_and_Course_Overview.mp4"
run_whisper "week1/1.2.1._Variables_as_Abstractions.mp4"
run_whisper "week1/1.2.2._Types_in_Python_PL.mp4"

# ============================================================
# WEEK 2
# ============================================================
run_whisper "week2/2.1.1._Expressions_and_Operators.mp4"
run_whisper "week2/2.1.2._Walrus_and_Assignment_Expressions.mp4"
run_whisper "week2/2.2.1._Lambda_Expressions.mp4"

# ============================================================
# WEEK 3
# ============================================================
run_whisper "week3/3.1.1._Reasoning_About_Assignment.mp4"
run_whisper "week3/3.2.1._Syntax_and_Semantics_of_Conditional_Branching.mp4"

# ============================================================
# WEEK 6
# ============================================================
run_whisper "week6/6.1.1._Shallow_Copy_vs_Deep_Copy.mp4"
run_whisper "week6/6.2.1._Functions_as_Abstraction.mp4"

# ============================================================
# WEEK 7
# ============================================================
run_whisper "week7/7.1.1._Function_Calls_and_Default_Values.mp4"
run_whisper "week7/7.2.1._Function_Calls_and_Return_Values.mp4"

# ============================================================
# WEEK 8
# ============================================================
# NOTE: 8.1.1 was a YouTube video — transcribe only if you downloaded it separately
# run_whisper "week8/8.1.1._Docstrings_and_Higher_Order_Functions.mp4"
run_whisper "week8/8.2.1._Dictionaries_in_Python.mp4"

# ============================================================
# WEEK 9
# ============================================================
run_whisper "week9/9.1.1._Recursion_and_BST_Part_1.mp4"
run_whisper "week9/9.1.2._Recursion_and_BST_Part_2.mp4"
run_whisper "week9/9.2.1._AVL_Height_Balanced_Trees.mp4"

# ============================================================
# WEEK 10
# ============================================================
run_whisper "week10/10.1.1._Intro_to_Spectral_Soil_Modeler_Project.mp4"

echo "============================================================"
echo "All transcriptions complete!"
echo "============================================================"