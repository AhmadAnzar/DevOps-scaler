mkdir -p test
cd test

echo "This is my logfile" > app.log
echo "Initial content set: $(cat app.log)"

echo "Enter new text to overwrite the log file:"
read -r user_input

echo "$user_input" > app.log

cat app.log