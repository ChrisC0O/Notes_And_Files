find / -perm -4000 -type f 2>/dev/null -exec sh -c '
for f; do
  [ -x "$f" ] && printf "%-50s | %s\n" "$f" "$(getcap "$f" 2>/dev/null)"
done
' sh {} +
