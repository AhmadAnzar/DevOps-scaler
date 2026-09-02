# Shell Scripting

**Name:** Anzar,  24BCS10289

These Bash scripts practise working with files, input, variables, functions, conditions, and loops.

## 1. Create a folder and file - hello.sh
```bash
#!/usr/bin/env bash
mkdir -p hello
printf '%s\n' "This is my logfile" > hello/app.log
cat hello/app.log
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./hello.sh
This is my logfile
```

## 2. Overwrite a file - data.sh
```bash
#!/usr/bin/env bash
mkdir -p data
printf '%s\n' "This is a log file." > data/app.log
cat data/app.log
printf '%s\n' "This is my file" > data/app.log
cat data/app.log
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./data.sh
This is a log file.
This is my file
```

## 3. Append to a file - script1.sh
```bash
#!/usr/bin/env bash
mkdir -p test
echo "This is file1" > test/app.log
echo "This is file2" >> test/app.log
cat test/app.log
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./script1.sh
This is file1
This is file2
```

## 4. Take input - input.sh
```bash
#!/usr/bin/env bash
read -r -p "Enter your name: " name
read -r -p "Enter your roll number: " roll_number
read -r -p "Enter your comment: " comment

echo "My name is $name"
echo "My roll number is $roll_number"
echo "My comment is: $comment"
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./input.sh
Enter your name: Anzar
Enter your roll number: 24BCS10289
Enter your comment: linux
My name is Anzar
My roll number is 24BCS10289
My comment is: linux
```
## 5. Variables - variable.sh
```bash
#!/usr/bin/env bash
name="Anzar"
roll_number="24BCS10289"
comment="learning Bash"
echo "My name is $name"
echo "My roll number is $roll_number"
echo "I am $comment
```
## 6. Function - function.sh
```bash
#!/usr/bin/env bash
show_info() {
	echo "This is a function"
}
```

## 7. For loop - loop.sh
```bash
#!/usr/bin/env bash
for ((i=0;i<=5;i++)); do
	echo "This is iteration number $i"
done
```
## 8. System report - system_info.sh
```bash
#!/usr/bin/env bash
read -r -p "Enter your name: " name
read -r -p "Enter your roll number: " roll_number
read -r -p "Enter your comment: " comment
current_date=$(date)
host_name=$(hostname)
user_name=$(whoami)
report_directory="system_report"
process_file="$report_directory/processes.txt"

mkdir -p "$report_directory"
touch "$process_file"

echo ""
echo "=== System Information ==="
echo "Current date: $current_date"
echo "Hostname: $host_name"
echo "Username: $user_name"

echo ""
echo "=== Disk Usage ==="
df -h

echo ""
echo "=== Running Processes ==="
ps aux > "$process_file"
echo "Process information saved to $process_file"
cat "$process_file"

echo ""
echo "=== User Details ==="
echo "My name is $name"
echo "My roll number is $roll_number"
echo "My comment is: $comment"
```

**Sample input:** `Anzar`, `24BCS10289`, `Learning Bash`

```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./system_info.sh
Enter your name: Anzar
Enter your roll number: 24BCS10289
Enter your comment: Learning Bash

=== System Information ===
Current date: Mon Aug 31 12:45:20 UTC 2026
Hostname: ip-172-31-38-20
Username: ubuntu

=== Disk Usage ===
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       7.6G  2.4G  5.2G  32% /
tmpfs           475M     0  475M   0% /dev/shm

=== Running Processes ===
Process information saved to system_report/processes.txt
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.5  21932 12840 ?        Ss   10:29   0:02 /sbin/init
ubuntu    2481  0.0  0.2  17820  6120 pts/0    Ss   12:42   0:00 -bash
[more processes follow]

=== User Details ===
My name is Anzar
My roll number is 24BCS10289
My comment is: Learning Bash
```

## 9. If-else condition - `condition.sh`
```bash
#!/usr/bin/env bash
read -r -p "Enter your age: " age
if [ "$age" -lt 0 ]; then
	echo "Invalid age. Please enter a valid age."
else
	echo "You are an adult."
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./condition.sh
Enter your age: 21
You are an adult.
```
## 10. While loop with input - while_loop.sh
```bash
#!/usr/bin/env bash
while true; do
	read -r -p "Enter a number (or 'q' to quit): " input

	if [[ "$input" == "q" ]]; then
		echo "Exiting the loop."
		break
	elif ! [[ "$input" =~ ^[0-9]+$ ]]; then
		echo "Invalid input. Please enter a valid number."
		continue
	fi

	echo "You entered: $input"
done
```
```
ubuntu@ip-172-31-38-20:~/devops-2028/shellscripting$ ./while_loop.sh
Enter a number (or 'q' to quit): 7
You entered: 7
Enter a number (or 'q' to quit): q
Exiting the loop.
```