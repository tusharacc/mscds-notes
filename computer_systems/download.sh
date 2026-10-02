#!/usr/bin/env bash
set -euo pipefail

# read -rsp "LMS session ID: " SESSION_ID
echo

BASE="https://dfl-courses.iiit.ac.in"
COURSE="asset-v1:IIITH_2026_04+MSDS101+2+type@asset+block@"
COOKIE_NAME="sessionid"   # change if your cookie is named differently
SESSION_ID="1|emjg9pukwdr5ds4w86gw8o9basrz6zro|Hd3g18jI4Ebt|IjVhNzFkZWUyYzEzNjc1YTdjOGU3N2VkNjYyNjg1ZDk1ZmYzODc1MmZkMjY2MzQ2ZDVmNjgwYmNmM2VmY2ZhMDMi:1x7OJ3:WcaykmMxsd54QfuTJf2p8iSVYcuN728ai07d6rCLHXo"
fetch () {
  local week="$1"; shift
  mkdir -p "videos/week-${week}"
  for f in "$@"; do
    echo "Week ${week}: ${f}"
    curl --fail --location --retry 3 --continue-at - \
         --cookie "${COOKIE_NAME}=${SESSION_ID}" \
         --output "videos/week-${week}/${f}" \
         "${BASE}/${COURSE}${f}"
  done
}

fetch 1 \
  "1.1.1._Introduction.mp4" \
  "1.1.2._A_Primer_on_Clocks_and_Cycle.mp4" \
  "1.1.3._MIPS_Instruction_Set.mp4" \
  "1.1.4._Operands_and_Registers.mp4" \
  "1.1.5._Memory_Address.mp4" \
  "1.1.6._Memory_Organization.mp4"

fetch 2 \
  "2.1.1._Control_Instructions.mp4" \
  "2.1.2._Branching_and_Converting_Simple_Line_of_Code.mp4" \
  "2.1.3._Procedure_Calls.mp4" \
  "2.1.4._Jump_and_Link.mp4" \
  "2.1.5._Data_Movement_among_Registers.mp4" \
  "2.1.6._Dealing_with_Characters.mp4" \
  "2.1.7._Large_Constants__Instruction_Sets__Endian-ness.mp4"

fetch 3 \
  "3.1.1._ASCII_vs_Binary__2_s_Complement.mp4" \
  "3.1.2._Signed-Unsigned__Sign_Extension__Alternative_Representations.mp4" \
  "3.1.3._Addition__Multiplication.mp4" \
  "3.1.4._Division.mp4"

fetch 4 \
  "4.1.1._Sign_and_Magnitude_Representation.mp4" \
  "4.1.2._Exponent_Representation.mp4" \
  "4.1.3._FP_Addition__Multiplication.mp4" \
  "4.1.4._Fixed_Point__Subword_Parallelism.mp4"

fetch 5 \
  "1.1.1._Von_Neumann_Architecture_fixed_nametag_intro.mp4" \
  "1.1.2._Latches_and_Clocks_fixed_nametag_intro.mp4" \
  "1.1.3._Pipelining_Notion_fixed_nametag_intro.mp4" \
  "1.1.4._A_5-Stage_Pipeline_fixed_nametag_intro.mp4" \
  "1.1.5._Conflicts___Problems_due_to_Pipelining_fixed_nametag_intro.mp4"

fetch 6 \
  "2.1.1._Data_Hazard_fixed_nametag_intro.mp4" \
  "2.1.2._Bypassing_fixed_nametag_intro.mp4" \
  "2.1.3._Examples_0-1-2_fixed_nametag_intro.mp4" \
  "2.1.4._Examples_3-4_fixed_nametag_intro.mp4" \
  "2.1.5._Control_Hazard_fixed_nametag_intro.mp4"

fetch 7 \
  "3.1.1._Branch_Predictors_fixed_nametag_intro.mp4" \
  "3.1.2._Bimodal_Predictor_fixed_nametag_intro.mp4" \
  "3.1.3._Out-of-Order_Execution_fixed_nametag_intro.mp4" \
  "3.1.4._Out-of-Order_Execution_Example_fixed_nametag_intro.mp4" \
  "3.1.5._Cache_Hierarchy_fixed_nametag_intro.mp4"

fetch 8 \
  "1.1.1._Origins_of_the_Internet_-_Part_1.mp4" \
  "1.1.1._Origins_of_the_Internet_-_Part_2.mp4" \
  "1.1.2._Key_Concepts_in_Networking_1_-_Part_1.mp4" \
  "1.1.2._Key_Concepts_in_Networking_1_-_Part_2.mp4" \
  "1.1.2._Key_Concepts_in_Networking_1_-_Part_3.mp4" \
  "1.1.3._Key_Concepts_in_Networking_2_-_Part_1.mp4" \
  "1.1.3._Key_Concepts_in_Networking_2_-_Part_2.mp4" \
  "1.1.3._Key_Concepts_in_Networking_2_-_Part_3.mp4" \
  "1.1.4._Key_Concepts_in_Networking_3_-_Part_1.mp4" \
  "1.1.4._Key_Concepts_in_Networking_3_-_Part_2.mp4" \
  "1.1.5._How_does_the_Internet_work__-_Part_1.mp4" \
  "1.1.5._How_does_the_Internet_work__-_Part_2.mp4" \
  "1.1.5._How_does_the_Internet_work__-_Part_3.mp4"

fetch 9 \
  "2.1.1._Computer_Networking_Devices_-_Part_1.mp4" \
  "2.1.1._Computer_Networking_Devices_-_Part_2.mp4" \
  "2.1.1._Computer_Networking_Devices_-_Part_3.mp4" \
  "2.1.2._Functioning_of_a_Router_-_Part_1.mp4" \
  "2.1.2._Functioning_of_a_Router_-_Part_2.mp4" \
  "2.1.3._Longest_Prefix_Match__LPM_.mp4" \
  "2.1.4._Longest_Prefix_Match_Implementation__LPM__-_Part_1.mp4" \
  "2.1.4._Longest_Prefix_Match_Implementation__LPM__-_Part_2.mp4" \
  "2.1.4._Longest_Prefix_Match_Implementation__LPM__-_Part_3.mp4" \
  "2.1.5._Crossbar_Switching_in_Router.mp4" \
  "2.1.6._Broadcast_and_Collision_Domain_-_Part_1.mp4" \
  "2.1.6._Broadcast_and_Collision_Domain_-_Part_2.mp4"

fetch 10 \
  "3.1.1._Internet_in_Practice_and_Firewall_-_Part_1.mp4" \
  "3.1.1._Internet_in_Practice_and_Firewall_-_Part_2.mp4" \
  "3.1.1._Internet_in_Practice_and_Firewall_-_Part_3.mp4" \
  "3.1.2._Network_Optimization_and_Traffic_Management_-_Part_1.mp4" \
  "3.1.2._Network_Optimization_and_Traffic_Management_-_Part_2.mp4" \
  "3.1.3._Network_Address_Translation__NAT__-_Part_1.mp4" \
  "3.1.3._Network_Address_Translation__NAT__-_Part_2.mp4" \
  "3.1.4._Static_NAT_and_PAT_-_Part_1.mp4" \
  "3.1.4._Static_NAT_and_PAT_-_Part_2.mp4" \
  "3.1.5._Dynamic_NAT_and_PAT.mp4" \
  "3.1.6._Dynamic_NAT.mp4" \
  "3.1.7._Policy_NAT_and_Twice_NAT_-_Part_1.mp4" \
  "3.1.7._Policy_NAT_and_Twice_NAT_-_Part_2.mp4"

echo "Done."