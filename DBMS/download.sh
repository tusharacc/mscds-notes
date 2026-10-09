et -euo pipefail

SESSION_ID="1|lgm7n7xtqngdllbqgsv53kg3c8ufi834|Kmc1eDF1cXSO|IjZkMGFiNDE3OWQ1NjE4M2ZkMzRjNDllMmRhNTI3MGNlZTI1OWRmODEzZDM5ZjE2MzdkMDViZmU5NGQ1Y2I3NTAi:1xDvdQ:Y0WJC0baKZHQvdpltZgZ2VRUlxNC8tJeoWojZiDmF8c"
echo

BASE="https://dfl-courses.iiit.ac.in"
COURSE="asset-v1:IIITH+MDS301+v1+type@asset+block@"
COOKIE_NAME="sessionid"   # Open edX default; verify in DevTools → Application → Cookies if needed

mkdir -p "videos/dbms/week-1"

for f in \
  "Introduction_to_the_Course_Week_1_Introduction_Database_Manageme__1__intro_added.mp4" \
  "Introduction_to_the_Course_Week_1_Introduction_Database_Manageme_intro_added.mp4" \
  "Introduction_to_the_Course_Week_1_Introduction_Database_Manageme__2__intro_added.mp4"
do
  echo "Downloading: $f"
  curl --fail --location --retry 3 --continue-at - \
       --cookie "${COOKIE_NAME}=${SESSION_ID}" \
       --output "videos/dbms/week-1/${f}" \
       "${BASE}/${COURSE}${f}"
done

echo "Done."